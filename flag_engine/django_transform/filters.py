import typing


class Reverser:
    """
    Helper class to allow us to reverse the sort direction for individual keys when
    sorting by multiple keys

        e.g. s = sorted(l, key=lambda e: (attr1, Reverser(attr2)))

    """

    def __init__(self, obj: typing.Any):
        self.obj = obj

    def __eq__(self, other):
        return self.obj == other.obj

    def __lt__(self, other):
        return other.obj < self.obj


def sort_and_filter_feature_segments(
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

    # TODO: determine why this sorting is necessary
    return sorted(
        feature_segments, key=lambda fs: (fs.feature_id, Reverser(fs.priority))
    )
