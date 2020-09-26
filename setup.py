from os import path

from setuptools import find_packages, setup
from setuptools.command.sdist import sdist

import pathlib
import pkg_resources
import tarfile

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

extras_require = {
    'complete': open('complete-requirements.txt').readlines()
}

class PreSDistNLTKDataUnpackCommand(sdist):
    """Before creating source distribution, untar nltk data files, so they'll be included via the manifest file.

    Note the usage of `pkg_resources.resource_filename` for pathing assumes you're building the source distribution with your cwd
    in the repo.
    """
    def run(self):
        nltk_data_tarball_path = pkg_resources.resource_filename('nlp_primitives', str(pathlib.Path('data','nltk-data.tar.gz')))
        nltk_data_extract_path = pkg_resources.resource_filename('nlp_primitives', str(pathlib.Path('data')))
        print(f'Extracting nltk data files from {nltk_data_tarball_path} to {nltk_data_extract_path}')
        print(pkg_resources.resource_listdir('nlp_primitives', str(pathlib.Path('data'))))
        tar = tarfile.open(nltk_data_tarball_path, "r:gz")
        tar.extractall(path=nltk_data_extract_path)
        tar.close()
        print(f'Extraction of nltk data files complete')
        sdist.run(self)

setup(
    name='nlp_primitives',
    version='1.0.0',
    author='Feature Labs, Inc.',
    author_email='support@featurelabs.com',
    license='BSD 3-clause',
    url='http://www.featurelabs.com/',
    install_requires=open('requirements.txt').readlines(),
    packages=find_packages(),
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
    cmdclass={
        'sdist': PreSDistNLTKDataUnpackCommand
    }
)
