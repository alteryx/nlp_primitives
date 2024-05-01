=========
Changelog
=========

Future Release
==============
    * Enhancements
    * Fixes
    * Changes
        * Temporarily restrict tensorflow version for complete install (:pr:`277`)
        * Remove Mac specific tensorflow requirements (:pr:`281`)
    * Documentation Changes
    * Testing Changes

    Thanks to the following people for contributing to this release:
    :user:`thehomebrewnerd`

v2.12.0 Feb 26, 2024
====================
    .. warning::
        This release of nlp-primitives will not support Python 3.8

    * Changes
        * Remove support for Python 3.8 and add support for 3.11 (:pr:`269`)
    * Testing Changes
       * Update ``release.yaml`` to use trusted publisher for PyPI releases (:pr:`269`)

    Thanks to the following people for contributing to this release:
    :user:`thehomebrewnerd`

v2.11.0 Apr 13, 2023
====================
    * Fixes
        * Fix Makefile ``package`` command (:pr:`241`)
    * Changes
       * Fix ruff argument in pyproject.toml (:pr:`239`)
       * Remove `constants.py` (:pr:`243`)
       * Remove Woodwork as a core requirement (:pr:`258`)
    * Testing Changes
       * Add pull request check for linked issues to CI workflow (:pr:`245`)

    Thanks to the following people for contributing to this release:
    :user:`gsheni`, :user:`sbadithe`

v2.10.0 Jan 10, 2023
====================
    * Enhancements
        * Add conda create feedstock pull request workflow (:pr:`220`)
        * Improve ``PartOfSpeech`` docstring (:pr:`224`)
    * Fixes
        * Fix handling of all-whitepace strings in ``MeanCharactersPerSentence`` (:pr:`234`)
    * Changes
        * Update workflow_dispatch to release workflow (:pr:`221`)
        * Add ruff, remove isort, and add more pre-commits (:pr:`237`)
    * Testing Changes
        * Add pytest-xdist as test requirement and use auto option to use all cores when running unit tests (:pr:`218`)
        * Adds Windows install test (:pr:`219`)

    Thanks to the following people for contributing to this release:
    :user:`gsheni`, :user:`sbadithe`

v2.9.0 Oct 24, 2022
===================
    * Fixes
        * Fixes erroneous case-sensitive stopword checking in ``clean_tokens`` (:pr:`211`)
    * Changes
        * Remove primitives that were transferred to Featuretools (:pr:`214`)

    Thanks to the following people for contributing to this release:
    :user:`sbadithe`, :user:`thehomebrewnerd`

Breaking Changes
++++++++++++++++
* Multiple primitives were removed from nlp_primitives and transferred to Featuretools as standad primitives. See :pr:`214` for a
complete list of primitives that were moved. These primitives can now be imported directly from Featuretools. For example,
use ``from featuretools.primitives import CountString`` instead of the previous import of ``from nlp_primitives import CountString``.


v2.8.0 Sep 14, 2022
===================
    * Enhancements
        * Add `NumberOfHashtags` and `NumberOfMentions`` primitives (:pr:`180`)
        * Add `NumberOfUniqueWords` primitive (:pr:`187`)
        * Add `NumberOfSentences` and `MeanSentenceLength` primitives (:pr:`188`)
        * Add `NumberOfWordsInQuotes` primitive (:pr:`196`)
    * Fixes
        * Update README.md with Alteryx info (:pr:`167`)
    * Changes
        * Add Woodwork as core dependency (:pr:`170`)
        * Add support for Python 3.10 (:pr:`175`)
        * Drop support for Python 3.7 (:pr:`176`)
        * Change `TitleWordCount`, `PunctuationCount`, `UpperCaseCount` to use `CountString` (:pr:`183`)
        * Remove readthedocs and docs requirements (:pr:`193`)
        * Use pyproject.toml only (move away from setup.cfg) (:pr:`201`)
    * Testing Changes
        * Change codecov v3 for GitHub workflow (:pr:`184`)

    Thanks to the following people for contributing to this release:
    :user:`gsheni`, :user:`sbadithe`, :user:`thehomebrewnerd`

v2.7.1 Jun 29, 2022
===================
    * Fixes
        * Clean up naming of LSA features to prevent full custom corpus from being displayed (:pr:`161`)

    Thanks to the following people for contributing to this release:
    :user:`thehomebrewnerd`

v2.7.0 Jun 16, 2022
===================
    * Enhancements
        * Allow users to optionally pass in a custom corpus to use with the LSA primitive (:pr:`148`)
    * Fixes
        * Fix bug in ``CountString`` with null values (:pr:`154`)
        * Fix a bug with nltk data was not included in package (:pr:`157`)
    * Documentation Changes
        * Update release branch naming convention in documentation (:pr:`155`)
    * Testing Changes
        * Add workflow to test nlp_primitives without test dependencies (:pr:`157`)

    Thanks to the following people for contributing to this release:
    :user:`gsheni`, :user:`rwedge`, :user:`thehomebrewnerd`

v2.6.0 Jun 16, 2022
===================
    * Changes
        * Transition to use pyproject.toml and setup.cfg (moving away from setup.py) (:pr:`127`, :pr:`132`)
        * ``Elmo`` and ``UniversalSentenceEncoder`` added to the ``nlp_primitives.tensorflow`` module namespace (:pr:`150`)
    * Testing Changes
        * Fix latest dependency checker to create PR (:pr:`129`)
        * Fixed unit tests workflow test choice logic (:pr:`151`)

    Thanks to the following people for contributing to this release:
    :user:`gsheni`, :user:`rwedge`, :user:`thehomebrewnerd`

v2.5.0 Apr 7, 2022
==================
    * Fixes
        * Fix ``NumUniqueSeparators`` to allow for serialization and deserialization (:pr:`122`)
    * Changes
        * Speed up LSA primitive initialization (:pr:`118`)
    * Testing Changes
        * Fix install test and update Makefile (:pr:`123`)

    Thanks to the following people for contributing to this release:
    :user:`rwedge`, :user:`thehomebrewnerd`

v2.4.0 Mar 31, 2022
===================
    * Changes
        * Added pip dependencies for M1 Macs (:pr:`117`)
    * Testing Changes
        * Added Release Notes CI Check (:pr:`110`)
        * Added CI check to ensure entrypoint works with Featuretools (:pr:`111`)
        * Fixed workflow that tests latest changes to featuretools (:pr:`112`)

    Thanks to the following people for contributing to this release:
    :user:`dvreed77`, :user:`gsheni`, :user:`jeff-hernandez`, :user:`thehomebrewnerd`

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
