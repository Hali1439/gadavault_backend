# scripts/smoke_test_api.py
import requests, sys

BASE = "http://127.0.0.1:8000/api"
def pretty(r):
    print("STATUS:", r.status_code)
    try:
        print("JSON:", r.json())
    except:
        print("TEXT:", r.text)

def signup(email="smoke2@example.com"):
    r = requests.post(f"{BASE}/users/signup/", json={"email":email,"password":"Passw0rd!","name":"Smoke"})
    pretty(r)
    return r

def login(email="smoke2@example.com"):
    r = requests.post(f"{BASE}/users/token/", json={"email":email,"password":"Passw0rd!"})
    pretty(r)
    return r

def contact():
    r = requests.post(f"{BASE}/users/contact/", json={"name":"X","email":"x@example.com","message":"hi"})
    pretty(r)
    return r

def protected(access_token):
    r = requests.get(f"{BASE}/users/", headers={"Authorization":f"Bearer {access_token}"})
    pretty(r)
    return r

if __name__ == "__main__":
    s = signup()
    if s.status_code in (201,200) and "access" in s.json():
        tok = s.json()["access"]
    else:
        l = login()
        tok = l.json().get("access")
    contact()
    if tok:
        protected(tok)
    else:
        print("No token available — check signup/login output")
