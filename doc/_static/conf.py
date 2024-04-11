
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'EMMO'
copyright = '2024, EMMC'
author = 'E. Ghedini, G. Goldbeck, J. Friis, A. Hashibon, G.J. Schmitz'
release = '1.0.0-rc1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

autoclass_content = 'both'
autodoc_member_order = 'bysource'

extensions = ['sphinxcontrib.globalsubs',
              'sphinx.ext.intersphinx',
              'sphinx.ext.autosectionlabel',
              'sphinx_design',
              'nbsphinx']

autosectionlabel_prefix_document = True

global_substitutions = {
}


templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix of source filenames.
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#html_theme = 'alabaster'
html_theme = 'pydata_sphinx_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
  # "show_nav_level": 4
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['../doc/_static']
html_css_files = ['custom.css']

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
html_logo = '../doc/emmo-logo.png'

# The name of an image file (within the static path) to use as favicon of the
# docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_flavicon = '../doc/figs/emmo-logo.ico'
