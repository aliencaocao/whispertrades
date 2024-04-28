# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../../src'))
project = 'Whispertrades'
copyright = '2024, Billy Cao'
author = 'Billy Cao'
release = '0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.viewcode', 'sphinx_immaterial']

templates_path = ['_templates']
exclude_patterns = []

html_theme_options = {
    "icon": {
        "repo": "fontawesome/brands/github",
        "edit": "material/file-edit-outline",
    },
    "site_url": "https://whispertrades.readthedocs.io/",
    "repo_url": "https://github.com/aliencaocao/whispertrades/",
    "repo_name": "whispertrades",
    "edit_uri": "tree/master/docs/source/",
    "globaltoc_collapse": True,
    "features": [
        "navigation.instant",
        "navigation.instant.prefetch",
        "navigation.instant.progress",
        "navigation.instant.preview",
        "navigation.tracking",
        "navigation.sections",
        "navigation.expand",
        "navigation.prune"
        "toc.follow",
        "toc.integrate",
        "navigation.top",
        "search.suggest",
        "search.highlight",
        "search.share",
        "toc.sticky",
        "navigation.sections",
        "header.autohide",
        "announce.dismiss",
        "navigation.footer",
        "content.action.view"
    ],
    "palette": [
        {
            "media": "(prefers-color-scheme)",
            "toggle": {
                "icon": "material/brightness-auto",
                "name": "Switch to light mode",
            },
        },

        {
            "media": "(prefers-color-scheme: light)",
            "scheme": "default",
            "primary": "indigo",
            "accent": "amber",
            "toggle": {
                "icon": "material/brightness-7",
                "name": "Switch to dark mode",
            },
        },
        {
            "media": "(prefers-color-scheme: dark)",
            "scheme": "slate",
            "primary": "indigo",
            "accent": "amber",
            "toggle": {
                "icon": "material/brightness-2",
                "name": "Switch to auto mode",
            },
        },
    ],
    "toc_title_is_page_title": True,
    # BEGIN: social icons
    "social": [
        {
            "icon": "fontawesome/brands/github",
            "link": "https://github.com/aliencaocao/whispertrades",
            "name": "Source on github.com",
        },
        {
            "icon": "fontawesome/brands/python",
            "link": "https://pypi.org/project/whispertrades/",
        },
    ],
    # END: social icons
}


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_immaterial'
html_static_path = ['_static']
