from django import forms


def get_klasses():
    """
    Get all the public classes from the Django modules of interest within forms.

    :returns: dict of the form {module: [classA, classB, classC]}
    """
    # TODO: update the list of modules
    modules = [forms.fields, forms.widgets]
    klasses = {}

    for module in modules:
        klasses[module] = []
        for klass_name in module.__all__:
            klass = getattr(module, klass_name)
            klasses[module].append(klass)
    return klasses
