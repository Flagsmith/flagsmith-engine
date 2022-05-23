import typing


def filter_feature_segments(
    feature_segments: typing.Iterable, environment_api_key: str
) -> typing.List:
    """
    Feature segments in the django data model are associated with a segment
    and an environment we need to make sure we only get the feature segments
    for the environment we are serializing.

    :param feature_segments: queryset of django FeatureSegment model objects
    :param environment_api_key: the api key of the environment we are looking for
    :return: filtered list of django FeatureSegment model objects for the
        current environment only
    """
    if environment_api_key:
        feature_segments = list(
            filter(
                lambda fs: fs.environment.api_key == environment_api_key,
                feature_segments,
            )
        )

    return feature_segments
