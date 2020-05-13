from django import VERSION as django_version

from cdf.utils import get_major_dot_minor_version


DJANGO_VERSIONS = [
    '3.0',
    '2.2',
    '2.1',
    '2.0',
    '1.11',
    '1.10',
    '1.9',
    '1.8',
]


VERSION = get_major_dot_minor_version(django_version)
BASE_URL = 'https://cdf.9vo.lt/'
