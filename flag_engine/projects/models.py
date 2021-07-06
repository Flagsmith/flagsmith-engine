import typing
from dataclasses import dataclass, field

from flag_engine.segments.models import SegmentModel


@dataclass
class ProjectModel:
    id: int
    name: str
    segments: typing.List[SegmentModel] = field(default_factory=list)
