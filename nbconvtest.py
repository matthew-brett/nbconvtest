#!/usr/bin/env python
""" Test notebook conversion via script """
from __future__ import print_function

import sys
from os.path import join as pjoin, split as psplit, abspath, dirname

from IPython.config import Config
from IPython.nbconvert.exporters import HTMLExporter
from IPython.nbformat.current import reads_json
from jinja2 import Environment, FileSystemLoader

# Jinja2 config
here = dirname(__file__)
template_path = pjoin(here, 'templates')
j2_env = Environment(loader=FileSystemLoader(template_path))
j2_env.globals.update(
                     )

def render_notebook(exporter, json_notebook):
    nb = reads_json(json_notebook)
    return exporter.from_notebook_node(nb)

def export_notebook(nbjson, **kwargs):
    # NBConvert config
    config = Config()
    config.HTMLExporter.template_file = 'basic'
    config.NbconvertApp.fileext = 'html'
    config.CSSHTMLHeaderTransformer.enabled = False

    exporter = HTMLExporter(config=config)

    download_url = None
    home_url = None

    nbhtml, resources = render_notebook(exporter, nbjson)

    from datetime import datetime
    date_fmt = "%a, %d %h %Y %H:%M:%S UTC"
    download_urls = [
        ""
    ]
    resources.update(nbhtml=nbhtml, 
                    date=datetime.utcnow().strftime(date_fmt),
                    **kwargs
                    )
    template = j2_env.get_template('static_notebook.html')
    return template.render(resources)


def main():
    fname = sys.argv[1]
    with open(fname, 'rt') as fobj:
        nbjson = fobj.read()

    home_icon = "home"
    home_text = "Home"
    home_url = "../"

    static = lambda path: "static/%s" % path
    css_urls = [ static(f) for f in [
        "css/font-awesome.min.css",
        "css/bootstrap.min.css",
        "css/bootstrap-responsive.min.css",
        "css/pygments.css",
        "css/ipython.min.css",
        "css/nbviewer.css",
    ]]
    js_urls = [ static(f) for f in [
        "js/jquery.min.js",
        "js/bootstrap.min.js",
        "js/bootstrap-collapse.js",
        "js/require.js",
    ]]
    js_urls.append("https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS_HTML")
    downloads = {"Notebook File" : fname, "Notebook File (Again)" : fname}

    print(export_notebook(nbjson,
        css_urls=css_urls,
        js_urls=js_urls,
        home_icon=home_icon,
        home_text=home_text,
        home_url=home_url,
        downloads=downloads,
    ))


if __name__ == '__main__':
    main()
