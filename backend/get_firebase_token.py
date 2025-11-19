#!/usr/bin/env python3
import requests
import json
import sys

FIREBASE_API_KEY = "AIzaSyDt2G9w9TGDAQg-LBTM5d-9tFQlZ8iF0MI"  # Replace with your key

def register_user(email, password):
    """Register a new user and get token"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['idToken']
    else:
        print(f"Error: {response.text}")
        return None

def login_user(email, password):
    """Login existing user and get token"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    
    data = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['idToken']
    else:
        print(f"Error: {response.text}")
        return None

if __name__ == "__main__":
    if FIREBASE_API_KEY == "YOUR_FIREBASE_API_KEY":
        print("ERROR: Please set FIREBASE_API_KEY in the script")
        sys.exit(1)
    
    email = "testuser1@example.com"
    password = "Test123456"
    
    print("Attempting to register user...")
    token = register_user(email, password)
    
    if not token:
        print("\nUser might already exist. Trying to login...")
        token = login_user(email, password)
    
    if token:
        print("\n" + "="*60)
        print("SUCCESS! Your Firebase Token:")
        print("="*60)
        print(token)
        print("="*60)
        print("\nUse it like this:")
        print(f'export FIREBASE_TOKEN="{token}"')
        print("\nOr in your curl command:")
        print(f'curl -H "Authorization: Bearer {token}" http://localhost:8004/api/alerts/')
    else:
        print("\nFailed to get token")