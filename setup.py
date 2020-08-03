from os import path

from setuptools import find_packages, setup

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

extras_require = {
    'complete': ['tensorflow>=1.14.0', 'tensorflow_hub>=0.4.0']
}

setup(
    name='nlp_primitives',
    version='0.3.1',
    author='Feature Labs, Inc.',
    author_email='support@featurelabs.com',
    license='BSD 3-clause',
    url='http://www.featurelabs.com/',
    install_requires=open('requirements.txt').readlines(),
    tests_require=open('test-requirements.txt').readlines(),
    packages=find_packages(),
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
