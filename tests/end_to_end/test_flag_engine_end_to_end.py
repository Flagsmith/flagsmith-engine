from datetime import datetime

from flag_engine.api.document_builders import (
    build_environment_document,
    build_identity_document,
)
from flag_engine.engine import (
    get_environment_feature_states,
    get_identity_feature_states,
)
from flag_engine.environments.builders import build_environment_model
from flag_engine.features.models import FlagsmithValue
from flag_engine.identities.builders import build_identity_dict, build_identity_model
from flag_engine.identities.traits.models import TraitModel
from tests.mock_django_classes import DjangoFeatureState, DjangoIdentity


def test_environment_end_to_end(mock_django_environment):
    # First, we need to dump the environment as if we were sending it to DynamoDB
    environment_dict = build_environment_document(mock_django_environment)
    assert environment_dict

    # Then we should be able to load that data again as if we were grabbing the
    # environment from dynamodb in the lambda edge functions
    environment_model = build_environment_model(environment_dict)
    assert environment_model

    # Finally, we should be able to get the flags for this environment
    feature_states = get_environment_feature_states(environment_model)
    # and the feature states should be correct
    assert len(feature_states) == 1
    assert feature_states[0].enabled is True
    assert feature_states[0].get_value() == FlagsmithValue(value="foobar")


def test_identity_end_to_end(mock_django_environment, mock_django_feature):
    # First, let's define the identity and overwrite a feature
    identity_feature_state_value = "overridden for identity"
    django_identity = DjangoIdentity(
        id=1,
        identifier="identity",
        created_date=datetime.now(),
        environment=mock_django_environment,
        feature_states=[
            DjangoFeatureState(
                id=3,
                feature=mock_django_feature,
                enabled=True,
                value=identity_feature_state_value,
            )
        ],
    )

    # Now let's dump the identity as if we're sending it to dynamo from the django
    # application
    identity_data_from_django = build_identity_document(django_identity)
    assert identity_data_from_django

    # Then, let's check we can load it from this data to simulate loading it from dynamo
    # in the lambda functions
    identity_model = build_identity_model(identity_data_from_django)
    assert identity_model

    # Then, since the lambda functions also write back to dynamo, let's add a trait and
    # simulate dumping back to dynamo to make sure the builder function also works on
    # the identity model
    identity_model.identity_traits.append(
        TraitModel(trait_key="foo", trait_value="bar")
    )
    identity_data_from_engine = build_identity_dict(identity_model)
    assert identity_data_from_engine

    # Finally, let's check that we can get the feature states for the identity and that
    # they are correct
    environment_model = build_environment_model(
        build_environment_document(mock_django_environment)
    )
    feature_states = get_identity_feature_states(
        environment=environment_model, identity=identity_model
    )
    assert feature_states
    assert len(feature_states) == 1
    assert feature_states[0].get_value() == FlagsmithValue(
        value=identity_feature_state_value
    )
