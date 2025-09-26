import os
import sys
import django
import requests
from decouple import config

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gada_vault.settings')
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

def create_test_user():
    """Create a test user if doesn't exist"""
    try:
        user, created = User.objects.get_or_create(
            username='smoketest',
            defaults={
                'email': 'smoke@test.com',
                'is_active': True
            }
        )
        if created:
            user.set_password('testpass123')
            user.save()
            print("Created test user: smoketest / testpass123")
        return user
    except Exception as e:
        print(f"Error creating test user: {e}")
        return None

def get_auth_token():
    """Get or create authentication token"""
    try:
        user = create_test_user()
        if not user:
            return None
            
        token, created = Token.objects.get_or_create(user=user)
        if created:
            print("Created new auth token")
        return token.key
    except Exception as e:
        print(f"Error getting auth token: {e}")
        return None

def get_jwt_token():
    """Get JWT token from API"""
    try:
        login_url = f"{BASE_URL}/api/token/"
        response = requests.post(login_url, json={
            'username': 'smoketest',
            'password': 'testpass123'
        })
        if response.status_code == 200:
            return response.json().get('access')
        else:
            print(f"JWT Login failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error getting JWT token: {e}")
        return None

def smoke_test():
    """Run smoke tests on API endpoints"""
    
    # Try to get authentication
    token = get_jwt_token()  # Try JWT first
    if not token:
        token = get_auth_token()  # Fallback to Token auth
    
    headers = {}
    if token:
        headers = {'Authorization': f'Bearer {token}'}  # JWT uses Bearer
        print(f"Using token: {token[:20]}...")
    else:
        print("No token available - testing public endpoints only")

    endpoints = [
        '/api/users/me/',
        '/api/products/',
        '/api/designers/',
    ]

    for endpoint in endpoints:
        try:
            url = f"{BASE_URL}{endpoint}"
            response = requests.get(url, headers=headers)
            print(f"\nENDPOINT: {endpoint}")
            print(f"STATUS: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS")
                data = response.json()
                if isinstance(data, list):
                    print(f"Retrieved {len(data)} items")
                elif isinstance(data, dict):
                    print(f"Keys: {list(data.keys())}")
            elif response.status_code == 401:
                print("❌ UNAUTHORIZED - Authentication required")
            elif response.status_code == 403:
                print("❌ FORBIDDEN - Insufficient permissions")
            elif response.status_code == 404:
                print("❌ NOT FOUND - Endpoint may not exist")
            else:
                print(f"Response: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ ERROR: {e}")

def test_authentication():
    """Test authentication endpoints"""
    print("\n" + "="*50)
    print("TESTING AUTHENTICATION ENDPOINTS")
    print("="*50)
    
    # Test token obtain endpoint
    try:
        token_url = f"{BASE_URL}/api/token/"
        response = requests.post(token_url, json={
            'username': 'smoketest',
            'password': 'testpass123'
        })
        print(f"\nToken Endpoint: {token_url}")
        print(f"STATUS: {response.status_code}")
        if response.status_code == 200:
            print("✅ Token authentication working")
            print(f"Token: {response.json().get('access', '')[:30]}...")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Token auth error: {e}")

if __name__ == '__main__':
    # Determine base URL
    BASE_URL = config('SMOKE_TEST_BASE_URL', default='http://localhost:8000')
    
    print("🚀 Starting API Smoke Tests")
    print(f"Target: {BASE_URL}")
    print("-" * 50)
    
    # Test authentication first
    test_authentication()
    
    # Run main smoke tests
    smoke_test()
    
    print("\n" + "="*50)
    print("Smoke tests completed!")
    print("="*50)