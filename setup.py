# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from distutils.core import Command


class Test(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from django.conf import settings
        settings.configure(
            INSTALLED_APPS=('collectionfield.tests',),
            SECRET_KEY='AAA',
            DATABASES={
                'default': {
                    'NAME': ':memory:',
                    'ENGINE': 'django.db.backends.sqlite3'
                }
            },
            MIDDLEWARE_CLASSES = ()
        )
        from django.core.management import call_command
        import django
        django.setup()
        call_command('test', 'collectionfield')


setup(
    name='django-collectionfield',
    version='0.0.1',
    description='Custom Django model field to store multiple values.',
    author='Pawel Scierski',
    author_email='escer@protonmail.com',
    url='https://github.com/escer/django-collectionfield',
    packages=find_packages(),
    cmdclass={'test': Test},
)
