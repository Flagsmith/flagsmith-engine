import random
import string

import pytest


@pytest.fixture()
def random_api_key():
    return "".join([random.choice(string.ascii_letters) for _ in range(20)])
