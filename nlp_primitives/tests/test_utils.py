from inspect import signature

import featuretools as ft
import pytest
from featuretools import (
    calculate_feature_matrix,
    dfs,
    list_primitives,
    load_features,
    save_features,
)
from featuretools.tests.testing_utils import make_ecommerce_entityset

ft.primitives._load_primitives()
PRIMITIVES = list_primitives()


class PrimitiveT:
    primitive = None

    @pytest.fixture(autouse=True, scope="session")
    def es(self):
        es = make_ecommerce_entityset()
        return es

    def test_name_and_desc(self):
        assert self.primitive.name is not None
        assert self.primitive.__doc__ is not None
        docstring = self.primitive.__doc__
        short_description = docstring.splitlines()[0]
        first_word = short_description.split(" ", 1)[0]
        valid_verbs = [
            "Calculates",
            "Determines",
            "Transforms",
            "Computes",
            "Shifts",
            "Extracts",
            "Applies",
        ]
        assert any(s in first_word for s in valid_verbs)
        assert self.primitive.input_types is not None

    def test_name_in_primitive_list(self):
        assert PRIMITIVES.name.eq(self.primitive.name).any()

    def test_arg_init(self):
        primitive_ = self.primitive()
        # determine the optional arguments in the __init__
        init_params = signature(self.primitive.__init__)
        for name, parameter in init_params.parameters.items():
            if parameter.default is not parameter.empty:
                assert hasattr(primitive_, name)

    def test_serialize(self, es):
        features = dfs(
            entityset=es,
            target_dataframe_name="log",
            trans_primitives=[self.primitive],
            max_features=-1,
            max_depth=3,
            features_only=True,
        )

        feat_to_serialize = None
        for feature in features:
            if feature.primitive.__class__ == self.primitive:
                feat_to_serialize = feature
                break
            for base_feature in feature.get_dependencies(deep=True):
                if base_feature.primitive.__class__ == self.primitive:
                    feat_to_serialize = base_feature
                    break
        assert feat_to_serialize is not None

        # Skip calculating feature matrix for long running primitives
        skip_primitives = ["elmo"]

        if self.primitive.name not in skip_primitives:
            df1 = calculate_feature_matrix([feat_to_serialize], entityset=es)

        new_feat = load_features(save_features([feat_to_serialize]))[0]
        assert isinstance(new_feat, ft.FeatureBase)

        if self.primitive.name not in skip_primitives:
            df2 = calculate_feature_matrix([new_feat], entityset=es)
            assert df1.equals(df2)


def find_applicable_primitives(primitive):
    from featuretools.primitives.utils import (
        get_aggregation_primitives,
        get_transform_primitives,
    )

    all_transform_primitives = list(get_transform_primitives().values())
    all_aggregation_primitives = list(get_aggregation_primitives().values())
    applicable_transforms = find_stackable_primitives(
        all_transform_primitives,
        primitive,
    )
    applicable_aggregations = find_stackable_primitives(
        all_aggregation_primitives,
        primitive,
    )
    return applicable_transforms, applicable_aggregations


def find_stackable_primitives(all_primitives, primitive):
    applicable_primitives = []
    for x in all_primitives:
        if x.input_types == [primitive.return_type]:
            applicable_primitives.append(x)
    return applicable_primitives


def valid_dfs(
    es,
    aggregations,
    transforms,
    feature_substrings,
    target_dataframe_name="log",
    multi_output=False,
    max_depth=3,
    max_features=-1,
    instance_ids=[0, 1, 2, 3],
):
    if not isinstance(feature_substrings, list):
        feature_substrings = [feature_substrings]

    features = dfs(
        entityset=es,
        target_dataframe_name=target_dataframe_name,
        agg_primitives=aggregations,
        trans_primitives=transforms,
        max_features=max_features,
        max_depth=max_depth,
        features_only=True,
    )
    applicable_features = []
    for feat in features:
        for x in feature_substrings:
            if x in feat.get_name():
                applicable_features.append(feat)
    if len(applicable_features) == 0:
        raise ValueError(
            "No feature names with %s, verify the name attribute                       "
            "    is defined and/or generate_name() is defined to                       "
            "    return %s " % (feature_substrings, feature_substrings),
        )
    df = ft.calculate_feature_matrix(
        entityset=es,
        features=applicable_features,
        instance_ids=instance_ids,
    )

    ft.encode_features(df, applicable_features)

    # TODO: check the multi_output shape by checking
    # feature.number_output_features for each feature
    # and comparing it with the matrix shape
    if not multi_output:
        assert len(applicable_features) == df.shape[1]
    return
