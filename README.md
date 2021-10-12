# NLP Primitives

![Tests](https://github.com/alteryx/nlp_primitives/workflows/Tests/badge.svg)

nlp_primitives is a Python library with Natural Language Processing Primitives, intended for use with [Featuretools](https://github.com/Featuretools/featuretools).

nlp_primitives allows you to make use of text data in your machine learning pipeline in the same pipeline as the rest of your data.

### Install
There are two options for installing nlp_primitives. Both of the options will also install Featuretools if it is not already installed.

The first option is to install a version of nlp_primitives that does not include Tensorflow. With this option, primitives that depend on Tensorflow cannot be used. Currently, the only primitive that can not be used with this install option is ``UniversalSentenceEncoder``.

nlp_primitives without Tensorflow can be installed with pip:
```shell
pip install nlp_primitives
```
or from the conda-forge channel on conda:
```shell
conda install -c conda-forge nlp-primitives
```

The second option is to install the complete version of nlp_primitives, which will also install Tensorflow and allow use of all primitives. 

To install the complete version of nlp_primitives with pip:
```shell
pip install "nlp_primitives[complete]"
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

## Feature Labs
<a href="https://www.featurelabs.com/">
    <img src="http://www.featurelabs.com/wp-content/uploads/2017/12/logo.png" alt="Featuretools" />
</a>

NLP Primitives is an open source project created by [Feature Labs](https://www.featurelabs.com/). To see the other open source projects we're working on visit Feature Labs [Open Source](https://www.featurelabs.com/open). If building impactful data science pipelines is important to you or your business, please [get in touch](https://www.featurelabs.com/contact/).
