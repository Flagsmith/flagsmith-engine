def is_semver(value: str) -> bool:
    """
    Checks if the given string have `:semver` suffix or not
    >>> is_semver("2.1.41-beta:semver")
    True
    >>> is_semver("2.1.41-beta")
    False
    """

    return value[-7:] == ":semver"


def remove_semver_suffix(value: str) -> str:
    """
    Remove the semver suffix(i.e: last 7 characters) from the given value
    >>> remove_semver_suffix("2.1.41-beta:semver")
    '2.1.41-beta'
    >>> remove_semver_suffix("2.1.41:semver")
    '2.1.41'
    """
    return value[:-7]
