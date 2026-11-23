#!/usr/bin/env python3
"""Export EMMO figures from a single draw.io sheet.

Every container cell on the sheet that has a custom ``figure`` property
(Edit Data / Ctrl+M in draw.io) is a figure frame.  Its content is exported
to ``<outdir>/<figure>.svg`` and ``<outdir>/<figure>.png``.  The frame
itself is not part of the exported image, and everything outside a frame
is ignored.

Usage:
    export-figures.py [--drawio-file doc/figures.drawio] [--outdir build/figs]
                      [--only NAME ...] [--formats svg,png] [--check-ttl]

Requires the draw.io desktop CLI (``drawio``).  On a headless machine, run
it via ``xvfb-run``.
"""
import argparse
import copy
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

WRAPPERS = ("object", "UserObject")
SKIP_DIRS = {"build", "public", "old", "fjern"}


def cell_info(elem):
    """Return (id, parent, mxCell element) for a cell, unwrapping
    <object>/<UserObject> wrappers that carry custom properties."""
    if elem.tag in WRAPPERS:
        inner = elem.find("mxCell")
        return elem.get("id"), inner.get("parent"), inner
    return elem.get("id"), elem.get("parent"), elem


def geometry(elem):
    """Return (x, y, w, h) of a vertex cell, or None."""
    _, _, cell = cell_info(elem)
    geo = cell.find("mxGeometry")
    if geo is None or cell.get("vertex") != "1":
        return None
    return tuple(float(geo.get(k, 0)) for k in ("x", "y", "width", "height"))


def load_diagrams(path):
    """Yield (diagram name, root element) for each page in the file."""
    tree = ET.parse(path)
    for diagram in tree.getroot().iter("diagram"):
        model = diagram.find("mxGraphModel")
        if model is None:
            sys.exit(
                f"{path}: page '{diagram.get('name')}' is compressed. "
                "Uncheck File > Properties > Compressed in draw.io and save."
            )
        yield diagram.get("name"), model.find("root")


def find_frames(root):
    """Return {figure name: frame element} and a list of warnings."""
    frames, warnings = {}, []
    for elem in root:
        if elem.tag in WRAPPERS and elem.get("figure"):
            name = elem.get("figure").strip()
            if name in frames:
                warnings.append(f"duplicated figure name: {name}")
            frames[name] = elem
    return frames, warnings


def descendants(root, frame_id):
    """Return all cells that (recursively) have `frame_id` as ancestor,
    in document order (which is also z-order)."""
    ids, result = {frame_id}, []
    changed = True
    elems = list(root)
    while changed:  # repeat to handle nested groups/containers
        changed = False
        for elem in elems:
            cid, parent, _ = cell_info(elem)
            if parent in ids and cid not in ids:
                ids.add(cid)
                changed = True
    for elem in elems:
        cid, _, _ = cell_info(elem)
        if cid in ids and cid != frame_id:
            result.append(elem)
    return result


def check_stray_cells(root, frames):
    """Warn about top-level cells lying on top of a frame without being
    its child (typically a shape that was not dropped into the frame)."""
    warnings = []
    layer_ids = {cell_info(e)[0] for e in root if cell_info(e)[1] == "0"}
    boxes = {n: geometry(f) for n, f in frames.items()}
    for elem in root:
        cid, parent, cell = cell_info(elem)
        if parent not in layer_ids or cell.get("style", "").find(
            "container=1"
        ) >= 0:
            continue
        g = geometry(elem)
        if g is None:
            continue
        cx, cy = g[0] + g[2] / 2, g[1] + g[3] / 2
        for name, (x, y, w, h) in boxes.items():
            if x < cx < x + w and y < cy < y + h:
                warnings.append(
                    f"cell '{cid}' lies inside frame '{name}' but is not "
                    "its child (drag it into the frame)"
                )
    return warnings


def make_figure_file(root, frame, path):
    """Write a standalone .drawio file with the content of `frame`."""
    frame_id = cell_info(frame)[0]
    mxfile = ET.Element("mxfile", compressed="false")
    diagram = ET.SubElement(mxfile, "diagram", id="fig", name="fig")
    model = ET.SubElement(diagram, "mxGraphModel")
    newroot = ET.SubElement(model, "root")
    ET.SubElement(newroot, "mxCell", id="0")
    ET.SubElement(newroot, "mxCell", id="1", parent="0")
    for elem in descendants(root, frame_id):
        elem = copy.deepcopy(elem)
        _, parent, cell = cell_info(elem)
        if parent == frame_id:
            cell.set("parent", "1")  # child geometry is frame-relative
        newroot.append(elem)
    ET.ElementTree(mxfile).write(path, encoding="utf-8", xml_declaration=True)


def run_drawio(drawio, srcdir, outdir, fmt, scale, border, no_sandbox=False):
    """Export all .drawio files in `srcdir` with a single drawio launch."""
    cmd = [drawio, "--export", "--format", fmt, "--border", str(border),
           "--output", str(outdir)]
    if fmt == "png":
        cmd += ["--scale", str(scale)]
    if fmt == "svg":
        cmd += ["--svg-theme", "light"]
    cmd.append(str(srcdir))
    # Electron refuses to run as root without --no-sandbox, and it is
    # often needed on CI runners
    if no_sandbox or os.geteuid() == 0:
        cmd.insert(1, "--no-sandbox")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode:
        sys.exit(f"drawio failed:\n{res.stdout}\n{res.stderr}")


def check_ttl(names, ttldir):
    """Check that all :illustration IRIs pointing to figs/ refer to an
    existing figure.  Returns a list of problems."""
    pattern = re.compile(r'"(https?://[^"]*/figs/([^"/]+)\.(?:png|svg))"')
    problems = []
    for ttl in sorted(Path(ttldir).rglob("*.ttl")):
        if any(part.startswith(".") or part in SKIP_DIRS
               for part in ttl.parts[:-1]):
            continue
        for lineno, line in enumerate(ttl.read_text().splitlines(), 1):
            for url, name in pattern.findall(line):
                if name not in names:
                    problems.append(f"{ttl}:{lineno}: no figure '{name}' ({url})")
    return problems


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--drawio-file", default="doc/figures.drawio",
                   help="drawio file. Default: doc/figures.drawio")
    p.add_argument("--outdir", default="build/figs",
                   help="Output directory. Default: build/figs/")
    p.add_argument("--only", nargs="+", metavar="NAME",
                   help="only export these figures")
    p.add_argument("--formats", default="svg,png",
                   help="Output formats (svg, png). Default: png")
    p.add_argument("--scale", type=float, default=2,
                   help="scale factor for PNG (default: 2)")
    p.add_argument("--border", type=int, default=4,
                   help="Border size. Default: 4")
    p.add_argument("--drawio", default=shutil.which("drawio") or "drawio",
                   help="Path to drawio executable.")
    p.add_argument("--no-sandbox", action="store_true",
                   help="Pass --no-sandbox to drawio (useful on CI)")
    p.add_argument("--check-ttl", action="store_true",
                   help="Check :illustration IRIs in *.ttl against figures.")
    p.add_argument("--list", action="store_true",
                   help="List figure names and exit (without exporting)")
    args = p.parse_args()

    frames, warnings, roots = {}, [], {}
    for page, root in load_diagrams(args.drawio_file):
        f, w = find_frames(root)
        warnings += w + check_stray_cells(root, f)
        for name, frame in f.items():
            if name in frames:
                warnings.append(f"duplicated figure name: {name}")
            frames[name] = frame
            roots[name] = root

    for w in warnings:
        print(f"WARNING: {w}", file=sys.stderr)

    status = 0
    if args.check_ttl:
        problems = check_ttl(set(frames), ".")
        for prob in problems:
            print(f"ERROR: {prob}", file=sys.stderr)
        status = 1 if problems else 0

    if args.list:
        print("\n".join(sorted(frames)))
        sys.exit(status)

    names = args.only or sorted(frames)
    missing = [n for n in names if n not in frames]
    if missing:
        sys.exit(f"unknown figure(s): {', '.join(missing)}")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmpdir:
        for name in names:
            make_figure_file(roots[name], frames[name],
                             Path(tmpdir) / f"{name}.drawio")
        for fmt in args.formats.split(","):
            run_drawio(args.drawio, tmpdir, outdir, fmt.strip(),
                       args.scale, args.border, args.no_sandbox)

    print(f"Exported {len(names)} figure(s) to {outdir}/")
    sys.exit(status)


if __name__ == "__main__":
    main()
