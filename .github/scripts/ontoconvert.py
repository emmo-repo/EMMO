#!/usr/bin/env python
"""Converts file format of input ontology and write it out output file(s).
"""
import os
import argparse

from rdflib import Graph, URIRef
from rdflib.util import guess_format

from emmo.utils import read_catalog


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'input',
        help='IRI/file to OWL source.')
    parser.add_argument(
        'output',
        help='Output file name.')
    parser.add_argument(
        '--input-format', '-f',
        help='Input format (default is to infer from input.')
    parser.add_argument(
        '--output-format', '-F',
        help='Output format (default is to infer from output.')
    parser.add_argument(
        '--recursive', '-r', action='store_true',
        help='Whether to also convert imported ontologies recursively. '
        'The output is written to a directory structure matching the input. '
        'This requires Protege catalog files to be present.')
    parser.add_argument(
        '--squash', '-s', action='store_true',
        help='Whether to also squash imported ontologies into a single output '
        'file.')

    args = parser.parse_args()

    # Inferred default input and output file formats
    if args.input_format:
        input_format = args.input_format
    else:
        input_format = guess_format(args.input)

    if args.output_format:
        output_format = args.output_format
    else:
        output_format = guess_format(args.output)
    if not output_format:
        output_format = 'xml'

    # Perform conversion
    if args.recursive:
        convert_imported(args.input, args.output,
                         input_format=input_format,
                         output_format=output_format)
    elif args.squash:
        return squash_imported(args.input, args.output,
                        input_format=input_format,
                        output_format=output_format)
    else:
        g = Graph()
        g.parse(args.input, format=input_format)
        g.serialize(destination=args.output, format=output_format)


def convert_imported(input, output, input_format=None, output_format='xml',
                     catalog_file='catalog-v001.xml'):
    """Convert imported ontologies.

    Store the output in a directory structure matching the source
    files.  This require catalog file(s) to be present.
    """
    inroot = os.path.dirname(os.path.abspath(input))
    outroot = os.path.dirname(os.path.abspath(output))
    d, dirs = read_catalog(inroot, catalog_file=catalog_file, recursive=True,
                           return_paths=True)

    # Create output dirs and copy catalog files
    outext = os.path.splitext(output)[1]
    for indir in dirs:
        outdir = os.path.normpath(
            os.path.join(outroot, os.path.relpath(indir, inroot)))
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        with open(os.path.join(indir, catalog_file), mode='rt') as f:
            s = f.read()
        for path in d.values():
            newpath = os.path.splitext(path)[0] + outext
            s = s.replace(os.path.basename(path), os.path.basename(newpath))
        with open(os.path.join(outdir, catalog_file), mode='wt') as f:
            f.write(s)

    outpaths = set()
    def recur(graph, outext):
        for imported in graph.objects(predicate=URIRef(
                'http://www.w3.org/2002/07/owl#imports')):
            inpath = d[str(imported)]
            outpath = os.path.splitext(os.path.normpath(
                os.path.join(outroot, os.path.relpath(
                    inpath, inroot))))[0] + outext
            if outpath not in outpaths:
                outpaths.add(outpath)
                g = Graph()
                g.parse(inpath, format=input_format)
                g.serialize(destination=outpath, format=output_format)
                recur(g, outext)

    # Write output files
    g = Graph()
    g.parse(input, format=input_format)
    g.serialize(destination=output, format=output_format)
    recur(g, outext)


def squash_imported(input, output, input_format=None, output_format='xml',
                     catalog_file='catalog-v001.xml'):
    """Convert imported ontologies and squash them into a single file.

    Store the output in a directory structure matching the source
    files.  This require catalog file(s) to be present.
    """
    inroot = os.path.dirname(os.path.abspath(input))
    if os.path.exists(os.path.join(inroot, catalog_file)):
        d = read_catalog(inroot, catalog_file=catalog_file, recursive=True)
    else:
        d = {}

    imported = set()
    def recur(g):
        for s, p, o in g.triples(
                (None, URIRef('http://www.w3.org/2002/07/owl#imports'), None)):
            g.remove((s, p, o))
            iri = d.get(str(o), str(o))
            if iri not in imported:
                imported.add(iri)
                g2 = Graph()
                g2.parse(iri, format=input_format)
                recur(g2)
                for t in g2.triples((None, None, None)):
                    graph.add(t)

    graph = Graph()
    graph.parse(input, format=input_format)
    recur(graph)
    graph.serialize(destination=output, format=output_format)

    return graph

if __name__ == '__main__':
    g = main()
