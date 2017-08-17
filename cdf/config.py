from django import VERSION as django_version


DJANGO_VERSIONS = [
    '1.8',
    '1.9',
    '1.10',
    '1.11',
]


VERSION = get_major_dot_minor_version(django_version)
EXACT_VERSION = django_version


def get_major_dot_minor_version(version):
    """
    Convert full VERSION Django tuple to
    a dotted string containing MAJOR.MINOR.

    For example, (1, 9, 3, 'final', 0) will result in '1.9'
    """
    return '.'.join(version.split('.')[:2])
