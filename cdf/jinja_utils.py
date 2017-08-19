from jinja2 import (
    select_autoescape,
    Environment,
    FileSystemLoader,
)


template_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(['html', 'xml'])
)
