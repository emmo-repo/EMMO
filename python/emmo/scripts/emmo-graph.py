#!/usr/bin/env python3
"""Tool for plotting selected parts of EMMO.
"""
import sys
import os
import argparse

import pydot

# Support to run from uninstalled version by adding parent dir to sys path
thisdir = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(1, os.path.abspath(os.path.join(thisdir, '..', '..')))

import emmo


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'output',
        help='name of output file.')
    parser.add_argument(
        '--root', '-r', default='entity',
        help='Name of root node.  Defaults to "entity".')
    #parser.add_argument(
    #    '--resoner', action='store_true', default=True,
    #    help='Run the reasoner (the default)')
    parser.add_argument(
        '--no-resoner', '-n', dest='reasoner', action='store_false',
        help='Do not run the reasoner.')
    parser.add_argument(
        '--format', '-f',
        help='Format of output file.  By default it is inferred from '
        'the output file extension.')
    parser.add_argument(
        '--rankdir', '-R', default='BT', choices=['BT', 'TB', 'RL', 'LR'],
        help='Graph direction (from leaves to root).  Possible values are: '
        '"BT" (bottom-top, default), "TB" (top-bottom), "RL" (right-left) and '
        '"LR" (left-right).')
    parser.add_argument(
        '--relations', action='store_true',
        help='Create a graph with only relations.')
    args = parser.parse_args()

    onto = emmo.get_ontology('emmo.owl')
    onto.load()

    if args.reasoner:
        onto.sync_reasoner()

    #rankdir = 'RL' if args.horizontal else 'BT'
    format = args.format if args.format else os.path.splitext(
        args.output)[1][1:]

    if args.relations:
        graph = onto.get_dot_relations_graph(rankdir=args.rankdir)
    else:
        graph = onto.get_dot_graph(args.root, rankdir=args.rankdir)

    try:
        graph.write(path=args.output, format=format)
    except pydot.InvocationException as e:
        sys.stderr.write(str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
