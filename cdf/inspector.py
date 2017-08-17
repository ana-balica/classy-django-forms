from django import forms


def get_klasses():
    """
    Get all the public classes from the Django modules of interest within forms.
    """
    # TODO: update the list of modules
    modules = [forms.fields, forms.widgets]
    klasses = []

    for module in modules:
        for klass_name in module.__all__:
            klass = getattr(module, klass_name)
            klasses.append(klass)
    return klasses
