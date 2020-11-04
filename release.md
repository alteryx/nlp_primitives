# Release Process
## Prerequisites
The environment variables `PYPI_USERNAME` and `PYPI_PASSWORD` must be already set in the repository as secrets. To add these variables, go to Secrets in the Settings of the repository.

## Test conda version before releasing on PyPI
Conda releases of nlp_primitives rely on PyPI's hosted nlp_primitives packages. Once a version is uploaded to PyPI we cannot update it, so it is important that the version we upload to PyPI will work for conda. We can test if a nlp_primitives release will run on conda by uploading a test release to PyPI's test server and building a conda version of nlp_primitives using the test release.

#### Upload nlp_primitives release to PyPI's test server
We need to upload a nlp_primitives package to test with the conda recipe
1. Make a new development release branch on nlp_primitives (in this example we'll be testing the 0.4.0 release)
    ```bash
    git checkout -b v0.4.0.dev
    ```
2. Update version number in `setup.py` and `nlp_primitives/__init__.py` to v0.4.0.dev0 and push branch to repo
3. Publish a new release of nlp_primitives on Github.
    1. Go to the [releases page](https://github.com/FeatureLabs/nlp_primitives/releases/) on Github
    2. Click "Draft a new release"
    3. For the target, choose the new branch (v0.4.0.dev)
    4. For the tag, use the new version number (v0.4.0.dev0)
    5. For the release title, use the new version number (v0.4.0.dev0)
    6. For the release description, write "Development release for testing purposes"
    7. Check the "This is a pre-release" box
    8. Publish the release
4. The new release will be uploaded to TestPyPI automatically

#### Set up fork of our conda-forge repo
Branches on the conda-forge nlp_primitives repo are automatically built and the package uploaded to conda-forge, so to test a release without uploading to conda-forge we need to fork the repo and develop on the fork.
1. Fork conda-forge/-feedstock: visit https://github.com/conda-forge/nlp_primitives-feedstock and click fork
2. Clone forked repo locally
3. Add conda-forge repo as the 'upstream' repository
    ```bash
    git remote add upstream https://github.com/conda-forge/nlp_primitives-feedstock.git
    ```
4. If you made the fork previously and its master branch is missing commits, update it with any changes from upstream
    ```bash
    git fetch upstream
    git checkout master
    git merge upstream/master
    git push origin master
    ```
5. Make a branch with the version you want to release
    ```bash
    git checkout -b v0.4.0dev0
    ```

#### Update conda recipe to use TestPyPI release of nlp_primitives
Fields to update in `recipe/meta.yaml` of feedstock repo:
* Always update:
    * Set the new release number (e.g. v0.4.0.dev0)
        ```
        {% set version = "0.4.0.dev0" %}
        ```
    * Source fields
        * url - visit https://test.pypi.org/project/nlp-primitives/, find correct release, go to download files page, and copy link location of the tar.gz file
        * sha256 - from the download files page, click the view hashes button for the tar.gz file and copy the sha256 digest
        ```
        source:
          url: https://test-files.pythonhosted.org/packages/11/7c/348ebaf78da667a6d14eda1f320da8f126a58baf47e586166ed3b6e33309/nlp_primitives-0.0.0.tar.gz
          sha256: c2e4452a27df254643ea9143c465fc811b860607db377bbfee305c2b4b1cd672
       ```
* Update if dependencies have changed:
    * setup-requirements.txt dependencies are host requirements
        ```
        requirements:
          host:
            - pip
            - python
        ```
    * requirements.txt dependencies are run requirements
        ```
        requirements:
          run:
            - click
            - cloupickle
        ```
    * test-requirements.txt dependencies are test requirements
        ```
        test:
          requires:
            - fastparquet
            - mock
        ```

#### Test with conda-forge CI
1. Install conda
    1. If using pyenv, `pyenv install miniconda3-latest`
    2. Otherwise follow instructions in [conda docs](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)
2. Install conda-smithy (conda-forge tool to update boilerplate in repo)
    ```bash
    conda install -n root -c conda-forge conda-smithy
    ```
3. Run conda-smithy on feedstock
    ```bash
    cd /path/to/feedstock/repo
    conda-smithy rerender --commit auto
    ```
4. Push updated branch to the forked feedstock repo
3. Make a PR on conda-forge/nlp_primitives-feedstock from the forked repo and let CI tests run - add "[DO NOT MERGE]" to the PR name to indicate this is PR should not be merged in
4. After the tests pass, close the PR without merging

## Create nlp_primitives release on Github

#### Create release branch
1. Branch off of main and name the branch the release version number (e.g. v0.4.0)

#### Bump version number
2. Bump verison number in `setup.py`, and `nlp_primitives/__init__.py`.

#### Update changelog
1. Replace "Future Release" in `docs/source/changelog.rst` with the current date
    ```
    **v0.4.0** Aug 11, 2020
    ```
2. Remove any unused changelog sections for this release (e.g. Fixes, Testing Changes)
3. Add yourself to the list of contributors to this release and put the contributors in alphabetical order
4. The release PR does not need to be mentioned in the list of changes

## Create Release PR
A release PR should have the version number as the title and the changelog updates as the PR body text. The contributors line is not necessary. The special sphinx docs syntax (:pr:`547`) needs to be changed to github link syntax (#547).

## Create GitHub Release
After the release pull request has been merged into the main branch, it is time draft the github release.
* The target should be the main branch
* The tag should be the version number with a v prefix (e.g. v0.4.0)
* Release title is the same as the tag
* Release description should be the full changelog updates for the release, including the line thanking contributors. Contributors should also have their links changed from the docs syntax (:user:`rwedge`) to github syntax (@rwedge)
* This is not a pre-release
* Publishing the release will automatically upload the package to PyPI

## Release on conda-forge
1. A bot should automatically create a new PR in conda-forge/nlp_primitives-feedstock
2. Update requirements changes in `recipe/meta.yaml` (bot should have handled version and source links on its own). Non-maintainers will need a maintainer to merge their changes into the bot's pull request.
3. After tests pass, a maintainer will merge the PR in