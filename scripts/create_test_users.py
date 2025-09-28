# scripts/create_test_users.py
import requests
import random

BASE_URL = "http://127.0.0.1:8000/api/users/auth/signup/"

roles = ["buyer", "seller", "designer", "artist", "admin"]

def create_user(i):
    data = {
        "username": f"testuser{i}",
        "email": f"user{i}@example.com",
        "first_name": f"First{i}",
        "last_name": f"Last{i}",
        "role": random.choice(roles),
        "avatar": "https://picsum.photos/200",
        "country": "Eth",
        "bio": f"Bio for user {i}"
    }
    r = requests.post(BASE_URL, json=data)
    print(r.status_code, r.json())

if __name__ == "__main__":
    for i in range(1, 6):  # generate 5 test users
        create_user(i)
