import os
import re
import shutil
import string
import tarfile
import tempfile

import nltk
import numpy as np
import pandas as pd
from featuretools.primitives.base import TransformPrimitive
from featuretools.utils import is_python_2
from featuretools.variable_types import Numeric, Text


class PartOfSpeechCount(TransformPrimitive):
    """Calculates the occurences of each different part of speech.

    Description:
        Given a list of strings, categorize each word in the string as
        a different part of speech, and return the total count for each
        of 15 different categories of speech.

        If a string is missing, return `NaN`.

    Examples:
        >>> x = ['He was eating cheese', '']
        >>> part_of_speech_count = PartOfSpeechCount()
        >>> part_of_speech_count(x).tolist()
        [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [1.0, 0.0], [0.0, 0.0]]
    """
    name = "part_of_speech_count"
    input_types = [Text]
    return_type = Numeric
    default_value = 0
    filename = "nltk-data.tar.gz"

    def __init__(self):
        self.number_output_features = 15
        self.n = 15

    def get_function(self):
        fp = os.path.normpath(os.path.join(os.path.realpath(__file__), '../data/nltk-data.tar.gz'))
        dp = os.path.normpath(os.path.join(fp, '../nltk-data'))
        nltk.data.path = [os.path.normpath(os.path.join(fp, '../nltk-data/nltk-data'))]
        wn = nltk.WordNetLemmatizer()
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

        def clean_tokens(textstr):
            textstr = nltk.word_tokenize(textstr)

            processed = [ch.lower() for ch in textstr if ch not in
                         set(string.punctuation).union(
                         set(nltk.corpus.stopwords.words('english')))]
            processed = ['0' if re.search('[0-9]+', ch) else ch for ch in processed]
            processed = [wn.lemmatize(w) for w in processed]
            return processed

        types = ['C', 'D', 'E', 'F', 'I', 'J',
                 'L', 'M', 'N', 'P', 'R', 'T',
                 'U', 'V', 'W']

        def part_of_speech_count(x):
            li = []
            for el in x:
                if pd.isnull(el):
                    li.append([np.nan] * 15)
                else:
                    tags = nltk.pos_tag(clean_tokens(el))
                    fd = nltk.FreqDist([b[0] for (a, b) in tags])
                    li.append([float(fd[i]) for i in types])
            li = (np.array(li).T).tolist()
            return pd.Series(li)

        return part_of_speech_count
