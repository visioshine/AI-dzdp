import requests

print("=== Testing Submit Review Fix ===")

# 1. 登录获取令牌
token_url = "http://localhost:8000/token"
login_data = {
    "username": "13800138000",
    "password": "newpassword123"
}

print("\n1. Logging in...")
login_response = requests.post(token_url, data=login_data)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    token_data = login_response.json()
    access_token = token_data['access_token']
    print(f"Token: {access_token}")
    
    # 2. 提交评价
    review_url = "http://localhost:8000/merchants/1/reviews"
    review_data = {
        "rating": 5,
        "content": "Test review after fix"
    }
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    print("\n2. Submitting review...")
    review_response = requests.post(review_url, json=review_data, headers=headers)
    print(f"Submit status: {review_response.status_code}")
    print(f"Response: {review_response.text}")
    
    if review_response.status_code == 200:
        print("\n✅ Review submitted successfully!")
        review = review_response.json()
        print(f"Review ID: {review['id']}")
        print(f"Content: {review['content']}")
        print(f"Rating: {review['rating']}")
        if 'merchant' in review:
            print(f"Merchant: {review['merchant']['name']}")
    else:
        print("\n❌ Review submission failed!")
else:
    print("\n❌ Login failed!")

print("\nTest completed!")
