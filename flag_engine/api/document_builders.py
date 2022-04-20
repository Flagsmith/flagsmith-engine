from flag_engine.api.schemas import (
    DjangoEnvironmentAPIKeySchema,
    DjangoEnvironmentSchema,
    DjangoIdentitySchema,
)

django_environment_schema = DjangoEnvironmentSchema()
django_identity_schema = DjangoIdentitySchema()

django_environment_api_key_schema = DjangoEnvironmentAPIKeySchema()


def build_environment_document(django_environment) -> dict:
    return django_environment_schema.dump(django_environment)


def build_identity_document(django_identity) -> dict:
    return django_identity_schema.dump(django_identity)


def build_environment_api_key_document(django_environment_api_key) -> dict:
    return django_environment_api_key_schema.dump(django_environment_api_key)
