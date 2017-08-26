def get_major_dot_minor_version(version):
    """
    Convert full VERSION Django tuple to
    a dotted string containing MAJOR.MINOR.

    For example, (1, 9, 3, 'final', 0) will result in '1.9'
    """
    return '.'.join([str(v) for v in version[:2]])


def get_module_short_name(klass):
    """
    Return the short module name.

    For example, full module name is `django.forms.fields` and
    the short module name will be `fields`.
    """
    return klass.__module__.rsplit('.', 1)[-1]
