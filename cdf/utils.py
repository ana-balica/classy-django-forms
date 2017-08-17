def get_major_dot_minor_version(version):
    """
    Convert full VERSION Django tuple to
    a dotted string containing MAJOR.MINOR.

    For example, (1, 9, 3, 'final', 0) will result in '1.9'
    """
    return '.'.join(version.split('.')[:2])
