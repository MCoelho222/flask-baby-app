"""
Configuration file for the Sphinx documentation builder.

or the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""
from __future__ import annotations

project = 'Data API'
copyright = '2023, Pix Force'
author = 'Pix Force'
release = 'v1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.napoleon',
    'sphinx_autodoc_typehints',
    'sphinx_autodoc_defaultargs',
    'sphinx_copybutton',
    'sphinx.ext.viewcode',
    'sphinxcontrib.bibtex',
    'sphinx_design',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', '.ipynb_checkpoints']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ['.rst']

# The master toctree document.
master_doc = 'index'

bibtex_bibfiles = ['references.bib']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'friendly'
pygments_dark_style = 'monokai'

html_theme = 'sphinx_rtd_theme'

html_static_path = ['_static']

# Changing sidebar title
html_title = 'Data API'

html_theme_options = {
    'navigation_with_keys': True,
}

htmlhelp_basename = 'data_api'
# html_css_files = ['css/main.css']
# html_js_files = ['js/custom.js']


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('http://numpy.org/doc/stable/', None),
}

# substitutes the default values
docstring_default_arg_substitution = 'Default: '
autodoc_preserve_defaults = True
