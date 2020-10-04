Files used for continous testing and releases on GitHub
=======================================================

**Sub-directories**
  - [workflows](workflows): YAML scripts defining GitHub Actions in response
    to push requests.
  - [scripts](scripts): Shell and puthon scripts for testing and creating
    documentation
  - [pages](pages): Local copy of
    [GitHub Pages](git@github.com:emmo-repo/emmo-repo.github.io.git)
    used for releasing documentation and inferred ontology.
    Run `scripts/update_pages.sh` to create/update this local copy and push
    to GitHub Pages.
  - [tmp](tmp): Temporary directory used when generating documentation.


Scripts
-------
Scripts found in the [scripts](scripts) sub-directory:

  * update_pages.sh [-g -p -v]

    Main script that calls the other scripts to update GitHub Pages.

    Options:
      -n  Just update local copy of GitHub Pages, do not add and commit
          changes.
      -l  Just work on local copy of GitHub Pages.  Do not push changes.
      -v  Verbose.  Print commands as they are executed.

  * init_pages.sh

    Clones GitHub Pages to .github/pages.

  * makeindex.sh

    Creates index.html file in local copy of GitHub Pages.

  * makeversions.sh [-r -v]

    Creates version sub-directories in local copy of GitHub Pages.
    Calls makedoc.sh and fixinferred.sh.

    Options:
      -r  Recreate existing sub-directories and their content.
      -v  Verbose.  Print commands as they are executed.

  * makedoc.sh inferred version outdir

    Generates EMMO documentation in html and pdf formats.

    Arguments:
      - inferred: path to inferred ontology
      - version: version to generate documentation for
      - outdir: output directory

  * fixinferred.sh owlfile

    Fix inferred ontology modifying the target file in-place.
    It is safe to run this script multiple times on the same file.

    Arguments:
      - owlfile: Inferred ontology up fix.
