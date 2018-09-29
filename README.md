# Classy Django Forms

Classy Django Forms is an API inspector of classes available in Django forms module. It exposes all public classes with their attributes, properties, methods and the dependencies to other classes. This project is heavily based on [Classy Class-Based Views](http://ccbv.co.uk) and [Classy Django Rest Framework](http://www.cdrf.co).

## Development

Requires Python 3.

`$ pip install -r requirements.txt`

`$ make build`

To run locally:

`$ make runserver`

## How it works

This project generates a static website (see `public` folder). This is achieved using 2 scripts:

* `bin/generate_index.py` - pulls all the public classses from Django forms module and saved them as a JSON file (see `klasses.json`)
* `bin/compile_static.py` - gets the data from the JSON file and renders pages with all the class info

These 2 scripts are called for each tox environment. Tox is used to create multiple virtual environments each with a different version of Django.

**Tip:** during development if you don't want to build the static files for all versions of Django, you can run `tox -e dj19` to generate the index and `tox -e djbuild19` to compile static files only for Django 1.9.

## How to add a new Django version

1. Update `cdf/config.py` and `tox.ini` like [this](https://github.com/ana-balica/classy-django-forms/commit/45ef9b8cbdc52a5608f16f527c6f93bb716942db).
2. Activate virtualenv and run `make build_local`.
3. You should see a new folder in `public/` and a new key in `.klasses.json` with the added Django version.

## How to deploy

The website is hosted by GitHub Pages on a custom domain [https://cdf.9vo.lt](https://cdf.9vo.lt).

To deploy a new version, do the following:

1. Merge latest master to gh-pages branch `git checkout gh-pages && git merge master`.
2. Build public folder `make build`.
3. Commit newly generated files `git add public/ && git commit`.
4. Run `git subtree push --prefix public/ origin gh-pages`. This will push only the public folder to gh-pages.
5. Check [https://cdf.9vo.lt/](https://cdf.9vo.lt/).
