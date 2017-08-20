from django import forms


def get_klasses():
    """
    Get all the public classes from the Django modules of interest within forms.

    :returns: dict of the form {'module_name': ['classA', 'classB', 'classC']}
    """
    # TODO: update the list of modules
    modules = [forms.fields, forms.widgets]
    klasses = {}

    for module in modules:
        module_name = module.__name__
        klasses[module_name] = []
        for klass_name in module.__all__:
            klasses[module_name].append(klass_name)
    return klasses
