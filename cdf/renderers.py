from cdf.config import DJANGO_VERSIONS, VERSION
from cdf.jinja_utils import template_env


class BasicPageRenderer(object):

    def __init__(self, klasses):
        self.klasses = klasses

    def render(self, template_name, filename):
        template = template_env.get_template(template_name)
        context = self.get_context()
        rendered_template = template.render(context)
        with open(filename, 'w') as f:
            f.write(rendered_template)

    def get_context(self):
        other_versions = list(DJANGO_VERSIONS)
        other_versions.remove(VERSION)
        return {
            'version_prefix': 'Django',
            'version': VERSION,
            'versions': DJANGO_VERSIONS,
            'other_versions': other_versions,
            'klasses': self.klasses
        }


