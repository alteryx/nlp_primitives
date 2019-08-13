from setuptools import find_packages, setup

setup(
    name='nlp_primitives',
    version='v0.0.0',
    author='Feature Labs, Inc.',
    author_email='support@featurelabs.com',
    license='BSD 3-clause',
    url='http://www.featurelabs.com/',
    install_requires=open('requirements.txt').readlines(),
    tests_require=open('test-requirements.txt').readlines(),
    packages=find_packages(),
    package_data = {'nlp_primitives': ['data/nltk-data.tar.gz']},
    include_package_data=True,
    zip_safe=False,
)
