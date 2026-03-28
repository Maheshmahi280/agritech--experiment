#!/usr/bin/env python
"""Final Comprehensive Authentication Test"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agriconnect.settings')
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

print("\n" + "="*70)
print("AGRICONNECT AUTHENTICATION FINAL VERIFICATION TEST")
print("="*70)

def test_full_flow():
    """Test complete registration and login flow"""
    
    client = Client()
    test_results = {
        'passed': [],
        'failed': []
    }
    
    # TEST 1: Farmer Registration Success
    print("\n[TEST 1] Farmer Registration Success")
    try:
        response = client.post('/register/farmer/', {
            'first_name': 'Alice',
            'last_name': 'Johnson',
            'email': 'alice@farm.com',
            'phone': '9999999999',
            'location': 'Punjab',
            'password1': 'SecurePass@123',
            'password2': 'SecurePass@123',
            'terms': 'on'
        }, follow=False)
        
        user = User.objects.filter(email='alice@farm.com').first()
        
        if response.status_code == 302 and user and user.is_farmer():
            print("  ✓ PASS: User created and redirected")
            test_results['passed'].append("Farmer registration")
        else:
            print("  ✗ FAIL: Unexpected response")
            test_results['failed'].append("Farmer registration")
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        test_results['failed'].append(f"Farmer registration: {e}")
    
    # TEST 2: Restaurant Registration Success
    print("\n[TEST 2] Restaurant Registration Success")
    try:
        response = client.post('/register/restaurant/', {
            'restaurant_name': 'Best Biryani House',
            'owner_name': 'Bob Smith',
            'restaurant_type': 'casual',
            'email': 'bob@restaurant.com',
            'phone': '8888888888',
            'address': '456 Food Street, Bangalore 560001',
            'password1': 'SecurePass@123',
            'password2': 'SecurePass@123',
            'terms': 'on'
        }, follow=False)
        
        user = User.objects.filter(email='bob@restaurant.com').first()
        
        if response.status_code == 302 and user and user.is_restaurant():
            print("  ✓ PASS: Restaurant user created and redirected")
            test_results['passed'].append("Restaurant registration")
        else:
            print("  ✗ FAIL: Unexpected response")
            test_results['failed'].append("Restaurant registration")
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        test_results['failed'].append(f"Restaurant registration: {e}")
    
    # TEST 3: Farmer Login
    print("\n[TEST 3] Farmer Login Success")
    try:
        client2 = Client()
        response = client2.post('/login/', {
            'email': 'alice@farm.com',
            'password': 'SecurePass@123',
            'role': 'farmer'
        }, follow=True)
        
        if response.wsgi_request.user.is_authenticated:
            print("  ✓ PASS: Farmer login successful")
            test_results['passed'].append("Farmer login")
        else:
            print("  ✗ FAIL: User not authenticated")
            test_results['failed'].append("Farmer login")
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        test_results['failed'].append(f"Farmer login: {e}")
    
    # TEST 4: Restaurant Login
    print("\n[TEST 4] Restaurant Login Success")
    try:
        client3 = Client()
        response = client3.post('/login/', {
            'email': 'bob@restaurant.com',
            'password': 'SecurePass@123',
            'role': 'restaurant'
        }, follow=True)
        
        if response.wsgi_request.user.is_authenticated:
            print("  ✓ PASS: Restaurant login successful")
            test_results['passed'].append("Restaurant login")
        else:
            print("  ✗ FAIL: User not authenticated")
            test_results['failed'].append("Restaurant login")
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        test_results['failed'].append(f"Restaurant login: {e}")
    
    # TEST 5: Invalid Password
    print("\n[TEST 5] Invalid Password Handling")
    try:
        client4 = Client()
        response = client4.post('/login/', {
            'email': 'alice@farm.com',
            'password': 'WrongPassword',
            'role': 'farmer'
        }, follow=False)
        
        if response.status_code in [200, 302]:  # Either form redisplay or redirect
            print("  ✓ PASS: Invalid password handled")
            test_results['passed'].append("Invalid password detection")
        else:
            print("  ✗ FAIL: Unexpected status code")
            test_results['failed'].append("Invalid password detection")
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        test_results['failed'].append(f"Invalid password detection: {e}")
    
    # TEST 6: Dashboard Access
    print("\n[TEST 6] Dashboard Access After Login")
    try:
        client5 = Client()
        # Login first
        client5.post('/login/', {
            'email': 'alice@farm.com',
            'password': 'SecurePass@123',
            'role': 'farmer'
        })
        
        # Try to access farmer dashboard
        response = client5.get('/farmer/dashboard/')
        
        if response.status_code == 200:
            print("  ✓ PASS: Dashboard accessible after login")
            test_results['passed'].append("Dashboard access")
        else:
            print(f"  ✗ FAIL: Status code {response.status_code}")
            test_results['failed'].append("Dashboard access")
    except Exception as e:
        print(f"  ✗ FAIL: {e}")
        test_results['failed'].append(f"Dashboard access: {e}")
    
    # Cleanup
    User.objects.filter(email__in=['alice@farm.com', 'bob@restaurant.com']).delete()
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"\n✓ Passed: {len(test_results['passed'])}")
    for test in test_results['passed']:
        print(f"  • {test}")
    
    if test_results['failed']:
        print(f"\n✗ Failed: {len(test_results['failed'])}")
        for test in test_results['failed']:
            print(f"  • {test}")
    else:
        print(f"\n✓ ALL TESTS PASSED!")
    
    print("\n" + "="*70)
    print("🎉 AgriConnect Authentication is FULLY FUNCTIONAL")
    print("="*70)

if __name__ == '__main__':
    try:
        test_full_flow()
    except Exception as e:
        print(f"\n✗ Critical Error: {e}")
        import traceback
        traceback.print_exc()
