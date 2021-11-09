import typing
from dataclasses import dataclass, field

from flag_engine.environments.integrations.models import IntegrationModel
from flag_engine.features.models import FeatureStateModel
from flag_engine.projects.models import ProjectModel
from flag_engine.segments.models import SegmentModel
from flag_engine.utils.exceptions import FeatureStateNotFound


def environment_feature_state_filter(feature_state: FeatureStateModel) -> bool:
    return feature_state.segment_id is None and feature_state.identity_id is None


def segment_override_feature_state_filter(feature_state: FeatureStateModel) -> bool:
    return feature_state.segment_id is not None


@dataclass
class EnvironmentModel:
    id: int
    api_key: str
    project: ProjectModel
    _all_feature_states: typing.List[FeatureStateModel] = field(default_factory=list)
    amplitude_config: IntegrationModel = None
    segment_config: IntegrationModel = None
    mixpanel_config: IntegrationModel = None
    heap_config: IntegrationModel = None

    @property
    def feature_states(self) -> typing.List[FeatureStateModel]:
        return list(filter(environment_feature_state_filter, self._all_feature_states))

    @property
    def segment_overrides(self) -> typing.List[FeatureStateModel]:
        return list(
            filter(segment_override_feature_state_filter, self._all_feature_states)
        )

    def get_segment(self, segment_id: int) -> SegmentModel:
        return next(
            filter(lambda segment: segment.id == segment_id, self.project.segments)
        )

    def get_feature_state(self, feature_name: str) -> FeatureStateModel:
        try:
            return next(
                filter(lambda f: f.feature.name == feature_name, self.feature_states)
            )

        except StopIteration:
            raise FeatureStateNotFound()
