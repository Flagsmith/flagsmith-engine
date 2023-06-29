from pydantic import BaseModel


class OrganisationModel(BaseModel):
    id: int
    name: str
    feature_analytics: bool
    stop_serving_flags: bool
    persist_trait_data: bool

    @property
    def unique_slug(self):
        return str(self.id) + "-" + self.name
