=========
Changelog
=========

Future Release
==============
    * Enhancements
        * Added Release Notes CI Check (:pr:`110`)
    * Fixes
        * Fixed scheduler workflow to test latest changes in featuretools (:pr:`112`)
    * Changes
        * Added CI check to ensure entrypoint works with Featuretools (:pr:`111`)
    * Documentation Changes
    * Testing Changes

    Thanks to the following people for contributing to this release:
    :user:`dvreed77`, :user:`jeff-hernandez`

v2.3.0 Feb 28, 2022
===================
    * Changes
        * Tensorflow dependent primitives only imported at top level if tensorflow is installed (:pr:`105`)
    * Testing Changes
        * Skip Tensorflow dependent tests if --notensorflow flag is passed to pytest (:pr:`107`)

    Thanks to the following people for contributing to this release:
    :user:`dvreed77`, :user:`rwedge`

v2.2.0 Feb 17, 2022
===================
    * Enhancements
        * Add NumberOfUniqueSeparators primitive (:pr:`90`)
        * Add NumberOfCommonWords primitive (:pr:`92`)
        * Add CountString and WhitespaceCount primitives (:pr:`89`)
        * Add entry point for featuretools primitives (:pr:`98`)
    * Fixes
        * Fixes error with MeanCharactersPerWord primitive with series of Nones (:pr:`101`)
    * Documentation Changes
        * Remove testing on conda forge in release.md (:pr:`84`)
    * Testing Changes
        * Update scheduler workflow to use correct name and file (:pr:`87`, :pr:`86`)
        * Add workflow to auto-merge dependency PRs (:pr:`93`)
        
    Thanks to the following people for contributing to this release:
    :user:`dvreed77`, :user:`gsheni`, :user:`jeff-hernandez`, :user:`tuethan1999`
    
v2.1.0 Dec 21, 2021
===================
    * Enhancements
        * Add primitive for total word length ``TotalWordLength`` (:pr:`79`)
        * Add primitive for median word length ``MedianWordLength`` (:pr:`80`)
    * Changes
        * Update setup.py with new and correct information (:pr:`72`)
    * Testing Changes
        * Add python 3.9 CI for unit tests and entrypoint tests (:pr:`72`)

    Thanks to the following people for contributing to this release:
    :user:`gsheni`, :user:`jeff-hernandez`

v2.0.0 Oct 13, 2021
===================
    * Changes
        * Update primitives for compatibility with Featuretools 1.0.0 (:pr:`61`)
    * Testing Changes
        * Individual CI jobs will not cancel if other jobs fail (:pr:`67`)

    Thanks to the following people for contributing to this release:
    :user:`rwedge`, :user:`thehomebrewnerd`

v1.2.0 Sept 3, 2021
===================
    * Enhancements
        * Add Elmo primitive (:pr:`64`)
    * Changes
        * Drop python 3.6 support (:pr:`57`)
    * Documentation Changes
        * Update UniversalSentenceEncoder docstring example (:pr:`42`)

    Thanks to the following people for contributing to this release:
    :user:`davesque`, :user:`gsheni`, :user:`jeff-hernandez`, :user:`rwedge`

Breaking Changes
++++++++++++++++
* Drop python 3.6 support (:pr:`57`)

v1.1.0 Oct 26, 2020
===================
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

v1.0.0 Aug 12, 2020
===================
    * Changes
        * Remove tensorflow and tensorhub as core requirements, but they
        can be installed with ``pip install nlp_primitives[complete]``. The
        ``UniversalSentenceEncoder`` primitive requires the ``nlp_primitives[complete]``
        install but all other primitives work with the standard install. (:pr:`24`)
    * Testing Changes
        * Update CircleCI to perform complete install and use matrix jobs (:pr:`24`)

    Thanks to the following people for contributing to this release:
    :user:`thehomebrewnerd`

v0.3.1
======
    * Fix installation error related to scipy version

v0.3.0
======
    * Fixed case-insensitivity in the Stopword Count Primitive
    * Made compatible with Tensorflow 2
    * Dropped Python 3.5 and added Python 3.8

v0.2.5
======
    * Removed python-dateutil as a requirement

v0.2.4
======
    * Added Featuretools Entry Point
    * PyPI Upload

v0.2.3
======
    * Small bug fixes

v0.2.2
======
    * Now comes with description for PyPI

v0.1.0
======
    * Fixed reliance on external data files

v0.0.0
======
    * Initial Release
