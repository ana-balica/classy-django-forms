import os

from jinja2 import (
    contextfunction,
    select_autoescape,
    Environment,
    FileSystemLoader,
)

from cdf.config import VERSION, EXACT_VERSION


template_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(['html', 'xml'])
)


@contextfunction
def get_klass_url(context, klass, version=VERSION):
    return os.path.join('/', version, klass.__module__, klass.__name__ + '.html')


template_env.globals['get_klass_url'] = get_klass_url
