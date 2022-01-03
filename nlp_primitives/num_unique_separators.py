import pandas as pd
from featuretools.primitives import TransformPrimitive
from woodwork.column_schema import ColumnSchema
from woodwork.logical_types import IntegerNullable, NaturalLanguage

natural_language_separators = " .,!?;\n"


class NumUniqueSeparators(TransformPrimitive):
    """Calculates the number of unique separators.

    Description:
        Given list of strings and a string of separators, determine
        the number of unique separators in each string. If a string
        is null determined by pd.isnull return pd.NA.

    Examples:
        >>> x = ['First. Line.', 'This. is the second, line!', 'notinlist@#$%^%&']
        >>> num_unique_separators = NumUniqueSeparators(".,!")
        >>> num_unique_separators(x).tolist()
        [1, 3, 0]
    """

    name = "num_unique_separators"
    input_types = [ColumnSchema(logical_type=NaturalLanguage)]
    return_type = ColumnSchema(logical_type=IntegerNullable, semantic_tags={'numeric'})

    def __init__(self, separators=natural_language_separators):
        if separators is not None:
            self.separators = set(separators)

    def get_function(self):
        def count_unique_separator(s):
            if pd.isnull(s):
                return pd.NA
            return len(self.separators.intersection(set(s)))

        def get_separator_count(column):
            assert self.separators is not None, "separators needs to be defined"
            return column.apply(count_unique_separator)

        return get_separator_count

    def generate_names(self, base_feature_names):
        name = self.generate_name(base_feature_names)
        return f"{name}[{self.separators}]"
