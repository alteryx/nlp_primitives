import os
from os import path
import shutil
import tempfile

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

extras_require = {
    'complete': open('complete-requirements.txt').readlines()
}

setup(
    name='nlp_primitives',
    version='1.0.0',
    author='Feature Labs, Inc.',
    author_email='support@featurelabs.com',
    license='BSD 3-clause',
    url='http://www.featurelabs.com/',
    install_requires=open('requirements.txt').readlines(),
    package_data = {'nlp_primitives': ['data/nltk-data.tar.gz']},
    include_package_data=True,
    zip_safe=False,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    extras_require=extras_require,
    entry_points={
        'featuretools_plugin': [
            'nlp_primitives = nlp_primitives',
        ],
    },
)


fp = os.path.normpath(os.path.join(os.path.realpath(__file__), '../data/nltk-data.tar.gz'))
dp = os.path.normpath(os.path.join(fp, '../nltk-data'))
try:
    tf = tempfile.mkdtemp()
    shutil.unpack_archive(fp, tf)
    if os.path.exists(dp):
        shutil.rmtree(dp)
    shutil.copytree(tf, dp)
    print('Unloaded nltk data to', dp)
finally:
    shutil.rmtree(tf)
