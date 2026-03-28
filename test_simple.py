#!/usr/bin/env python
"""Simple registration test"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriconnect.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test():
    client = Client()
    
    # Test farmer registration
    print("\n" + "="*60)
    print("Testing Farmer Registration")
    print("="*60)
    
    farmer_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john@farm.com',
        'phone': '1234567890',
        'location': 'California',
        'password1': 'Test@1234',
        'password2': 'Test@1234',
    }
    
    print("1. Registering farmer...")
    response = client.post('/register/farmer/', farmer_data, follow=False)
    
    print(f"   Status: {response.status_code}")
    print(f"   Redirect URL: {response.get('Location', 'No redirect')}")
    
    user = User.objects.filter(email='john@farm.com').first()
    if user:
        print(f"   ✓ User created: {user.email}")
        print(f"   ✓ Is farmer: {user.is_farmer()}")
    else:
        print("   ✗ User NOT created")
        return
    
    # Test that messages were set
    print("\n2. Testing form error handling (duplicate email)...")
    response = client.post('/register/farmer/', {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'john@farm.com',  # Duplicate
        'phone': '9876543210',
        'location': 'Texas',
        'password1': 'Test@1234',
        'password2': 'Test@1234',
    }, follow=False)
    
    print(f"   Status: {response.status_code}")
    messages = list(response.context.get('messages', [])) if response.context else []
    print(f"   Messages: {len(messages)}")
    for msg in messages:
        print(f"     - {msg.level_tag}: {msg.message}")
    
    # Test login
    print("\n3. Testing login...")
    client2 = Client()  # New client to test login
    login_response = client2.post('/login/', {
        'email': 'john@farm.com',
        'password': 'Test@1234',
        'role': 'farmer'
    }, follow=True)
    
    print(f"   Login status: {login_response.status_code}")
    print(f"   User authenticated: {login_response.wsgi_request.user.is_authenticated}")
    
    if login_response.wsgi_request.user.is_authenticated:
        print(f"   ✓ Successfully logged in as: {login_response.wsgi_request.user.email}")
    
    # Cleanup
    User.objects.filter(email='john@farm.com').delete()
    print("\n✓ Test complete - user deleted")

if __name__ == '__main__':
    try:
        test()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
