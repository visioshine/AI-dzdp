import urllib.request
import json

# 简单的 HTTP 请求函数
def http_request(url, method='GET', data=None, headers=None):
    if not headers:
        headers = {}
    
    req = urllib.request.Request(url, method=method)
    
    if data:
        if isinstance(data, dict):
            data_str = json.dumps(data)
            if 'Content-Type' not in headers:
                headers['Content-Type'] = 'application/json'
        else:
            data_str = data
        req.data = data_str.encode('utf-8')
    
    for key, value in headers.items():
        req.add_header(key, value)
    
    try:
        with urllib.request.urlopen(req) as response:
            status_code = response.getcode()
            response_content = response.read().decode('utf-8')
            return status_code, response_content
    except urllib.error.HTTPError as e:
        status_code = e.code
        response_content = e.read().decode('utf-8')
        return status_code, response_content
    except Exception as e:
        return None, str(e)

print("=== Testing Review Flow ===")

# 1. 登录获取令牌
print("\n1. User Login...")
login_data = "username=13800138000&password=newpassword123"
status_code, body = http_request(
    "http://localhost:8000/token",
    method="POST",
    data=login_data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)

print(f"Status Code: {status_code}")
if status_code == 200:
    token_data = json.loads(body)
    access_token = token_data['access_token']
    print("Login successful, token obtained")
    
    # 2. 创建一个测试商家（如果还没有）
    print("\n2. Check if test merchant exists...")
    status_code, body = http_request("http://localhost:8000/merchants/1")
    
    if status_code != 200:
        print("Creating test merchant...")
        merchant_data = {
            "name": "Test Restaurant",
            "description": "A test restaurant",
            "address": "123 Test Street, Beijing",
            "category": "Food",
            "phone": "13800138000",
            "image_url": "https://picsum.photos/id/1019/600/400"
        }
        status_code, body = http_request(
            "http://localhost:8000/merchants",
            method="POST",
            data=merchant_data
        )
        print(f"Create merchant status: {status_code}")
    else:
        print("Test merchant already exists")
    
    # 3. 提交一个评价
    print("\n3. Submit a review...")
    review_data = {
        "rating": 5,
        "content": "This is a test review for the test merchant!"
    }
    status_code, body = http_request(
        "http://localhost:8000/merchants/1/reviews",
        method="POST",
        data=review_data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Submit review status: {status_code}")
    print(f"Response: {body}")
    
    if status_code == 200:
        submitted_review = json.loads(body)
        print("Review submitted successfully!")
        print(f"Review ID: {submitted_review['id']}")
        print(f"Review merchant: {submitted_review['merchant']['name']}")
    
    # 4. 查看个人中心的"我的评价"
    print("\n4. Get user's reviews...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/reviews",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Get reviews status: {status_code}")
    print(f"Response: {body}")
    
    if status_code == 200:
        user_reviews = json.loads(body)
        print(f"Total reviews: {len(user_reviews)}")
        
        if len(user_reviews) > 0:
            print("\nFirst review details:")
            print(f"ID: {user_reviews[0]['id']}")
            print(f"Content: {user_reviews[0]['content']}")
            print(f"Rating: {user_reviews[0]['rating']}")
            if 'merchant' in user_reviews[0]:
                print(f"Merchant: {user_reviews[0]['merchant']['name']}")
            else:
                print("Warning: No merchant information in the review!")
    
    # 5. 验证评价是否展示在商家详情中
    print("\n5. Get merchant details...")
    status_code, body = http_request("http://localhost:8000/merchants/1")
    
    print(f"Get merchant status: {status_code}")
    if status_code == 200:
        merchant_details = json.loads(body)
        print(f"Merchant: {merchant_details['name']}")
        print(f"Total reviews: {merchant_details['reviews_count']}")
        if 'reviews' in merchant_details:
            print(f"Reviews in details: {len(merchant_details['reviews'])}")
        else:
            print("Warning: No reviews in merchant details!")
            
else:
    print(f"Login failed: {body}")
    exit()

print("\n=== Review flow test completed ===")
