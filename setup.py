import os

from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drftest',
    version='1.0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='drftest is a minimal testing library that aims to facilitate writing tests for '
                'django rest framework views. It also [optionally] generates good looking API '
                'documentations based on tests it runs.',
    install_requires=[
        'django>=1.11.0',
        'djangorestframework',
        'django_nose',
    ],
    long_description=README,
    url='https://github.com/pdrum/drftest',
    author='Pedram Hajesmaeeli',
    author_email='pedram.esmaeeli@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
