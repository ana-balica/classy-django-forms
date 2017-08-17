#!/usr/bin/env python
import os
import json

from itertools import groupby

from cdf.config import VERSION
from cdf.inspector import get_klasses


def sort_by_module(klasses):
    return sorted(klasses, key=lambda klass: klass.__module__)


def group_by_module(klasses):
    klasses_by_module = {}
    for key, value in groupby(klasses, lambda klass:  klass.__module__):
        klasses_by_module[key] = list(map(lambda x: x.__name__, list(value)))

    return klasses_by_module


def main():
    all_klasses = get_klasses()
    klasses = sort_by_module(all_klasses)
    klasses_by_module = group_by_module(klasses)

    # Load existing Django forms spec
    forms_api_spec = {}
    if os.path.isfile('.klasses.json'):
        with open('.klasses.json', 'r') as f:
            forms_api_spec = json.loads(f.read())

    # Update the spec and write back
    forms_api_spec[VERSION] = klasses_by_module
    with open('.klasses.json', 'w') as f:
        json.dump(forms_api_spec, f, indent=2)


if __name__ == '__main__':
    main()
