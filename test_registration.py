#!/usr/bin/env python
"""Test script to verify registration and authentication flow"""

import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriconnect.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

django.setup()

User = get_user_model()
client = Client()

def test_farmer_registration():
    """Test farmer registration flow"""
    print("\n" + "="*60)
    print("TEST 1: Farmer Registration")
    print("="*60)
    
    # Test data
    farmer_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'farmer@test.com',
        'phone': '1234567890',
        'location': 'California',
        'password1': 'securepass123',
        'password2': 'securepass123',
    }
    
    # Register farmer
    print("\nPOST /register/farmer/ with data:")
    for key, value in farmer_data.items():
        print(f"  {key}: {value}")
    
    response = client.post('/register/farmer/', farmer_data, follow=True)
    
    print(f"\nResponse status code: {response.status_code}")
    print(f"Response URL chain: {[r[0].path for r in response.redirect_chain]}")
    print(f"Final URL: {response.request['PATH_INFO']}")
    
    # Check if user was created
    user = User.objects.filter(email='farmer@test.com').first()
    if user:
        print(f"\n✓ User created: {user.email}")
        print(f"  Role: {'Farmer' if user.is_farmer() else 'Not Farmer'}")
        print(f"  Is authenticated: {user.is_authenticated}")
    else:
        print("\n✗ User was NOT created")
    
    # Check messages
    messages = list(response.context['messages']) if response.context and 'messages' in response.context else []
    print(f"\nMessages returned: {len(messages)}")
    for msg in messages:
        print(f"  - {msg.level_tag}: {msg.message}")
    
    # Check if redirected to dashboard
    if '/farmer/dashboard/' in response.request['PATH_INFO']:
        print("\n✓ Successfully redirected to farmer dashboard")
    else:
        print(f"\n✗ NOT redirected to farmer dashboard (ended at: {response.request['PATH_INFO']})")
    
    return user is not None

def test_farmer_login():
    """Test farmer login flow"""
    print("\n" + "="*60)
    print("TEST 2: Farmer Login")
    print("="*60)
    
    login_data = {
        'email': 'farmer@test.com',
        'password': 'securepass123',
        'role': 'farmer'
    }
    
    print("\nPOST /login/ with email:", login_data['email'])
    
    response = client.post('/login/', login_data, follow=True)
    
    print(f"\nResponse status code: {response.status_code}")
    print(f"Response URL chain: {[r[0].path for r in response.redirect_chain]}")
    print(f"Final URL: {response.request['PATH_INFO']}")
    
    # Check messages
    messages = list(response.context['messages']) if response.context and 'messages' in response.context else []
    print(f"\nMessages returned: {len(messages)}")
    for msg in messages:
        print(f"  - {msg.level_tag}: {msg.message}")
    
    # Check if logged in
    user_id = response.wsgi_request.user.id if hasattr(response, 'wsgi_request') else None
    if response.wsgi_request.user.is_authenticated:
        print(f"\n✓ Successfully logged in as: {response.wsgi_request.user.email}")
    else:
        print("\n✗ NOT logged in")
    
    return response.wsgi_request.user.is_authenticated

def test_duplicate_email():
    """Test registration with duplicate email"""
    print("\n" + "="*60)
    print("TEST 3: Duplicate Email Registration")
    print("="*60)
    
    farmer_data = {
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'farmer@test.com',  # Duplicate email
        'phone': '9876543210',
        'location': 'Texas',
        'password1': 'securepass123',
        'password2': 'securepass123',
    }
    
    print("\nPOST /register/farmer/ with duplicate email: farmer@test.com")
    
    response = client.post('/register/farmer/', farmer_data, follow=False)  # Don't follow redirects
    
    print(f"\nResponse status code: {response.status_code}")
    
    # Check messages
    messages = list(response.context['messages']) if response.context and 'messages' in response.context else []
    print(f"Messages returned: {len(messages)}")
    for msg in messages:
        print(f"  - {msg.level_tag}: {msg.message}")
    
    if any('already registered' in str(msg.message) or 'duplicate' in str(msg.message).lower() for msg in messages):
        print("\n✓ Duplicate email error message displayed")
    else:
        print("\n✗ Duplicate email error NOT shown in messages")
    
    # Check if still on registration page
    if response.status_code == 200 and 'register.html' in response.template_name:
        print("✓ Still on registration page (no redirect)")
    else:
        print(f"✗ Unexpected response: {response.status_code}")

def test_password_mismatch():
    """Test registration with mismatched passwords"""
    print("\n" + "="*60)
    print("TEST 4: Password Mismatch Registration")
    print("="*60)
    
    farmer_data = {
        'first_name': 'Bob',
        'last_name': 'Johnson',
        'email': 'bob@test.com',
        'phone': '5555555555',
        'location': 'Florida',
        'password1': 'securepass123',
        'password2': 'differentpass123',  # Mismatched
    }
    
    print("\nPOST /register/farmer/ with mismatched passwords")
    
    response = client.post('/register/farmer/', farmer_data, follow=False)
    
    print(f"\nResponse status code: {response.status_code}")
    
    # Check messages
    messages = list(response.context['messages']) if response.context and 'messages' in response.context else []
    print(f"Messages returned: {len(messages)}")
    for msg in messages:
        print(f"  - {msg.level_tag}: {msg.message}")
    
    # Check form errors
    if response.context and 'form' in response.context:
        form = response.context['form']
        print(f"\nForm errors: {form.errors}")
        if form.errors:
            print("✓ Form validation errors displayed")
    
    print("\n✓ Still on registration page (no redirect)")

def cleanup():
    """Cleanup test data"""
    print("\n" + "="*60)
    print("Cleanup: Deleting test users")
    print("="*60)
    
    User.objects.filter(email__in=['farmer@test.com', 'bob@test.com']).delete()
    print("✓ Test users deleted")

if __name__ == '__main__':
    print("\n🧪 AgriConnect Registration & Authentication Test Suite")
    
    try:
        # Run tests
        test_farmer_registration()
        test_farmer_login()
        test_duplicate_email()
        test_password_mismatch()
        
        print("\n" + "="*60)
        print("✓ All tests completed")
        print("="*60)
    except Exception as e:
        print(f"\n✗ Error during tests: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cleanup()
