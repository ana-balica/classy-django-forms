import collections
import sys
import typing

import django
from django.conf import settings

settings.configure(
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        }
    },
)

# Monkey patching needed for newer Python versions and older Django ones:
if not hasattr(collections, "Mapping"):
    collections.Mapping = typing.Mapping
if not hasattr(collections, "Iterator"):
    collections.Iterator = typing.Iterator
if not hasattr(collections, "Sequence"):
    collections.Sequence = typing.Sequence
sys.modules["collections"] = collections

django.setup()
