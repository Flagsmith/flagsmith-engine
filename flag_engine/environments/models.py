import typing
from datetime import datetime

from pydantic import BaseModel, Field

from flag_engine.environments.integrations.models import IntegrationModel
from flag_engine.features.models import FeatureStateModel
from flag_engine.projects.models import ProjectModel
from flag_engine.utils.datetime import utcnow_with_tz


class EnvironmentAPIKeyModel(BaseModel):
    id: int
    key: str
    created_at: datetime
    name: str
    client_api_key: str
    expires_at: typing.Optional[datetime] = None
    active: bool = True

    @property
    def is_valid(self):
        return self.active and (
            not self.expires_at or self.expires_at > utcnow_with_tz()
        )


class WebhookModel(BaseModel):
    url: str
    secret: str


class EnvironmentModel(BaseModel):
    id: int
    api_key: str
    project: ProjectModel
    feature_states: typing.List[FeatureStateModel] = Field(default_factory=list)

    name: typing.Optional[str] = None
    allow_client_traits: bool = True
    updated_at: datetime = Field(default_factory=utcnow_with_tz)
    hide_sensitive_data: bool = False
    hide_disabled_flags: typing.Optional[bool] = None
    use_identity_composite_key_for_hashing: bool = False

    amplitude_config: typing.Optional[IntegrationModel] = None
    dynatrace_config: typing.Optional[IntegrationModel] = None
    heap_config: typing.Optional[IntegrationModel] = None
    mixpanel_config: typing.Optional[IntegrationModel] = None
    rudderstack_config: typing.Optional[IntegrationModel] = None
    segment_config: typing.Optional[IntegrationModel] = None

    webhook_config: typing.Optional[WebhookModel] = None

    _INTEGRATION_ATTS = [
        "amplitude_config",
        "heap_config",
        "mixpanel_config",
        "rudderstack_config",
        "segment_config",
    ]

    @property
    def integrations_data(self) -> typing.Dict[str, typing.Dict[str, str]]:
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
