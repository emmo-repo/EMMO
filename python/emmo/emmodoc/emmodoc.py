#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import time
import re
import tempfile
import shutil
import shlex
from glob import glob
from collections import OrderedDict
import xml.etree.ElementTree as ET


# Add emmo package to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology

# Load emmo and sync the resoner
emmo = get_ontology()
emmo.load()
#emmo.sync_reasoner()


abbreviations = {
    'has_part only': 'hp-o',
    'has_part some': 'hp-s',
    'is_part_of only': 'ipo-o',
    'has_member some': 'hm-s',
    'is_member_of some': 'imo-s',
    'has_abstraction some': 'ha-s',
    'is_abstraction_of some': 'iao-s',
    'has_abstract_part only': 'hap-o',
    'has_abstract_part some': 'hap-s',
    'is_abstract_part_of only': 'iapo-o',
    'is_representation_for some': 'irf-s',
    'has_representation some': 'hr-s',
    'has_space_slice some': 'hss-s',
    'is_space_slice_of some': 'isso-s',
    'has_time_slice some': 'hts-s',
    'is_time_slice_of some': 'itso-s',
    'has_projection some': 'hp-s',
    'is_projection_of some': 'ipo-s',
    'is_property_for some': 'ipf-s',
    'has_proper_part some': 'hpp-s',
    'is_proper_part_of some': 'ippo-s',
    'has_proper_part_of some': 'hppo-s',
    'has_spatial_proper_part some': 'hspp-s',
    'has_spatial_proper_part only': 'hspp-o',
    'has_spatial_direct_part min': 'hsdp-m',
    'has_spatial_direct_part some': 'hsdp-s',
    'has_spatial_direct_part exactly': 'hsdp-e',
    'has_temporal_proper_part only': 'htpp-o',
    'has_temporal_proper_part some': 'htpp-s',
    'has_temporal_direct_part only': 'htdp-o',
    'has_temporal_direct_part some': 'htdp-s',
    'encloses some': 'e-s',
    'encloses only': 'e-o',
    'is_enclosed_by some': 'ieb-s',
    'is_enclosed_by only': 'ieb-o',
    'has_sign some': 'hs-s',
    }
max_width = 668  # max width of image in px


def emmodoc(filename='emmodoc.html', format=None, figformat=None,
            figstyle='uml', figscale=None, tmpdir=None):
    """Generates EMMO documentation using pandoc.

    Parameters
    ----------
    filename : string
        Name of generated document.
    format : None | "html" | "pdf" | ...
        Format of generated document.  If None, the format is inferred
        from `filename`.
    figformat : None | "svg" | "pdf" | ...
        Format of generated figures.  If None, the figure format is inferred
        from `format`.
    figstyle : dict | "uml"
        Figure style.  See the `style` option of Ontology.get_dot_graph()
        for details.
    figscale : None | float
        Scaling factor for size of generated graphs.
    tmpdir : None | string
        By default the temporary directory in which the documentation
        is created will be deleted at return.  This option allows to
        provide a persistent name of the temporary directory for debugging.
    """
    if tmpdir is None:
        with tempfile.TemporaryDirectory() as tmpdir:
            emmodoc(filename=filename, format=format, figformat=figformat,
                    figstyle=figstyle, figscale=figscale, tmpdir=tmpdir)

    root, ext = os.path.splitext(filename)
    basename = os.path.basename(root)
    if format is None:
        format = (ext[1:] if ext.startswith('.') else ext).lower()
    if figformat is None:
        figformat = dict(html='svg', pdf='pdf').get(format, 'png')

    # Relative paths
    figdir = 'html_files'  # relative path to figures
    href = filename  # relative path to documentation file
    mdfile = (root + '.md' if os.path.isabs(root)
              else os.path.join(tmpdir, basename + '.md'))
    htmldir = os.path.join(tmpdir, 'html_files')
    os.makedirs(htmldir, exist_ok=True)

    # Generate the markdown document
    doc = []

    # Chapter 1 - introduction
    with open(os.path.join(thisdir, 'introduction.md'), 'r') as f:
        doc.append(f.read() + '\n\n')

    # Chapter 2 - EMMO relations
    relations = get_sections('relations.md')
    intro = relations.pop(None, '')
    add_figs(relations, figformat=figformat, figdir=figdir, outdir=htmldir,
             figscale=figscale)
    make_graphs(relations, outdir=htmldir, format=figformat,
                relations='is_a', style=figstyle, href=href)

    doc.append(emmo.get_vocabulary(
        sections=relations, chapter='EMMO relations', introduction=intro,
        template='markdown'))

    # Chapter 3 - EMMO classes
    entities = get_sections('emmo.md')
    intro = entities.pop(None, '')
    add_figs(entities, figformat=figformat, figdir=figdir, outdir=htmldir,
             figscale=figscale)
    make_graphs(entities, outdir=htmldir, format=figformat,
                style=figstyle, href=href)
    doc.append(emmo.get_vocabulary(
        sections=entities, chapter='EMMO classes', introduction=intro,
        template='markdown'))

    ## Chapter 4 - individuals
    #doc.append(emmo.get_vocabulary(
    #    items=emmo.individuals(), chapter='Individuals',
    #    template='markdown'))

    # Appendix - full taxonomy
    entity_graph = emmo.get_dot_graph('emmo', relations=True,
                                      edgelabels=abbreviations)
    figname = os.path.join(htmldir, 'entity_graph.' + figformat)
    writer = getattr(entity_graph, 'write_' + figformat)
    writer(figname)
    doc.append('\n\n# Appendix\n\n')
    doc.append(
        '![The complete EMMO taxonomy.](%s)\n\n' % figname)

    # Write markdown document
    with open(mdfile, 'w') as f:
        f.write('\n'.join(doc) + '\n')

    # Rescale html figure sizes
    if format in ('html', 'html5', 'htm'):
        rescale_md_figs(mdfile, figscale=figscale)

    # Copy all figures into htmldir
    for fname in glob(os.path.join(thisdir, 'figs', '*.*')):
        if not os.path.exists(os.path.join(
                htmldir, os.path.basename(fname))):
            shutil.copy(fname, htmldir)

    # Prepare arguments for pandoc
    outfile = filename if os.path.isabs(filename) else os.path.join(
        os.getcwd(), filename)
    outdir = os.path.dirname(outfile)
    metafile = os.path.join(thisdir, 'emmodoc-meta.yaml')
    args = [mdfile, metafile,
            '--output=%s' % outfile,
            '--standalone',
            '--self-contained',
            '--toc',
            '--toc-depth=3',
            '--variable=date:%s' % time.strftime('%B %d, %Y'),
            '--variable=logo:%s' % os.path.join(figdir, 'emmc-logo.png'),
            '--variable=titlegraphic:%s' % os.path.join(
                figdir, 'emmo-multidisciplinary.png'),
    ]
    if format in ('html', 'html5', 'htm'):
        #subtitle = 'Generated from <a href="%s">%s</a>' % (
        #    emmo.base_iri, emmo.base_iri)
        #args.append('--variable=subtitle:%s' % subtitle)
        args.append('--to=html5')
        args.append('--css=%s' % os.path.join(thisdir, 'emmodoc.css'))
        args.append('--template=%s' %
                    os.path.join(thisdir, 'emmodoc-template.html'))
    elif format in ('pdf', ):
        #subtitle = r'Generated from \url{%s}' % (emmo.base_iri, )
        #args.append('--variable=subtitle:%s' % subtitle)
        args.append('--variable=urlcolor:blue')
        args.append('--variable=toccolor:blue')
        args.append('--variable=geometry:margin=2cm')
        args.append('--from=markdown+auto_identifiers')
        args.append('--template=%s' %
                    os.path.join(thisdir, 'emmodoc-template.tex'))
        args.append('--variable=documentclass:report')


    # Run pandoc
    cmd = ['pandoc'] + args
    print()
    print('* Executing command: %r in %r' % (
        ' '.join(shlex.quote(s) for s in cmd), tmpdir))
    subprocess.check_call(cmd, cwd=tmpdir)

    # Finalise -- not needed for standalone documents
    #curdir = os.getcwd()
    #if format in ('html', 'htm'):
    #    if not os.path.samefile(outdir, thisdir):
    #        shutil.copy(os.path.join(thisdir, 'emmodoc.css'), outdir)



def make_graphs(sections, outdir='.', format='svg', relations=True,
                style='uml', href=''):
    """Reads `sections` dict and generate graphs for each section.

    Parameters
    ----------
    sections : dict
        A dict of section name - section ingress pairs. The section
        names should correspond to the name of the root class of the
        branch to document that section.
    outdir : str
        Directory to write generated figures to.
    format : "svg" | "pdf" | "png" | ...
        Output format.
    relations : None | True | string | sequence
        Relations to include.
    style : None | dict | "uml"
        Output style.  See ontology.gen_dot_graph() for details.
    href : str
        Base name of document to create links to.  This should typically
        be a relative path from `outdir` to "emmodoc.html".
    """
    for name in sections:
        leafs = set(sections.keys())
        leafs.discard(name)
        graph = emmo.get_dot_graph(name, relations=relations, leafs=leafs,
                                   style=style, edgelabels=abbreviations)

        for node in graph.get_nodes():
            node.set_URL("%s#%s" % (href, node.get_name().strip('"')))
            node.set_target("_top")

        writer = getattr(graph, 'write_' + format)
        writer(os.path.join(outdir, name + '.' + format))


def get_figwidths(sections, outdir='.'):
    """Returns a dict mapping section names to corresponding figure
    widths."""
    widths = {}
    widthsfile = os.path.join(outdir, 'figwidths.txt')
    if os.path.exists(widthsfile):
        with open(widthsfile, 'r') as f:
            for line in f:
                name, width = line.rstrip().split(':', 1)
                widths[name] = width

    if not set(sections.keys()).issubset(widths.keys()):
        make_graphs(sections, outdir=outdir, format='svg')
        for name in sections:
            xml = ET.parse(os.path.join(outdir, name +'.svg'))
            svg = xml.getroot()
            widths[name] = svg.attrib['width']

        with open(widthsfile, 'w') as f:
            for name, width in widths.items():
                f.write('%s: %s\n' % (name, width))

    return widths


def add_figs(sections, figformat='svg', figdir='html_files', outdir='.',
             figscale=None):
    """Update `sections` by injecting figures after the ingress."""
    scaled_widths = {}
    if figscale:
        widths = get_figwidths(sections, outdir)
        for k, v in widths.items():
            v = v.strip()
            for i in range(len(v)):
                if not v[i].isdigit():
                    break
            width = min(float(v[:i]) * figscale, max_width)
            scaled_widths[k] = '{ width=%.0fpx }' % width

    for k in sections:
        sections[k] = '%s\n\n![The %s branch.](%s/%s.%s)%s\n\n' % (
            sections[k], k, figdir, k, figformat, scaled_widths.get(k, ''))


def rescale_md_figs(filename, figscale=None):
    """Rscale all figures in markdown file `filename`.  Default figure
    scaling is assumed to be 0.7.  If `figscale` is None all scaling
    is removed."""
    patt = re.compile(r'(^\s*!\[.*\]\(.*\))((\{ *width=)(\d+)(.*\}))?')
    with open(filename, 'r') as f:
        lines = []
        while True:
            line = f.readline()
            if not line:
                break
            if line.lstrip().startswith('!['):
                m = re.match(patt, line)
                while not m:
                    line = line.rstrip('\n') + f.readline()
                    m = re.match(patt, line)
                g = m.groups()
                if figscale is None:
                    line = g[0] + '\n'
                elif g[3]:
                    line = '%s%s%.0f%s\n' % (
                        g[0], g[2], float(g[3]) / 0.7 * figscale, g[4])
                else:
                    line = g[0] + '\n'
            lines.append(line)

    with open(filename, 'w') as f:
        f.writelines(lines)


def get_sections(filename):
    """Returns a dict mapping section names to some introductionary text.

    A possible introduction to the whole "chapter" may be returned under
    the key `None`.

    Math should be allowed by enclosing it in `$$`, like `$$ y = k x + m $$`.
    """
    filename = os.path.join(thisdir, filename)
    sections = OrderedDict()
    section = None
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith(';'):
                continue
            if line.startswith('#'):
                sections[section] = '\n'.join(lines)
                section = line.lstrip('#').strip()
                lines = []
            elif lines or line.strip():
                lines.append(line.rstrip('\n'))

    if section:
        sections[section] = '\n'.join(lines)

    return sections




if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    tmpdir = os.path.join(thisdir, 'output')
    emmodoc('emmodoc.html', figscale=1.2, tmpdir=tmpdir)
    emmodoc('emmodoc.pdf', figscale=0.7, tmpdir=tmpdir)
