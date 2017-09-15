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

* `bin/generate_index.py` - pulls all the public classses from Django forms module and saved them as a JSON to a file (see `klasses.json`)
* `bin/compile_static.py` - gets the data from the JSON file and renders pages with all the class info

These 2 scripts are called for each tox environment. Tox is used to create multiple virtual environments each with a different version of Django.

**Tip:** during development if you don't want to build the static files for all versions of Django, you can run `tox -e dj19` to generate the index and `tox -e djbuild19` to compile static files only for Django 1.9.
