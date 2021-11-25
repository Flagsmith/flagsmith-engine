import typing
from dataclasses import dataclass, field

from flag_engine.environments.integrations.models import IntegrationModel
from flag_engine.features.models import FeatureStateModel
from flag_engine.projects.models import ProjectModel
from flag_engine.segments.models import SegmentModel
from flag_engine.utils.exceptions import FeatureStateNotFound


@dataclass
class EnvironmentModel:
    id: int
    api_key: str
    project: ProjectModel
    feature_states: typing.List[FeatureStateModel] = field(default_factory=list)
    amplitude_config: IntegrationModel = None
    segment_config: IntegrationModel = None
    mixpanel_config: IntegrationModel = None
    heap_config: IntegrationModel = None

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
