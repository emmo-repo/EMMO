#!/usr/bin/env python3
import sys
import os
import subprocess
import time
import tempfile
import shutil
from collections import OrderedDict


# Add emmo package to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))
from emmo import get_ontology

# Load emmo and sync the resoner
emmo = get_ontology('emmo.owl')
emmo.load()
emmo.sync_reasoner()


def emmodoc(filename='emmodoc.html', format=None, figformat=None,
            figstyle='uml', **kw):
    """Generates EMMO documentation using pandoc.

    Parameters
    ----------
    filename : string
        Name of generated document.  Additional files and directories
        may also be generated.
    format : None | "html" | "pdf" | ...
        Format of generated document.  If None, the format is inferred
        from `filename`.
    figformat : None | "svg" | "pdf" | ...
        Format of generated figures.  If None, the figure format is inferred
        from `format`.
    figstyle : dict | "uml"
        Figure style.  See the `style` option of Ontology.get_dot_graph()
        for details.
    """
    root, ext = os.path.splitext(filename)
    basename = os.path.basename(root)
    if format is None:
        format = (ext[1:] if ext.startswith('.') else ext).lower()
    if figformat is None:
        figformat = dict(html='svg', pdf='pdf').get(format, 'png')

    # Relative paths
    figdir = 'html_files'  # relative path to figures
    href = filename  # relative path to documentation file

    with tempfile.TemporaryDirectory() as tmpdir:
    #if True:
    #    tmpdir = os.path.join(thisdir, 'xxx')  # XXX
        mdfile = (root + '.md' if os.path.isabs(root)
                  else os.path.join(tmpdir, basename + '.md'))
        htmldir = os.path.join(tmpdir, 'html_files')
        os.makedirs(htmldir) # XXX
        #os.makedirs(htmldir, exist_ok=True) # XXX

        # Generate document and graphs
        doc = []

        relations = get_sections('relations.md')
        introduction = relations.pop(None, '')
        #add_figs(relations, figformat=figformat, figdir=figdir)
        #make_graphs(relations, outdir=htmldir, format=figformat,
        #            style=figstyle, href=href)
        doc.append(emmo.get_vocabulary(
            sections=relations, chapter='Relations', introduction=introduction,
            template='markdown'))

        entities = get_sections('entities.md')
        introduction = entities.pop(None, '')
        add_figs(entities, figformat=figformat, figdir=figdir)
        make_graphs(entities, outdir=htmldir, format=figformat,
                    style=figstyle, href=href)
        doc.append(emmo.get_vocabulary(
            sections=entities, chapter='Entities', introduction=introduction,
            template='markdown'))

        doc.append(emmo.get_vocabulary(
            items=emmo.individuals(), chapter='Instances',
            template='markdown'))

        with open(mdfile, 'w') as f:
            f.write('\n'.join(doc) + '\n')

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
                '--toc-depth=2',
                '--variable=date:%s' % time.strftime('%B %d, %Y'),
                '--variable=author:Europeean Materials Modelling Council',
        ]
        if format in ('html', 'htm'):
            subtitle = 'Generated from <a href="%s">%s</a>' % (
                emmo.base_iri, emmo.base_iri)
            args.append('--variable=subtitle:%s' % subtitle)
            args.append('--to=html5')
            args.append('--css=%s' % os.path.join(thisdir, 'emmodoc.css'))
            args.append('--template=%s' %
                        os.path.join(thisdir, 'emmodoc-template.html'))
        elif format in ('pdf', ):
            subtitle = r'Generated from \url{%s}' % (emmo.base_iri, )
            args.append('--variable=subtitle:%s' % subtitle)
            args.append('--variable=urlcolor:blue'),
            args.append('--variable=toccolor:blue'),
            args.append('--variable=geometry:margin=2cm'),
            args.append('--from=markdown+auto_identifiers'),

        # Run pandoc
        subprocess.check_call(['pandoc'] + args, cwd=tmpdir)

        # Finalise
        curdir = os.getcwd()
        if format in ('html', 'htm'):
            if not os.path.samefile(outdir, thisdir):
                shutil.copy(os.path.join(thisdir, 'emmodoc.css'), outdir)



def make_graphs(sections, outdir='.', format='svg', style='uml', href=''):
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
    style : None | dict | "uml"
        Output style.  See ontology.gen_dot_graph() for details.
    href : str
        Base name of document to create links to.  This should typically
        be a relative path from `outdir` to "emmodoc.html".
    """
    for name in sections:
        leafs = set(sections.keys())
        leafs.discard(name)
        graph = emmo.get_dot_graph(name, relations=True, leafs=leafs,
                                   style=style)

        for node in graph.get_nodes():
            node.set_URL("%s#%s" % (href, node.get_name()))
            node.set_target("_top")

        writer = getattr(graph, 'write_' + format)
        writer(os.path.join(outdir, name + '.' + format))


def add_figs(sections, figformat='svg', figdir='html_files'):
    """Update `sections` by injecting figures after the ingress."""
    for k in sections:
        sections[k] = ('%s\n\n![The %s branch.](%s/%s.%s)\n\n' % (
            sections[k], k, figdir, k, figformat))


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
                if lines:
                    sections[section] = '\n'.join(lines)
                section = line.lstrip('#').strip()
                lines = []
            elif lines or line.strip():
                lines.append(line.rstrip('\n'))

    if section:
        sections[section] = '\n'.join(lines)

    return sections




if __name__ == '__main__':
    emmodoc('myemmo.html')
    emmodoc('myemmo.pdf')
