# Release Process

## Create nlp_primitives release on Github

#### Create release branch
1. Branch off of main. For the branch name, please use "release_vX.Y.Z" as the naming scheme (e.g. "release_v0.13.3"). Doing so will bypass our release notes checkin test which requires all other PRs to add a release note entry.

#### Bump version number
2. Bump verison number in `nlp_primitives/version.py` and `nlp_primitives/tests/test_version.py`.

#### Update changelog
1. Replace "Future Release" in `release_notes.rst` with the current date
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

In order to release on conda-forge, you can either wait for a bot to create a pull request, or use a GitHub Actions workflow

### Option a: Use a GitHub Action workflow

1. After the package has been uploaded on PyPI, the **Create Feedstock Pull Request** workflow should automatically kickoff a job. 
    * If it does not, go [here](https://github.com/alteryx/nlp_primitives/actions/workflows/create_feedstock_pr.yaml)
    * Click **Run workflow** and input the letter `v` followed by the release version (e.g. `v0.13.3`)
    * Kickoff the GitHub Action, and monitor the Job Summary.
2. Once the job has been completed, you will see summary output, with a URL. 
    * Visit that URL and create a pull request.
    * Alternatively, create the pull request by clicking the branch name (e.g. - `v0.13.3`): 
      - https://github.com/alteryx/nlp_primitives-feedstock/branches
3. Verify that the PR has the following: 
    * The `build['number']` is 0 (in __recipe/meta.yml__).
    * The `requirements['run']` (in __recipe/meta.yml__) matches the `[project]['dependencies']` in __nlp_primitives/pyproject.toml__.
    * The `test['requires']` (in __recipe/meta.yml__) matches the `[project.optional-dependencies]['test']` in __nlp_primitives/pyproject.toml__
4. Satisfy the conditions in pull request description and **merge it if the CI passes**. 

### Option b: Waiting for bot to create new PR

1. A bot should automatically create a new PR in [conda-forge/nlp_primitives-feedstock](https://github.com/conda-forge/nlp_primitives-feedstock/pulls) - note, the PR may take up to a few hours to be created
2. Update requirements changes in `recipe/meta.yaml` (bot should have handled version and source links on its own)
3. After tests pass, a maintainer will merge the PR in
