import typing

from pydantic import BaseModel, Field

from flag_engine.organisations.models import OrganisationModel
from flag_engine.segments.models import SegmentModel


class ProjectModel(BaseModel):
    id: int
    name: str
    organisation: OrganisationModel
    hide_disabled_flags: bool
    segments: typing.List[SegmentModel] = Field(default_factory=list)
    enable_realtime_updates: bool = False
    server_key_only_feature_ids: typing.List[int] = Field(default_factory=list)
