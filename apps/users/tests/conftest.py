import pytest
from rest_framework.test import APIClient

@pytest.fixture
def client():
    """Shortcut fixture for DRF's APIClient."""
    return APIClient()
