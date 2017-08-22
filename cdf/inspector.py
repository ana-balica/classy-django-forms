import json

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


class Inspector:

    def __init__(self, klass):
        self.klass = klass
        self.klass_name = klass.__name__
        self.module_name = klass.__module__

    def get_available_versions(self):
        """
        Return a list of versions in which the class is present.
        """
        with open('.klasses.json', 'r') as f:
            klass_versions = json.loads(f.read())

        return [
            version
            for version in klass_versions
            if self.module_name in klass_versions[version] and
            self.klass_name in klass_versions[version][self.module_name]
        ]
