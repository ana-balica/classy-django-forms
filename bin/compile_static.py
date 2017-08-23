#!/usr/bin/env python
import os

from cdf.config import DJANGO_VERSIONS, VERSION
from cdf.inspector import get_klasses
from cdf.renderers import (
    BasicPageRenderer,
)


def main():
    klasses_by_module = get_klasses()

    out_folder = 'public'
    for module, klasses in klasses_by_module.items():
        target_path = os.path.join(out_folder, VERSION, module.__name__)
        os.makedirs(target_path, exist_ok=True)

    renderer = IndexPageRenderer(klasses)
    index_path = os.path.join(out_folder, VERSION, 'index.html')
    renderer.render(index_path)

    renderer = BasicPageRenderer(klasses_by_module)
    index_version_path = os.path.join(out_folder, VERSION, 'index.html')
    renderer.render('index.html', index_version_path)

    if VERSION == DJANGO_VERSIONS[-1]:
        index_path = os.path.join(out_folder, 'index.html')
        renderer.render('index.html', index_path)
        not_found_path = os.path.join(out_folder, '404.html')
        renderer.render('404.html', not_found_path)

if __name__ == '__main__':
    main()
