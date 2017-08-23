import types
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

    def get_ancestors(self):
        """
        Return a list of class ancestors using the method resolution order.
        """
        ancestors = []
        for ancestor in type.mro(self.klass):
            if ancestor is not object:
                ancestors.append(ancestor)
        return ancestors

    def get_direct_ancestors(self):
        return self.klass.__bases__

    def get_descendants(self):
        """
        Get the list of classes that inherit from the target class.
        """
        descendants = []
        klasses_by_module = get_klasses()
        for module, klasses in klasses_by_module.items():
            for klass in klasses:
                if klass != self.klass and issubclass(klass, self.klass):
                    descendants.append(klass)
        return descendants

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
