from flag_engine.django_transform.schemas import (
    DjangoEnvironmentSchema,
    DjangoIdentitySchema,
)

django_environment_schema = DjangoEnvironmentSchema()
django_identity_schema = DjangoIdentitySchema()


def build_environment_document(django_environment) -> dict:
    return django_environment_schema.dump(django_environment)


def build_identity_document(django_identity) -> dict:
    return django_identity_schema.dump(django_identity)
