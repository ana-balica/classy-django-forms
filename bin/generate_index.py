#!/usr/bin/env python
import os
import json

from cdf.config import VERSION
from cdf.inspector import get_klasses


def main():
    klasses = get_klasses()

    # Load existing Django forms spec
    forms_api_spec = {}
    if os.path.isfile('.klasses.json'):
        with open('.klasses.json', 'r') as f:
            forms_api_spec = json.loads(f.read())

    # Update the spec and write back
    forms_api_spec[VERSION] = klasses
    with open('.klasses.json', 'w') as f:
        json.dump(forms_api_spec, f, indent=2)


if __name__ == '__main__':
    main()
