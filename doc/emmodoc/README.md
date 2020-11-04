Generate documentation for EMMO
===============================
This directory contains the needed templates, introductory text and
figures for generating the full EMMO documentation using `ontodoc`.
Since the introduction is written in markdown, pandoc is required for
both pdf and html generation.

For a standalone html documentation including all inferred relations,
enter this directory and run

    ontodoc --template=emmo.md --format=html emmo-inferred emmo.html

Pandoc options may be adjusted with the files
[pandoc-args.yaml](pandoc-args.yaml) and
[pandoc-html-args.yaml](pandoc-html-args.yaml).

Similarly, for generating pdf documentation, enter this directory and run

    ontodoc --template=emmo.md emmo-inferred emmo.pdf

By default, we have configured pandoc to use xelatex for better unicode
support.  It is possible to change these settings in
[pandoc-args.yaml](pandoc-args.yaml) and
[pandoc-pdf-args.yaml](pandoc-pdf-args.yaml).


Content of this directory
-------------------------
### `ontodoc` templates with introductory text and document layout
  * [emmo.md](emmo.md): Main template for EMMO. It includes the other
    templates.
  * [introduction.md](introduction.md): Introductory text.
  * [relations.md](relations.md): Introduction and sections for Relations
    chapter.
  * [classes.md](classes.md): Introduction and sections for Classes
  * [figs](figs): Figures used in the introduction.

### `pandoc` configuration files
  * [emmodoc-meta.yaml](emmodoc-meta.yaml): Metadata for EMMO, like title,
    authers, abstract, etc.
  * [pandoc-args.yaml](pandoc-args.yaml): General pandoc options.
  * [pandoc-html-args.yaml](pandoc-html-args.yaml): Additional pandoc options
    for html generation.
  * [pandoc-pdf-args.yaml](pandoc-pdf-args.yaml): Additional pandoc options
    for pdf generation.
  * [pandoc-html.css](pandoc-html.css): css file used for html generation.
  * [pandoc-template.html](pandoc-template.html): Modified copy of the
    standard pandoc html template with a small adjustment for the author list.
  * [pandoc-template.tex](pandoc-template.tex): Modified copy of the
    standard pandoc latex template with a small adjustment for the author list.


Using this example as a starting point for documenting your own ontology
------------------------------------------------------------------------
For simple html documentation, you can skip all input files and simply
run `ontodoc` as

    ontodoc --format=simple-html YOUR_ONTO.owl YOUR_ONTO.html

It is also possible to include ontodoc templates using the --template
option for adding additional information and structure the document.
In this case the template may only contain `ontodoc` pre-processer
directives and inline html, but not markdown.

In order to produce output in pdf (or any other output format supported
by pandoc), you can write your `ontodoc` template in markdown (with
`ontodoc` pre-processer directives) and follow these steps to get started:

  * Copy all the files starting with `pandoc-` to a new directory.
  * Create a metadata yaml file for your ontology. You can use
    [emmodoc-meta.yaml](emmodoc-meta.yaml) as a template.
  * Update [pandoc-args.yaml](pandoc-args.yaml).  Especially change:
      - `input-files` to the name of your new yaml metadata file
      - `logo` to the path of your logo (or remove it)
      - `titlegraphic` to the path of your title figure (or remove it)
  * Optionally add `ontodoc` template files with additional information
    about your ontology and document layout.

That should be it.  Good luck!
