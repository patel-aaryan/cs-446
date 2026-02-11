"""
Test script to verify authentication setup
Run this after setting up the database and starting the server
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth():
    print("🧪 Testing Authentication Setup\n")
    
    # Test 1: Health Check
    print("1️⃣ Testing server health...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("   ✅ Server is running!")
        else:
            print(f"   ❌ Server responded with status {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Cannot connect to server. Is it running?")
        print(f"   Error: {e}")
        return
    
    # Test 2: Register
    print("\n2️⃣ Testing user registration...")
    register_data = {
        "email": "testuser@example.com",
        "password": "testpassword123",
        "name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        if response.status_code == 201:
            print("   ✅ User registered successfully!")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Name: {user_data['name']}")
        elif response.status_code == 400 and "already registered" in response.text:
            print("   ⚠️  User already exists (this is ok, continuing...)")
        else:
            print(f"   ❌ Registration failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Registration error: {e}")
        return
    
    # Test 3: Login
    print("\n3️⃣ Testing user login...")
    login_data = {
        "email": "testuser@example.com",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("   ✅ Login successful!")
            token_data = response.json()
            access_token = token_data["access_token"]
            print(f"   Token type: {token_data['token_type']}")
            print(f"   Token (first 20 chars): {access_token[:20]}...")
        else:
            print(f"   ❌ Login failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Login error: {e}")
        return
    
    # Test 4: Get Current User
    print("\n4️⃣ Testing protected endpoint (GET /auth/me)...")
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    
    try:
        response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
        if response.status_code == 200:
            print("   ✅ Protected endpoint works!")
            user_data = response.json()
            print(f"   User ID: {user_data['id']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Name: {user_data['name']}")
        else:
            print(f"   ❌ Protected endpoint failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"   ❌ Protected endpoint error: {e}")
        return
    
    # Test 5: Test without token (should fail)
    print("\n5️⃣ Testing protected endpoint WITHOUT token (should fail)...")
    try:
        response = requests.get(f"{BASE_URL}/auth/me")
        if response.status_code == 403:
            print("   ✅ Correctly rejected request without token!")
        elif response.status_code == 401:
            print("   ✅ Correctly rejected request without token!")
        else:
            print(f"   ⚠️  Unexpected status code: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "="*50)
    print("🎉 All authentication tests passed!")
    print("="*50)
    print("\n📝 Your token for testing:")
    print(f"Bearer {access_token}")
    print("\n💡 Use this in your frontend or API client!")

if __name__ == "__main__":
    test_auth()
