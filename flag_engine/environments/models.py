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

    _INTEGRATION_ATTS = [
        "amplitude_config",
        "segment_config",
        "mixpanel_config",
        "heap_config",
    ]

    @property
    def integrations_data(self) -> dict:
        integrations_data = {}
        for integration_attr in self._INTEGRATION_ATTS:
            integration_config: IntegrationModel = getattr(self, integration_attr, None)
            if integration_config:
                integrations_data[integration_attr] = {
                    "base_url": integration_config.base_url,
                    "api_key": integration_config.api_key,
                }
        return integrations_data
