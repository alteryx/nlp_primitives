# NLP Primitives

<p align="center">
    <a href="https://codecov.io/gh/alteryx/nlp_primitives">
        <img src="https://codecov.io/gh/alteryx/nlp_primitives/branch/main/graph/badge.svg"/>
    </a>
    <a href="https://github.com/alteryx/nlp_primitives/actions?query=branch%3Amain+workflow%3ATests" target="_blank">
        <img src="https://github.com/alteryx/nlp_primitives/workflows/Tests/badge.svg?branch=main" alt="Tests" />
    </a>
    <a href="https://badge.fury.io/py/nlp_primitives" target="_blank">
        <img src="https://badge.fury.io/py/nlp_primitives.svg?maxAge=2592000" alt="PyPI Version" />
    </a>
    <a href="https://anaconda.org/conda-forge/nlp_primitives" target="_blank">
        <img src="https://anaconda.org/conda-forge/nlp-primitives/badges/version.svg" alt="Anaconda Version" />
    </a>
    <a href="https://stackoverflow.com/questions/tagged/featuretools" target="_blank">
        <img src="http://img.shields.io/badge/questions-on_stackoverflow-blue.svg" alt="StackOverflow" />
    </a> 
    <a href="https://pepy.tech/project/nlp_primitives" target="_blank">
        <img src="https://pepy.tech/badge/nlp_primitives/month" alt="PyPI Downloads" />
    </a>
</p>
<hr>

nlp_primitives is a Python library with Natural Language Processing Primitives, intended for use with [Featuretools](https://github.com/Featuretools/featuretools).

nlp_primitives allows you to make use of text data in your machine learning pipeline in the same pipeline as the rest of your data.

## Installation

There are two options for installing nlp_primitives. Both of the options will also install Featuretools if it is not already installed.

The first option is to install a version of nlp_primitives that does not include Tensorflow. With this option, primitives that depend on Tensorflow cannot be used. Currently, the only primitive that can not be used with this install option is ``UniversalSentenceEncoder``.

#### PyPi
nlp_primitives without Tensorflow can be installed with pip:
```shell
python -m pip install nlp_primitives
```

#### conda-forge
or from the conda-forge channel on conda:
```shell
conda install -c conda-forge nlp-primitives
```

The second option is to install the complete version of nlp_primitives, which will also install Tensorflow and allow use of all primitives. 

To install the complete version of nlp_primitives with pip:
```shell
python -m pip install "nlp_primitives[complete]"
```
or from the conda-forge channel on conda:
```shell
conda install -c conda-forge nlp-primitives-complete
```

### Demos

* [Blog Post](https://blog.featurelabs.com/natural-language-processing-featuretools/)
* [Predict resturant review ratings](https://github.com/FeatureLabs/predict-restaurant-rating)

## Calculating Features
With nlp_primitives primtives in `featuretools`, this is how to calculate the same feature.

```python
from featuretools.nlp_primitives import PolarityScore

data = ["hello, this is a new featuretools library",
        "this will add new natural language primitives",
        "we hope you like it!"]

pol = PolarityScore()
pol(data)
```
```
0    0.365
1    0.385
2    1.000
dtype: float64
```
## Combining Primitives
In `featuretools`, this is how to combine nlp_primitives primitives with built-in or other installed primitives.
```python
import featuretools as ft
from featuretools.nlp_primitives import TitleWordCount
from featuretools.primitives import Mean

entityset = ft.demo.load_retail()
feature_matrix, features = ft.dfs(entityset=entityset, target_dataframe_name='products', agg_primitives=[Mean], trans_primitives=[TitleWordCount])

feature_matrix.head(5)
```
```
           MEAN(order_products.quantity)  MEAN(order_products.unit_price)  MEAN(order_products.total)  TITLE_WORD_COUNT(description)
product_id
10002                         16.795918                          1.402500                   23.556276                           3.0
10080                         13.857143                          0.679643                    8.989357                           3.0
10120                          6.620690                          0.346500                    2.294069                           2.0
10123C                         1.666667                          1.072500                    1.787500                           3.0
10124A                           3.2000                            0.6930                      2.2176                           5.0
```

## Development
To install from source, clone this repo and run
```bash
make installdeps-test
```

This will install all pip dependencies.

## Built at Alteryx

**NLP Primitives** is an open source project maintained by [Alteryx](https://www.alteryx.com). To see the other open source projects we’re working on visit [Alteryx Open Source](https://www.alteryx.com/open-source). If building impactful data science pipelines is important to you or your business, please get in touch.

<p align="center">
  <a href="https://www.alteryx.com/open-source">
    <img src="https://alteryx-oss-web-images.s3.amazonaws.com/OpenSource_Logo-01.png" alt="Alteryx Open Source" width="800"/>
  </a>
</p>
