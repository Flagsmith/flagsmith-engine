import datetime
import typing
import uuid

from pydantic import UUID4, BaseModel, Field, root_validator
from pydantic_collections import BaseCollectionModel

from flag_engine.features.models import FeatureStateModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.utils.datetime import utcnow_with_tz
from flag_engine.utils.exceptions import DuplicateFeatureState


class IdentityFeaturesList(BaseCollectionModel[FeatureStateModel]):
    # TODO @khvn26 Consider dropping pydantic_collections in favour of a `list`/`set`
    #      subclass after upgrading to Pydantic V2
    #      or not use custom collections at all and move their validation/interfaces
    #      to the parent model
    #      https://github.com/Flagsmith/flagsmith-engine/issues/172
    @classmethod
    def __get_validators__(
        cls,
    ) -> typing.Generator[typing.Callable[..., typing.Any], None, None]:
        yield cls.validate
        yield cls._ensure_unique_feature_ids

    @staticmethod
    def _ensure_unique_feature_ids(
        value: "IdentityFeaturesList",
    ) -> "IdentityFeaturesList":
        for i, feature_state in enumerate(value, start=1):
            if feature_state.feature.id in [
                feature_state.feature.id for feature_state in value[i:]
            ]:
                raise DuplicateFeatureState(
                    f"Feature state for feature id={feature_state.feature.id} already exists"
                )
        return value

    def append(self, feature_state: "FeatureStateModel") -> None:
        self._ensure_unique_feature_ids([*self, feature_state])
        super().append(feature_state)


class IdentityModel(BaseModel):
    identifier: str
    environment_api_key: str
    created_date: datetime.datetime = Field(default_factory=utcnow_with_tz)
    identity_features: IdentityFeaturesList = Field(
        default_factory=IdentityFeaturesList
    )
    identity_traits: typing.List[TraitModel] = Field(default_factory=list)
    identity_uuid: UUID4 = Field(default_factory=uuid.uuid4)
    django_id: typing.Optional[int] = None
    composite_key: str = Field(default_factory=lambda: None)

    # TODO @khvn26 Migrate to @computed_field https://github.com/Flagsmith/flagsmith-engine/issues/172
    @root_validator(skip_on_failure=True)
    def _generate_default_composite_key(
        cls,
        values: typing.Dict[str, typing.Any],
    ) -> typing.Dict[str, typing.Any]:
        if not values.get("composite_key"):
            values["composite_key"] = cls.generate_composite_key(
                values["environment_api_key"],
                values["identifier"],
            )
        return values

    @staticmethod
    def generate_composite_key(env_key: str, identifier: str) -> str:
        return f"{env_key}_{identifier}"

    def get_hash_key(self, use_identity_composite_key_for_hashing: bool) -> str:
        return (
            self.composite_key
            if use_identity_composite_key_for_hashing
            else self.identifier
        )

    def update_traits(
        self, traits: typing.List[TraitModel]
    ) -> typing.Tuple[typing.List[TraitModel], bool]:
        existing_traits = {trait.trait_key: trait for trait in self.identity_traits}
        traits_changed = False

        for trait in traits:
            existing_trait = existing_traits.get(trait.trait_key)

            if trait.trait_value is None and existing_trait:
                existing_traits.pop(trait.trait_key)
                traits_changed = True

            elif getattr(existing_trait, "trait_value", None) != trait.trait_value:
                existing_traits[trait.trait_key] = trait
                traits_changed = True

        self.identity_traits = list(existing_traits.values())
        return self.identity_traits, traits_changed

    def prune_features(self, valid_feature_names: typing.List[str]) -> None:
        self.identity_features = IdentityFeaturesList(
            [
                fs
                for fs in self.identity_features
                if fs.feature.name in valid_feature_names
            ]
        )
