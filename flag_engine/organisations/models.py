from dataclasses import dataclass


@dataclass
class OrganisationModel:
    name: str
    id: int
    feature_analytics: bool
    stop_serving_flags: bool
    persist_trait_data: bool
