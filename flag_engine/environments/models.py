import typing
from dataclasses import dataclass, field
from datetime import datetime

from flag_engine.environments.integrations.models import IntegrationModel
from flag_engine.features.models import FeatureStateModel
from flag_engine.projects.models import ProjectModel
from flag_engine.utils.datetime import utcnow_with_tz


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
        return self.active and (
            not self.expires_at or self.expires_at > utcnow_with_tz()
        )


@dataclass
class WebhookModel:
    created_at: datetime
    updated_at: datetime
    url: str
    secret: str
    enabled: bool = True


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
    dynatrace_config: IntegrationModel = None
    webhooks: typing.List[WebhookModel] = field(default_factory=list)

    _INTEGRATION_ATTS = [
        "amplitude_config",
        "segment_config",
        "mixpanel_config",
        "heap_config",
        "dynatrace_config",
        "webhooks",
    ]

    @property
    def integrations_data(self) -> dict:
        """
        Return a dictionary representation of all integration config objects.

            e.g.
            {
                "mixpanel_configuration": {"base_url": None, "api_key": "some-key"},
                "segment_configuration": {
                    "base_url": "https://api.segment.com",
                    "api_key": "some-key",
                }
            }
        """

        integrations_data = {}
        for integration_attr in self._INTEGRATION_ATTS:
            integration_config: IntegrationModel = getattr(self, integration_attr, None)
            if integration_config:
                integrations_data[integration_attr] = {
                    "base_url": integration_config.base_url,
                    "api_key": integration_config.api_key,
                    "entity_selector": integration_config.entity_selector,
                }
        return integrations_data
