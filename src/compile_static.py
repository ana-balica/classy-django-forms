#!/usr/bin/env python
import os

from cdf.config import DJANGO_VERSIONS, VERSION
from cdf.inspector import get_klasses
from cdf.renderers import (
    BasicPageRenderer,
    DetailsPageRenderer,
    SitemapRenderer,
)


def main():
    klasses_by_module = get_klasses()

    out_folder = 'public'
    for module, klasses in klasses_by_module.items():
        target_path = os.path.join(out_folder, VERSION, module.__name__)
        os.makedirs(target_path, exist_ok=True)

        for klass in klasses:
            renderer = DetailsPageRenderer(klasses_by_module, klass)
            details_path = os.path.join(out_folder, VERSION, module.__name__, klass.__name__ + '.html')
            renderer.render('details.html', details_path)

    renderer = BasicPageRenderer(klasses_by_module)
    index_version_path = os.path.join(out_folder, VERSION, 'index.html')
    renderer.render('index.html', index_version_path)

    # Render one version of homepage, 404 and sitemap pages
    if VERSION == DJANGO_VERSIONS[0]:
        index_path = os.path.join(out_folder, 'index.html')
        renderer.render('home.html', index_path)
        not_found_path = os.path.join(out_folder, '404.html')
        renderer.render('404.html', not_found_path)

        renderer = SitemapRenderer(klasses)
        sitemap_path = os.path.join(out_folder, 'sitemap.xml')
        renderer.render('sitemap.xml', sitemap_path)


if __name__ == '__main__':
    main()
