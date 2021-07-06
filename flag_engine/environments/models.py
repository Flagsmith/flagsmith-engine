import typing
from dataclasses import dataclass, field

from flag_engine.environments.integrations.models import IntegrationModel
from flag_engine.features.models import FeatureStateModel
from flag_engine.projects.models import ProjectModel
from flag_engine.segments.models import SegmentOverrideModel


@dataclass
class EnvironmentModel:
    id: int
    api_key: str
    project: ProjectModel
    feature_states: typing.List[FeatureStateModel] = field(default_factory=list)
    segment_overrides: typing.List[SegmentOverrideModel] = field(default_factory=list)
    amplitude_config: IntegrationModel = None
    segment_config: IntegrationModel = None
    mixpanel_config: IntegrationModel = None
    heap_config: IntegrationModel = None
