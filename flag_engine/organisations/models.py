from dataclasses import dataclass


@dataclass
class OrganisationModel:
    feature_analytics: bool
    stop_serving_flags: bool
    persist_trait_data: bool
