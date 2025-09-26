# apps/users/tests/test_api.py
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_signup_and_login():
    client = APIClient()

    # --- SIGNUP ---
    signup_data = {
        "email": "testuser@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    resp = client.post("/api/users/auth/signup/", signup_data, format="json")
    assert resp.status_code == 201
    tokens = resp.data
    assert "access" in tokens
    assert "refresh" in tokens

    # --- LOGIN (token) ---
    login_data = {"username": signup_data["email"], "password": "password123"}
    resp = client.post("/api/users/auth/token/", login_data, format="json")
    assert resp.status_code == 200
    assert "access" in resp.data

@pytest.mark.django_db
def test_signup_alias():
    client = APIClient()

    # --- SIGNUP via alias ---
    signup_data = {
        "email": "testuser2@example.com",
        "password": "password123",
        "first_name": "Test",
        "last_name": "User"
    }
    resp = client.post("/api/users/signup/", signup_data, format="json")
    assert resp.status_code == 201
    tokens = resp.data
    assert "access" in tokens
    assert "refresh" in tokens
