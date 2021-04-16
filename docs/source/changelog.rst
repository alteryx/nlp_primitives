=========
Changelog
=========
**Future Release** TBD
    * Enhancements
    * Fixes
    * Changes
    * Documentation Changes
        * Update UniversalSentenceEncoder docstring example (:pr:`42`)
    * Testing Changes

    Thanks to the following people for contributing to this release:
    :user:`rwedge`

**v1.1.0** Oct 26, 2020
    * Changes
        * Upgrade to Featuretools 0.20.0 and replace Text variable type with NaturalLanguage (:pr:`34`)
        * Include corpus download with package instead of downloading at first run. (:pr:`31`)
        * Change corpus used by LSA primitive (:pr:`35`)
        * Refactor ``clean_tokens`` function (:pr:`29`)
    * Testing Changes
        * Add another set of CI jobs which ensure that we can make an nlp_primitives package, install that, and then still pass all the unit tests, vs an editable install :pr:`31`
        * Move some test utils into `test/` :pr:`31`

    Thanks to the following people for contributing to this release:
    :user:`dsherry`, :user:`eccabay`, :user:`gsheni`, :user:`rwedge`

**v1.0.0** Aug 12, 2020
    * Changes
        * Remove tensorflow and tensorhub as core requirements, but they
        can be installed with ``pip install nlp_primitives[complete]``. The
        ``UniversalSentenceEncoder`` primitive requires the ``nlp_primitives[complete]``
        install but all other primitives work with the standard install. (:pr:`24`)
    * Testing Changes
        * Update CircleCI to perform complete install and use matrix jobs (:pr:`24`)

    Thanks to the following people for contributing to this release:
    :user:`thehomebrewnerd`

**v0.3.1**
    * Fix installation error related to scipy version

**v0.3.0**
    * Fixed case-insensitivity in the Stopword Count Primitive
    * Made compatible with Tensorflow 2
    * Dropped Python 3.5 and added Python 3.8

**v0.2.5**
    * Removed python-dateutil as a requirement

**v0.2.4**
    * Added Featuretools Entry Point
    * PyPI Upload

**v0.2.3**
    * Small bug fixes

**v0.2.2**
    * Now comes with description for PyPI

**v0.1.0**
    * Fixed reliance on external data files

**v0.0.0**
    * Initial Release
