from dataclasses import dataclass


@dataclass
class IntegrationModel:
    api_key: str = None
    base_url: str = None
    entity_selector: str = None
