import typing
from dataclasses import dataclass, field

from flag_engine.organisations.models import OrganisationModel
from flag_engine.segments.models import SegmentModel


@dataclass
class ProjectModel:
    id: int
    name: str
    organisation: OrganisationModel
    hide_disabled_flags: bool
    segments: typing.List[SegmentModel] = field(default_factory=list)
    enable_realtime_updates: bool = False
    server_key_only_feature_ids: typing.List[int] = field(default_factory=list)
