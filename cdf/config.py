from django import VERSION as django_version

from cdf.utils import get_major_dot_minor_version


DJANGO_VERSIONS = [
    '1.8',
    '1.9',
    '1.10',
    '1.11',
]


VERSION = get_major_dot_minor_version(django_version)
BASE_URL = 'http://someurl.com'
