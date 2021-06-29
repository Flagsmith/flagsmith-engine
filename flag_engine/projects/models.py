import typing
from dataclasses import dataclass, field

from flag_engine.segments.models import Segment


@dataclass
class Project:
    id: int
    name: str
    segments: typing.List[Segment] = field(default_factory=list)
