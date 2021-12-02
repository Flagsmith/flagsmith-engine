from flag_engine.environments.schemas import EnvironmentSchema


def test_environment_schema_dump_sets_api_key_in_context(django_environment):
    # Given
    schema = EnvironmentSchema()

    # When
    environment_data = schema.dump(django_environment)

    # Then
    assert environment_data
    assert schema.context.get("environment_api_key") == django_environment.api_key
