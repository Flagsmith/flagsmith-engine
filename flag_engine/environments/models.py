import typing
from dataclasses import dataclass, field

from flag_engine.projects.models import Project
from flag_engine.segments.models import SegmentOverride
from flag_engine.features.models import Feature, FeatureState


@dataclass
class Environment:
    id: int
    api_key: str
    project: Project
    feature_states: typing.List[FeatureState] = field(default_factory=list)
    segment_overrides: typing.List[SegmentOverride] = field(default_factory=list)

    def get_feature_state_for_feature(self, feature: Feature) -> FeatureState:
        return next(filter(lambda fs: fs.feature == feature, self.feature_states))
