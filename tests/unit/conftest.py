from datetime import datetime

import pytest

from flag_engine.environments.models import EnvironmentModel
from flag_engine.features.constants import STANDARD
from flag_engine.features.models import (
    FeatureModel,
    FeatureStateModel,
    MultivariateFeatureOptionModel,
    MultivariateFeatureStateValueModel,
)
from flag_engine.identities.models import IdentityModel
from flag_engine.identities.traits.models import TraitModel
from flag_engine.organisations.models import OrganisationModel
from flag_engine.projects.models import ProjectModel
from flag_engine.segments import constants
from flag_engine.segments.models import (
    SegmentConditionModel,
    SegmentModel,
    SegmentRuleModel,
)


@pytest.fixture()
def segment_condition_property() -> str:
    return "foo"


@pytest.fixture()
def segment_condition_string_value() -> str:
    return "bar"


@pytest.fixture()
def segment_condition(
    segment_condition_property: str,
    segment_condition_string_value: str,
) -> SegmentConditionModel:
    return SegmentConditionModel(
        operator=constants.EQUAL,
        property_=segment_condition_property,
        value=segment_condition_string_value,
    )


@pytest.fixture()
def segment_rule(segment_condition: SegmentConditionModel) -> SegmentRuleModel:
    return SegmentRuleModel(type=constants.ALL_RULE, conditions=[segment_condition])


@pytest.fixture()
def segment(segment_rule: SegmentRuleModel) -> SegmentModel:
    return SegmentModel(id=1, name="my_segment", rules=[segment_rule])


@pytest.fixture()
def organisation() -> OrganisationModel:
    return OrganisationModel(
        id=1,
        name="test Org",
        stop_serving_flags=False,
        persist_trait_data=True,
        feature_analytics=True,
    )


@pytest.fixture()
def project(
    organisation: OrganisationModel,
    segment: SegmentModel,
) -> ProjectModel:
    return ProjectModel(
        id=1,
        name="Test Project",
        organisation=organisation,
        hide_disabled_flags=False,
        segments=[segment],
    )


@pytest.fixture()
def feature_1() -> FeatureModel:
    return FeatureModel(id=1, name="feature_1", type=STANDARD)


@pytest.fixture()
def feature_2() -> FeatureModel:
    return FeatureModel(id=2, name="feature_2", type=STANDARD)


@pytest.fixture()
def feature_state_1(feature_1: FeatureModel) -> FeatureStateModel:
    return FeatureStateModel(feature=feature_1, enabled=True)


@pytest.fixture()
def feature_state_2(feature_2: FeatureModel) -> FeatureStateModel:
    return FeatureStateModel(feature=feature_2, enabled=True)


@pytest.fixture()
def environment(
    feature_1: FeatureModel,
    feature_2: FeatureModel,
    project: ProjectModel,
) -> EnvironmentModel:
    return EnvironmentModel(
        id=1,
        api_key="api-key",
        project=project,
        feature_states=[
            FeatureStateModel(django_id=1, feature=feature_1, enabled=True),
            FeatureStateModel(django_id=2, feature=feature_2, enabled=False),
        ],
    )


@pytest.fixture()
def identity(environment: EnvironmentModel) -> IdentityModel:
    return IdentityModel(
        identifier="identity_1",
        environment_api_key=environment.api_key,
        created_date=datetime.now(),
    )


@pytest.fixture()
def trait_matching_segment(segment_condition: SegmentConditionModel) -> TraitModel:
    return TraitModel(
        trait_key=segment_condition.property_,
        trait_value=segment_condition.value,
    )


@pytest.fixture()
def identity_in_segment(
    trait_matching_segment: TraitModel,
    environment: EnvironmentModel,
) -> IdentityModel:
    return IdentityModel(
        identifier="identity_2",
        environment_api_key=environment.api_key,
        identity_traits=[trait_matching_segment],
    )


@pytest.fixture()
def segment_override_fs(
    segment: SegmentModel,
    feature_1: FeatureModel,
) -> FeatureStateModel:
    fs = FeatureStateModel(
        django_id=4,
        feature=feature_1,
        enabled=False,
    )
    fs.set_value("segment_override")
    return fs


@pytest.fixture()
def mv_feature_state_value() -> MultivariateFeatureStateValueModel:
    return MultivariateFeatureStateValueModel(
        id=1,
        multivariate_feature_option=MultivariateFeatureOptionModel(
            id=1, value="test_value"
        ),
        percentage_allocation=100,
    )


@pytest.fixture()
def environment_with_segment_override(
    environment: EnvironmentModel,
    segment_override_fs: FeatureStateModel,
    segment: SegmentModel,
) -> EnvironmentModel:
    segment.feature_states.append(segment_override_fs)
    environment.project.segments.append(segment)
    return environment
