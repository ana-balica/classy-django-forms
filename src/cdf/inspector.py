import inspect
import json
import types
from collections import namedtuple
from typing import MutableSequence

from django import forms
from pygments import highlight
from pygments.lexers import PythonLexer

from cdf.custom_formatter import CodeHtmlFormatter


def get_klasses():
    """
    Get all the public classes from the Django modules of interest within forms.

    :returns: dict of the form {module: [classA, classB, classC]}
    """
    module_names = [
        'boundfield',
        'fields',
        'forms',
        'formsets',
        'models',
        'widgets',
    ]
    klasses = {}

    for module_name in module_names:
        module = getattr(forms, module_name, None)
        if module:
            klasses[module] = []
            for klass_name in module.__all__:
                klass = getattr(module, klass_name)
                if inspect.isclass(klass):
                    klasses[module].append(klass)
            klasses[module].sort(key=lambda x: x.__name__)
    return klasses


Attribute = namedtuple('Attribute', ['name', 'value', 'classobject', 'instance_class', 'overridden'])


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
    def getter_code(self):
        return self.code('fget')

    @property
    def setter_code(self):
        return self.code('fset')

    @property
    def deleter_code(self):
        return self.code('fdel')

    @property
    def accessors_code(self):
        return {
            'getter': self.getter_code,
            'setter': self.setter_code,
            'deleter': self.deleter_code,
        }

    @property
    def accessors(self):
        funcs = [
            getattr(self.value, 'fget'),
            getattr(self.value, 'fset'),
            getattr(self.value, 'fdel'),
        ]
        return [f for f in funcs if f is not None]

    def code(self, func_name):
        func = getattr(self.value, func_name)
        if func is None:
            return ''

        code = inspect.getsource(func)
        return highlight(code, PythonLexer(), CodeHtmlFormatter(self.instance_class))


class KlassItems(MutableSequence):

    def __init__(self):
        self.items = []

    def __getitem__(self, index):
        return self.items[index]

    def __setitem__(self, index, value):
        if index < len(self.items) or not isinstance(index, int):
            raise ValueError("Can't change value of position")

        try:
            existing_item = next(x for x in self.items if x.name == value.name)
            existing_item.children.append(value)
        except StopIteration:
            self.items.append(value)

    def __delitem__(self, index):
        del self.items[index]

    def __len__(self):
        return len(self.items)

    def insert(self, index, value):
        self.__setitem__(index, value)

    def sort(self, *args, **kwargs):
        self.items.sort(*args, **kwargs)


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
        attrs_names = []

        for klass in self.get_ancestors():
            for attr_name in klass.__dict__.keys():
                if not attr_name.startswith('__'):
                    attr_value = getattr(klass, attr_name)
                    # Filter out class methods and properties
                    if not callable(attr_value) and not isinstance(attr_value, property):
                        # Overridden attributes come later due to mro order
                        overridden = True if attr_name in attrs_names else False
                        attr = Attribute(
                            name=attr_name,
                            value=repr(attr_value),  # Sort out the lazy attributes
                            classobject=klass,
                            instance_class=self.klass,
                            overridden=overridden,
                        )
                        attrs.append(attr)
                        attrs_names.append(attr_name)
        attrs.sort(key=lambda x: x.name)
        return attrs

    def get_properties(self):
        """
        Get a list of class properties.
        """
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

    def _get_properties_accessors(self, properties):
        """
        Put all properties accessors (getter / setter / deleter)
        in a single list.
        """
        properties_accessors = []
        for p in properties:
            properties_accessors.extend(p.accessors)
        return properties_accessors

    def get_methods(self, properties=None):
        """
        Get all class methods, exclude getter / setter / deleter methods
        of any class properties.
        """
        methods = KlassItems()
        properties_accessors = self._get_properties_accessors(properties or [])

        for klass in self.get_ancestors():
            for method_name in klass.__dict__.keys():
                if not method_name.startswith('__'):
                    method_value = getattr(klass, method_name)
                    if isinstance(method_value, types.FunctionType) and method_value not in properties_accessors:
                        method = Method(
                            name=method_name,
                            value=method_value,
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
