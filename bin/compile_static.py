#!/usr/bin/env python
import os

from cdf.config import DJANGO_VERSIONS, VERSION
from cdf.inspector import get_klasses
from cdf.renderers import (
    IndexPageRenderer,
)


def main():
    klasses = get_klasses()

    out_folder = 'public'
    for module, _ in klasses.items():
        target_path = os.path.join(out_folder, VERSION, module)
        os.makedirs(target_path, exist_ok=True)

    renderer = IndexPageRenderer(klasses)
    index_path = os.path.join(out_folder, VERSION, 'index.html')
    renderer.render(index_path)


if __name__ == '__main__':
    main()
