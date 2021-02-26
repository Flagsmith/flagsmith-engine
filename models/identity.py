from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class Trait():
    key: str
    value: str


@dataclass
class Identity():
    identifier: str
    environment_api_key:str 
    created_date: date
    environment_id: int
    traits: List[Trait]

