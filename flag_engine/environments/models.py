import typing
from dataclasses import dataclass, field
from datetime import datetime

from flag_engine.environments.integrations.models import IntegrationModel
from flag_engine.features.models import FeatureStateModel
from flag_engine.projects.models import ProjectModel


@dataclass
class EnvironmentAPIKeyModel:
    id: int
    key: str
    created_at: datetime
    name: str
    client_api_key: str
    expires_at: datetime = None
    active: bool = True

    @property
    def is_valid(self):
        return self.active and (not self.expires_at or self.expires_at > datetime.now())


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
