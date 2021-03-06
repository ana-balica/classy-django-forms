import json

from cdf.config import BASE_URL, DJANGO_VERSIONS, VERSION
from cdf.inspector import Inspector
from cdf.jinja_utils import template_env


class BasicPageRenderer:

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
            'klasses': self.klasses,
            'base_url': BASE_URL,
        }


class DetailsPageRenderer(BasicPageRenderer):

    def __init__(self, klasses, klass):
        super(DetailsPageRenderer, self).__init__(klasses)
        self.klass = klass
        self.inspector = Inspector(klass)

    def get_context(self):
        context = super(DetailsPageRenderer, self).get_context()
        available_versions = self.inspector.get_available_versions()

        context['other_versions'] = [
            version
            for version in context['other_versions']
            if version in available_versions
        ]
        context['this_klass'] = self.klass
        context['this_klass_name'] = self.klass.__name__
        context['ancestors'] = self.inspector.get_ancestors()
        context['direct_ancestors'] = self.inspector.get_direct_ancestors()
        context['descendants'] = self.inspector.get_descendants()
        context['attributes'] = self.inspector.get_attributes()
        properties = self.inspector.get_properties()
        context['properties'] = properties
        context['methods'] = self.inspector.get_methods(properties)
        return context


class SitemapRenderer(BasicPageRenderer):

    def get_context(self):
        context = {}
        with open('.klasses.json', 'r') as f:
            klasses = json.loads(f.read())

        context['klasses'] = klasses
        context['latest_version'] = DJANGO_VERSIONS[-1]
        context['base_url'] = BASE_URL
        return context
