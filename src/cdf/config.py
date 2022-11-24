from django import VERSION as django_version

from cdf.utils import get_major_dot_minor_version


DJANGO_VERSIONS = [
    '4.1',
    '4.0',
    '3.2',
    '3.1',
    '3.0',
    '2.2',
    '2.1',
    '2.0',
]


VERSION = get_major_dot_minor_version(django_version)
BASE_URL = '/'
