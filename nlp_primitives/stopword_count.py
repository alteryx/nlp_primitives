# -*- coding: utf-8 -*-
import os
import shutil
import tarfile
import tempfile

import nltk
import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from featuretools.utils import is_python_2
from featuretools.variable_types import Numeric, Text


class StopwordCount(TransformPrimitive):
    """Determines number of stopwords in a string.

    Description:
        Given list of strings, determine the number of stopwords
        characters in each string. Looks for any of the English
        stopwords defined in `nltk.corpus.stopwords`. Case insensitive.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['This is a test string.', 'This is second string', 'third string']
        >>> stopword_count = StopwordCount()
        >>> stopword_count(x).tolist()
        [3.0, 2.0, 0.0]
    """
    name = "stopword_count"
    input_types = [Text]
    return_type = Numeric
    default_value = 0
    filename = "nltk-data.tar.gz"

    def get_function(self):
        fp = os.path.normpath(os.path.join(os.path.realpath(__file__), '../data/nltk-data.tar.gz'))
        dp = os.path.normpath(os.path.join(fp, '../nltk-data'))
        nltk.data.path = [os.path.normpath(os.path.join(fp, '../nltk-data/nltk-data'))]
        if not os.path.exists(nltk.data.path[0]):
            try:
                tf = tempfile.mkdtemp()
                if is_python_2():
                    def unpacktar(filename, extract_dir):
                        tarobj = tarfile.open(filename)
                        try:
                            tarobj.extractall(extract_dir)
                        finally:
                            tarobj.close()
                    unpacktar(fp, tf)
                else:
                    shutil.unpack_archive(fp, tf)
                shutil.copytree(tf, dp)
            finally:
                shutil.rmtree(tf)

        def stopword_count(array):
            li = []
            swords = set(nltk.corpus.stopwords.words('english'))
            for el in array:
                if pd.isnull(el):
                    li.append(np.nan)
                else:
                    li.append(sum(map(lambda x: x in swords, nltk.tokenize.word_tokenize(el))))
            return pd.Series(li)

        return stopword_count
