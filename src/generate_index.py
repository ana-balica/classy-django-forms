#!/usr/bin/env python
import os
import json

from cdf.config import VERSION
from cdf.inspector import get_klasses


def stringify_klasses_data(klasses_by_module):
    """
    Convert all the objects (modules and klasses) to their string names.
    """
    klasses_data = {}
    for module, klasses in klasses_by_module.items():
        module_name = module.__name__
        klasses_data[module_name] = []
        for klass in klasses:
            klasses_data[module_name].append(klass.__name__)
    return klasses_data


def main():
    klasses_by_module = get_klasses()

    # Load existing Django forms spec
    forms_api_spec = {}
    if os.path.isfile('.klasses.json'):
        with open('.klasses.json', 'r') as f:
            forms_api_spec = json.loads(f.read())

    # Update the spec and write back
    forms_api_spec[VERSION] = stringify_klasses_data(klasses_by_module)
    with open('.klasses.json', 'w') as f:
        json.dump(forms_api_spec, f, indent=2)


if __name__ == '__main__':
    main()
