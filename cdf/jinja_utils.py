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


@contextfunction
def get_version_url(context, version):
    if 'this_klass' in context:
        return get_klass_url(context, context['this_klass'], version)
    return os.path.join('/', version, 'index.html')


@contextfunction
def get_klass_docs(context, klass):
    if klass.__doc__ and klass.__doc__.strip():
        return klass.__doc__.strip()
    return ''


template_env.globals['get_klass_url'] = get_klass_url
template_env.globals['get_version_url'] = get_version_url
template_env.globals['get_klass_docs'] = get_klass_docs
