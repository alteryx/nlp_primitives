from os import path

from setuptools import find_packages, setup

import pathlib
import pkg_resources
import tarfile

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

extras_require = {
    'complete': open('complete-requirements.txt').readlines()
}

setup(
    name='nlp_primitives',
    version='2.0.0',
    author='Feature Labs, Inc.',
    author_email='support@featurelabs.com',
    classifiers=[
         'Development Status :: 3 - Alpha',
         'Intended Audience :: Developers',
         'Programming Language :: Python :: 3',
         'Programming Language :: Python :: 3.7',
         'Programming Language :: Python :: 3.8'
    ],
    license='BSD 3-clause',
    url='http://www.featurelabs.com/',
    install_requires=open('requirements.txt').readlines(),
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7, <4',
    extras_require=extras_require,
    entry_points={
        'featuretools_plugin': [
            'nlp_primitives = nlp_primitives',
        ],
    },
)
