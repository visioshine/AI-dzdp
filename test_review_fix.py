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

print("=== Testing Review Fixes ===")

# 1. 登录获取令牌
print("\n1. User Login...")
login_data = "username=visioshine&password=newpassword123"
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
    
    # 2. 获取初始的用户统计数据
    print("\n2. Get Initial User Stats...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/stats",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        initial_stats = json.loads(body)
        print(f"Initial reviews count: {initial_stats['reviews']}")
    else:
        print(f"Failed to get initial stats: {body}")
        exit()
    
    # 3. 提交一条新的评价
    print("\n3. Submit New Review...")
    review_data = {
        "rating": 4,
        "content": "这是一条测试评价，用于验证修复是否有效。"
    }
    status_code, body = http_request(
        "http://localhost:8000/merchants/1/reviews",
        method="POST",
        data=review_data,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        print("Review submitted successfully!")
    else:
        print(f"Failed to submit review: {body}")
        exit()
    
    # 4. 获取更新后的用户统计数据
    print("\n4. Get Updated User Stats...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/stats",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        updated_stats = json.loads(body)
        print(f"Updated reviews count: {updated_stats['reviews']}")
        if updated_stats['reviews'] == initial_stats['reviews'] + 1:
            print("✅ Reviews count updated correctly!")
        else:
            print("❌ Reviews count did not update correctly!")
    else:
        print(f"Failed to get updated stats: {body}")
    
    # 5. 获取用户评价列表
    print("\n5. Get User Reviews...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/reviews",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        reviews = json.loads(body)
        print(f"Total reviews retrieved: {len(reviews)}")
        if len(reviews) > 0:
            # 检查第一条评价是否包含商家信息
            first_review = reviews[0]
            if 'merchant' in first_review and first_review['merchant']:
                print(f"✅ First review includes merchant information: {first_review['merchant']['name']}")
            else:
                print("❌ Review does not include merchant information")
        print("✅ Get reviews successful!")
    else:
        print(f"❌ Get reviews failed: {body}")
    
else:
    print(f"Login failed: {body}")
    exit()

print("\n=== All tests completed ===")
