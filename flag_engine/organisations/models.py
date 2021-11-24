from dataclasses import dataclass


@dataclass
class OrganisationModel:
    id: int
    name: str
    feature_analytics: bool
    stop_serving_flags: bool
    persist_trait_data: bool

    def get_unique_slug(self):
        return str(self.id) + "-" + self.name
