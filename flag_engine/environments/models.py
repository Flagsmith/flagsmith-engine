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
    url: str
    secret: str


@dataclass
class EnvironmentModel:
    id: int
    api_key: str
    project: ProjectModel
    feature_states: typing.List[FeatureStateModel] = field(default_factory=list)

    name: str = None
    allow_client_traits: bool = True
    updated_at: datetime = field(default_factory=utcnow_with_tz)
    use_mv_v2_evaluation: bool = False
    hide_sensitive_data: bool = False

    amplitude_config: typing.Optional[IntegrationModel] = None
    dynatrace_config: typing.Optional[IntegrationModel] = None
    heap_config: typing.Optional[IntegrationModel] = None
    mixpanel_config: typing.Optional[IntegrationModel] = None
    rudderstack_config: typing.Optional[IntegrationModel] = None
    segment_config: typing.Optional[IntegrationModel] = None

    hide_disabled_flags: typing.Optional[bool] = None

    webhook_config: typing.Optional[WebhookModel] = None

    _INTEGRATION_ATTS = [
        "amplitude_config",
        "dynatrace_config",
        "heap_config",
        "mixpanel_config",
        "rudderstack_config",
        "segment_config",
    ]

    @property
    def integrations_data(self) -> dict:
        """
        Return a dictionary representation of all integration config objects.

            e.g.
            {
                "mixpanel_config": {"base_url": None, "api_key": "some-key"},
                "segment_config": {
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

    def get_hide_disabled_flags(self) -> bool:
        if self.hide_disabled_flags is not None:
            return self.hide_disabled_flags
        return self.project.hide_disabled_flags
