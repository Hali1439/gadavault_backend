# apps/users/tests/test_api.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class UsersAPITest(APITestCase):
    def setUp(self):
        self.base = "/api/users"
        self.signup_url = f"{self.base}/signup/"
        self.token_url = f"{self.base}/token/"
        self.contact_url = f"{self.base}/contact/"
        self.users_url = f"{self.base}/"  # viewset list (protected)

    def test_signup_returns_tokens_and_user(self):
        payload = {"email": "t1@example.com", "password": "Secret123!", "name": "T1"}
        resp = self.client.post(self.signup_url, payload, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED, resp.data)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)
        self.assertIn("user", resp.data)
        # Confirm user exists and password works
        user = User.objects.get(email="t1@example.com")
        self.assertTrue(user.check_password("Secret123!"))

    def test_login_obtain_tokens(self):
        # Create a user via signup endpoint to match how your backend creates users
        signup = self.client.post(self.signup_url, {"email":"t2@example.com","password":"Secret123!","name":"T2"}, format="json")
        self.assertEqual(signup.status_code, status.HTTP_201_CREATED, signup.data)
        # Now obtain tokens using token endpoint
        resp = self.client.post(self.token_url, {"email":"t2@example.com","password":"Secret123!"}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK, resp.data)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)

    def test_contact_is_public(self):
        payload = {"name":"Visitor","email":"vis@example.com","message":"Hello from tests"}
        resp = self.client.post(self.contact_url, payload, format="json")
        self.assertIn(resp.status_code, (status.HTTP_201_CREATED, status.HTTP_200_OK))
        # optionally: check Contact model count if available

    def test_protected_endpoint_requires_auth_and_allows_with_token(self):
        # Without token -> 401/403
        resp = self.client.get(self.users_url)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))
        # Create and sign in
        signup = self.client.post(self.signup_url, {"email":"t3@example.com","password":"Secret123!","name":"T3"}, format="json")
        token = signup.data["access"]
        # Set header and retry
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        resp2 = self.client.get(self.users_url)
        self.assertEqual(resp2.status_code, status.HTTP_200_OK, resp2.data)
