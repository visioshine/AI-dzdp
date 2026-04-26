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

print("=== Simple Review Test ===")

# 1. 登录获取令牌
login_data = "username=13800138000&password=newpassword123"
status, body = http_request(
    "http://localhost:8000/token",
    method="POST",
    data=login_data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)

if status != 200:
    print(f"Login failed: {body}")
    exit()

token = json.loads(body)['access_token']
print("Login successful!")

# 2. 提交评价
review_data = {"rating": 5, "content": "Test review 123"}
status, body = http_request(
    "http://localhost:8000/merchants/1/reviews",
    method="POST",
    data=review_data,
    headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
)

print(f"Submit review status: {status}")
if status == 200:
    review = json.loads(body)
    print(f"Review ID: {review['id']}")
    if 'merchant' in review:
        print(f"Has merchant info: {review['merchant']['name']}")
    else:
        print("No merchant info!")
else:
    print(f"Submit failed: {body}")

# 3. 获取我的评价
status, body = http_request(
    "http://localhost:8000/users/me/reviews",
    headers={'Authorization': f'Bearer {token}'}
)

print(f"Get reviews status: {status}")
if status == 200:
    reviews = json.loads(body)
    print(f"Total reviews: {len(reviews)}")
    if reviews:
        first_review = reviews[0]
        print(f"First review content: {first_review['content']}")
        if 'merchant' in first_review:
            print(f"Has merchant info: {first_review['merchant']['name']}")
        else:
            print("No merchant info!")
else:
    print(f"Get reviews failed: {body}")

print("\nTest completed!")
