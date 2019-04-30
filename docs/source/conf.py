import os
import sys

sys.path.insert(0, os.path.abspath('../..'))
extensions = ['sphinx.ext.autodoc']

project = 'npyi'
copyright = '2019, Andy Huynh'
author = 'Andy Huynh'
version = '1'
release = '0.1'
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
pygments_style = 'sphinx'
html_theme = 'alabaster'
html_static_path = ['_static']
