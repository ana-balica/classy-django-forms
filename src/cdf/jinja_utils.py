import inspect
import os

from jinja2 import (
    pass_context,
    select_autoescape,
    Environment,
    FileSystemLoader,
)

from cdf.config import VERSION, BASE_URL
from cdf.utils import get_module_short_name


template_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(['html', 'xml'])
)


@pass_context
def get_klass_url(context, klass, version=VERSION):
    return os.path.join(BASE_URL, version, klass.__module__, klass.__name__ + '.html')


@pass_context
def get_version_url(context, version):
    if 'this_klass' in context:
        return get_klass_url(context, context['this_klass'], version)
    return os.path.join(BASE_URL, version, 'index.html')


@pass_context
def get_klass_docs(context, klass):
    if klass.__doc__ and klass.__doc__.strip():
        return klass.__doc__.strip()
    return ''


@pass_context
def get_doc_link(context, klass, version=VERSION):
    base_url = 'https://docs.djangoproject.com/en/{version}/ref/forms/{module}/#{klass}'
    return base_url.format(
        version=version,
        module=get_module_short_name(klass),
        klass=klass.__name__.lower()
    )


@pass_context
def get_src_link(context, klass, version=VERSION):
    src_url = "https://github.com/django/django/blob/stable/{version}.x/django/forms/{module}.py#L{lineno}"
    local_path = inspect.getsourcefile(klass)
    lineno = inspect.getsourcelines(klass)[-1]
    return src_url.format(
        version=version,
        module=get_module_short_name(klass),
        lineno=lineno
    )


template_env.globals['get_klass_url'] = get_klass_url
template_env.globals['get_version_url'] = get_version_url
template_env.globals['get_klass_docs'] = get_klass_docs
template_env.globals['get_doc_link'] = get_doc_link
template_env.globals['get_src_link'] = get_src_link
