import inspect
import json
import types
from collections import namedtuple

from django import forms
from pygments import highlight
from pygments.lexers import PythonLexer

from cdf.custom_formatter import CodeHtmlFormatter


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


Attribute = namedtuple('Attribute', ['name', 'value', 'classobject', 'instance_class'])


class Method:

    def __init__(self, name, value, classobject, instance_class):
        self.name = name
        self.value = value
        self.classobject = classobject
        self.instance_class = instance_class
        self.children = []

    def params(self):
        stack = []
        argspec = inspect.getargspec(self.value)
        if argspec.keywords:
            stack.insert(0, '**' + argspec.keywords)
        if argspec.varargs:
            stack.insert(0, '*' + argspec.varargs)
        defaults = list(argspec.defaults or [])
        for arg in argspec.args[::-1]:
            if defaults:
                default = defaults.pop()
                stack.insert(0, '{}={}'.format(arg, default))
            else:
                stack.insert(0, arg)
        return ', '.join(stack)

    def code(self):
        code = inspect.getsource(self.value)
        return highlight(code, PythonLexer(), CodeHtmlFormatter(self.instance_class))


class Property:

    def __init__(self, name, value, classobject, instance_class):
        self.name = name
        self.value = value
        self.classobject = classobject
        self.instance_class = instance_class
        self.children = []

    @property
    def getter(self):
        return self.code('fget')

    @property
    def setter(self):
        return self.code('fset')

    @property
    def deleter(self):
        return self.code('fdel')

    @property
    def accessors(self):
        return {
            'getter': self.getter,
            'setter': self.setter,
            'deleter': self.deleter,
        }

    def code(self, func_name):
        func = getattr(self.value, func_name)
        if func is None:
            return ''

        code = inspect.getsource(func)
        return highlight(code, PythonLexer(), CodeHtmlFormatter(self.instance_class))


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

    def get_attributes(self):
        """
        Get all class attributes (including the ones from the base classes),
        excluding the dunder attributes, methods and properties.
        """
        attrs = []

        for klass in self.get_ancestors():
            for attr_str in klass.__dict__.keys():
                if not attr_str.startswith('__'):
                    attr_value = getattr(klass, attr_str)
                    # Filter out class methods and properties
                    if not callable(attr_value) and not isinstance(attr_value, property):
                        attr = Attribute(
                            name=attr_str,
                            value=repr(attr_value),  # Sort out the lazy attributes
                            classobject=klass,
                            instance_class=self.klass
                        )
                        attrs.append(attr)
        attrs.sort(key=lambda x: x.name)
        return attrs

    def get_properties(self):
        properties = []

        for klass in self.get_ancestors():
            for attr_str in klass.__dict__.keys():
                if not attr_str.startswith('__'):
                    attr_value = getattr(klass, attr_str)
                    if isinstance(attr_value, property):
                        method = Property(
                            name=attr_str,
                            value=attr_value,
                            classobject=klass,
                            instance_class=self.klass
                        )
                        properties.append(method)
        properties.sort(key=lambda x : x.name)
        return properties

    def get_methods(self):
        """
        Get all class methods.
        """
        methods = []

        for klass in self.get_ancestors():
            for attr_str in klass.__dict__.keys():
                if not attr_str.startswith('__'):
                    attr_value = getattr(klass, attr_str)
                    if isinstance(attr_value, types.FunctionType):
                        method = Method(
                            name=attr_str,
                            value=attr_value,
                            classobject=klass,
                            instance_class=self.klass
                        )
                        methods.append(method)
        methods.sort(key=lambda x : x.name)
        return methods

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
