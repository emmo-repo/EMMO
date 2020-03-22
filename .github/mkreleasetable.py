#!/usr/bin/env python3
"""Generates a release table.
"""
import os
import argparse
from glob import glob
from distutils.version import LooseVersion

import semver


emmo_base_url = 'http://emmo.info/emmo'
pages_base_url = ('https://raw.githubusercontent.com/emmo-repo/'
                  'emmo-repo.github.io/master')

template = """\
<head>
  <link rel="stylesheet" type="text/css" href="../css/style.css">
</head>
<table class"reltable">
  <tr>
    <th>Version</th>
    <th>Ontology IRI</th>
    <th>Inferred ontology IRI</th>
    <th>HTML documentation</th>
    <th>PDF documentation</th>
  </tr>
{versions}
</table>
"""

def release_table(pages_dir, unstable_version=None):
    """Returns generated release table."""
    entries = []
    versions = [os.path.basename(d)
                for d in glob(os.path.join(pages_dir, 'versions', '*'))]

    for version in sorted(versions,
                          key=lambda v: semver.parse_version_info(v),
                          reverse=True):
        lines = []
        name = 'unstable' if version == 'unstable_version' else version
        emmo_url = '%s/%s' % (emmo_base_url, version)
        pages_url = '%s/versions/%s' % (pages_base_url, version)
        inferred_url = '%s/emmo-inferred.owl' % pages_url
        html_url = '%s/emmo.html' % pages_url
        pdf_url = '%s/emmo.pdf' % pages_url
        lines.append('  <tr>')
        lines.append('    <td>%s</td>' % name)
        lines.append('    <td><a href="%s" target="_blank">%s</a></td>' % (
            emmo_url, emmo_url))
        lines.append('    <td><a href="%s" target="_blank">%s</a></td>' % (
            emmo_url + '/emmo-inferred', inferred_url))
        lines.append('    <td><a href="%s" target="_blank">%s</a></td>' % (
            version, html_url))
        lines.append('    <td><a href="%s" target="_blank">%s</a></td>' % (
            version, pdf_url))
        lines.append('  </tr>')
        entries.append('\n'.join(lines))
    table = template.format(versions='\n'.join(entries))
    return table


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'pages_dir', metavar='DIR',
        help='Path to root directory to checkout out EMMO-repo GitHub Pages.')
    parser.add_argument(
        '--unstable-version', '-u',
        help='Version to mark as unstable in the table.')
    parser.add_argument(
        '--output', '-o',
        help='Write table to this file instead of standard output.')
    args = parser.parse_args()

    table = release_table(
        args.pages_dir,
        unstable_version=args.unstable_version,
    )

    if args.output:
        with open(args.output, 'wt') as f:
            f.write(table)
    else:
        print(table)


if __name__ == '__main__':
    main()
