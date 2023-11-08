from flag_engine.organisations.models import OrganisationModel


def test_unique_slug_property() -> None:
    # Given
    org_id = 1
    org_name = "test"
    org_model = OrganisationModel(
        id=org_id,
        name=org_name,
        feature_analytics=False,
        stop_serving_flags=False,
        persist_trait_data=False,
    )

    # Then
    assert org_model.unique_slug == f"{org_id}-{org_name}"
