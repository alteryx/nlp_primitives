# NLP Primitives

[![CircleCI](https://circleci.com/gh/FeatureLabs/nlp_primitives/tree/master.svg?style=shield)](https://circleci.com/gh/FeatureLabs/nlp_primitives/tree/master)
[![codecov](https://codecov.io/gh/FeatureLabs/nlp_primitives/branch/master/graph/badge.svg)](https://codecov.io/gh/FeatureLabs/nlp_primitives)
[![Documentation Status](https://readthedocs.org/projects/nlp_primitives/badge/?version=latest)](http://docs.nlp_primitives/en/latest/?badge=latest)

### Install
```shell
pip install 'featuretools[nlp_primitives]'
```
## Calculating Features
In `nlp_primitives`, this is how to calculate a feature.
```python
from nlp_primitives import diversity_score

data = ["hello there, this is a new featuretools library",
        "this will add new natrual language primitives"]

agg_autocorrelation(data, param=param)
```
```
[('f_agg_"mean"__maxlag_5', 0.1717171717171717)]
```
With nlp_primitives primtives in `featuretools`, this is how to calculate the same feature.
```python
from featuretools.nlp_primitives import AggAutocorrelation

data = list(range(10))
AggAutocorrelation(f_agg='mean', maxlag=5)(data)
```
```
0.1717171717171717
```
## Combining Primitives
In `featuretools`, this is how to combine nlp_primitives primitives with built-in or other installed primitives.
```python
import featuretools as ft
from featuretools.nlp_primitives import AggAutocorrelation, Mean

entityset = ft.demo.load_mock_customer(return_entityset=True)
agg_primitives = [Mean, AggAutocorrelation(f_agg='mean', maxlag=5)]
feature_matrix, features = ft.dfs(entityset=entityset, target_entity='sessions', agg_primitives=agg_primitives)
```

## Feature Labs
<a href="https://www.featurelabs.com/">
    <img src="http://www.featurelabs.com/wp-content/uploads/2017/12/logo.png" alt="Featuretools" />
</a>

NLP Primitives is an open source project created by [Feature Labs](https://www.featurelabs.com/). To see the other open source projects we're working on visit Feature Labs [Open Source](https://www.featurelabs.com/open). If building impactful data science pipelines is important to you or your business, please [get in touch](https://www.featurelabs.com/contact/).