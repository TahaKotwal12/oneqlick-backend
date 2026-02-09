"""
Rate Limiting Test Script for OneQlick Backend

This script tests the rate limiting functionality by sending multiple requests
to various endpoints and verifying that rate limits are enforced correctly.
"""

import requests
import time
from typing import Dict, List

# Base URL for the API
BASE_URL = "http://localhost:8000"

def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}\n")

def test_rate_limit(endpoint: str, method: str = "GET", data: Dict = None, 
                   expected_limit: int = 10, num_requests: int = 15) -> Dict:
    """
    Test rate limiting on a specific endpoint
    
    Args:
        endpoint: API endpoint to test
        method: HTTP method (GET or POST)
        data: Request body for POST requests
        expected_limit: Expected rate limit
        num_requests: Number of requests to send
    
    Returns:
        Dictionary with test results
    """
    print(f"Testing: {method} {endpoint}")
    print(f"Expected limit: {expected_limit} requests")
    print(f"Sending {num_requests} requests...")
    
    success_count = 0
    rate_limited_count = 0
    headers_found = False
    
    for i in range(1, num_requests + 1):
        try:
            if method == "POST":
                response = requests.post(f"{BASE_URL}{endpoint}", json=data)
            else:
                response = requests.get(f"{BASE_URL}{endpoint}")
            
            # Check for rate limit headers
            if not headers_found and 'X-RateLimit-Limit' in response.headers:
                headers_found = True
                print(f"\n✓ Rate limit headers found:")
                print(f"  X-RateLimit-Limit: {response.headers.get('X-RateLimit-Limit')}")
                print(f"  X-RateLimit-Remaining: {response.headers.get('X-RateLimit-Remaining')}")
                print(f"  X-RateLimit-Reset: {response.headers.get('X-RateLimit-Reset')}")
            
            if response.status_code == 429:
                rate_limited_count += 1
                if rate_limited_count == 1:
                    print(f"\n✓ Rate limit exceeded at request #{i}")
                    print(f"  Response: {response.json()}")
            else:
                success_count += 1
        
        except Exception as e:
            print(f"✗ Error on request #{i}: {e}")
        
        # Small delay to avoid overwhelming the server
        time.sleep(0.1)
    
    # Results
    print(f"\nResults:")
    print(f"  Successful requests: {success_count}")
    print(f"  Rate limited requests: {rate_limited_count}")
    print(f"  Headers present: {'Yes' if headers_found else 'No'}")
    
    # Verification
    passed = (
        success_count <= expected_limit and 
        rate_limited_count > 0 and 
        headers_found
    )
    
    if passed:
        print(f"✓ TEST PASSED")
    else:
        print(f"✗ TEST FAILED")
    
    return {
        "endpoint": endpoint,
        "passed": passed,
        "success_count": success_count,
        "rate_limited_count": rate_limited_count,
        "headers_found": headers_found
    }

def test_rate_limit_status():
    """Test the rate limit status endpoint"""
    print_section("Rate Limit Status Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/api/v1/rate-limit/status")
        
        if response.status_code == 200:
            data = response.json()
            print("✓ Status endpoint accessible")
            print(f"\nConfiguration:")
            print(f"  Enabled: {data['data']['enabled']}")
            print(f"  Storage: {data['data']['storage_backend']}")
            print(f"  Whitelist count: {data['data']['whitelist_count']}")
            print(f"\nLimits:")
            for key, value in data['data']['limits'].items():
                print(f"  {key}: {value}")
            return True
        else:
            print(f"✗ Status endpoint failed: {response.status_code}")
            return False
    
    except Exception as e:
        print(f"✗ Error accessing status endpoint: {e}")
        return False

def main():
    """Run all rate limiting tests"""
    print_section("OneQlick Rate Limiting Test Suite")
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code != 200:
            print("✗ Server is not responding. Please start the backend server.")
            return
        print("✓ Server is running")
    except Exception as e:
        print(f"✗ Cannot connect to server: {e}")
        print(f"  Make sure the backend is running at {BASE_URL}")
        return
    
    # Test rate limit status endpoint
    if not test_rate_limit_status():
        print("\n✗ Rate limiting may not be enabled. Check configuration.")
        return
    
    # Test cases
    test_results: List[Dict] = []
    
    # Test 1: Login endpoint (10 req/min)
    print_section("Test 1: Login Rate Limit (10 req/min)")
    result = test_rate_limit(
        endpoint="/api/v1/auth/login",
        method="POST",
        data={"identifier": "test@example.com", "password": "wrongpassword"},
        expected_limit=10,
        num_requests=15
    )
    test_results.append(result)
    
    # Test 2: Search endpoint (50 req/min)
    print_section("Test 2: Search Rate Limit (50 req/min)")
    result = test_rate_limit(
        endpoint="/api/v1/search/?query=pizza&latitude=19.0760&longitude=72.8777",
        method="GET",
        expected_limit=50,
        num_requests=60
    )
    test_results.append(result)
    
    # Test 3: Restaurant nearby endpoint (100 req/min)
    print_section("Test 3: Restaurant Nearby Rate Limit (100 req/min)")
    result = test_rate_limit(
        endpoint="/api/v1/restaurants/nearby?latitude=19.0760&longitude=72.8777",
        method="GET",
        expected_limit=100,
        num_requests=110
    )
    test_results.append(result)
    
    # Summary
    print_section("Test Summary")
    passed_tests = sum(1 for r in test_results if r['passed'])
    total_tests = len(test_results)
    
    print(f"Tests passed: {passed_tests}/{total_tests}\n")
    
    for i, result in enumerate(test_results, 1):
        status = "✓ PASSED" if result['passed'] else "✗ FAILED"
        print(f"{i}. {result['endpoint']}: {status}")
    
    if passed_tests == total_tests:
        print(f"\n{'='*60}")
        print(" ✓ ALL TESTS PASSED - Rate limiting is working correctly!")
        print(f"{'='*60}\n")
    else:
        print(f"\n{'='*60}")
        print(f" ✗ {total_tests - passed_tests} test(s) failed - Review configuration")
        print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
