#!/usr/bin/env python
""" Test notebook conversion via script """
from __future__ import print_function

import sys
from os.path import join as pjoin, split as psplit, abspath, dirname

from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter
from nbviewer.render import render_notebook
from nbviewer.utils import ipython_info
from jinja2 import Environment, FileSystemLoader
import markdown

# Jinja2 config
here = dirname(__file__)
template_path = pjoin(here, 'templates')
j2_env = Environment(loader=FileSystemLoader(template_path))
j2_env.filters['markdown'] = markdown.markdown
git_data = {}
def nrhead():
    return ''
def nrfoot():
    return ''
j2_env.globals.update(nrhead=nrhead, nrfoot=nrfoot, git_data=git_data,
                      ipython_info=ipython_info()
                     )


def export_notebook(nbjson):
    # NBConvert config
    config = Config()
    config.HTMLExporter.template_file = 'basic'
    config.NbconvertApp.fileext = 'html'
    config.CSSHTMLHeaderTransformer.enabled = False

    exporter = HTMLExporter(config=config)

    download_url = None
    home_url = None

    nbhtml, nbconfig = render_notebook(exporter, nbjson)

    from datetime import datetime
    date_fmt = "%a, %d %h %Y %H:%M:%S UTC"

    nbconfig.update(body=nbhtml, download_url=download_url, home_url=home_url,
                    date=datetime.utcnow().strftime(date_fmt))
    template = j2_env.get_template('notebook.html')
    return template.render(nbconfig)


def main():
    fname = sys.argv[1]
    with open(fname, 'rt') as fobj:
        nbjson = fobj.read()
    print(export_notebook(nbjson))


if __name__ == '__main__':
    main()
