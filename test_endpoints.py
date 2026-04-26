import urllib.request
import json

# 测试所有端点
def test_endpoint(url, method='GET', data=None, headers=None):
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

print("=== Testing All Endpoints ===")

# 测试主页
print("\n1. Testing / (home)")
status, body = test_endpoint("http://localhost:8000/")
print(f"Status: {status}")

# 测试商家列表端点
print("\n2. Testing /merchants")
status, body = test_endpoint("http://localhost:8000/merchants")
print(f"Status: {status}")
print(f"Response: {body[:200]}...")  # 只显示前200个字符

# 测试用户统计端点
print("\n3. Testing /users/me/stats (requires auth)")
status, body = test_endpoint("http://localhost:8000/users/me/stats")
print(f"Status: {status}")
print(f"Response: {body[:200]}...")

# 测试登录端点
print("\n4. Testing /token (login)")
login_data = "username=13800138000&password=newpassword123"
status, body = test_endpoint(
    "http://localhost:8000/token",
    method="POST",
    data=login_data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)
print(f"Status: {status}")

if status == 200:
    token_data = json.loads(body)
    access_token = token_data['access_token']
    print("Login successful, token obtained")
    
    # 测试需要认证的端点
    print("\n5. Testing /users/me (requires auth)")
    status, body = test_endpoint(
        "http://localhost:8000/users/me",
        headers={'Authorization': f'Bearer {access_token}'}
    )
    print(f"Status: {status}")
    print(f"Response: {body[:200]}...")
    
    print("\n6. Testing /users/me/stats (with auth)")
    status, body = test_endpoint(
        "http://localhost:8000/users/me/stats",
        headers={'Authorization': f'Bearer {access_token}'}
    )
    print(f"Status: {status}")
    print(f"Response: {body[:200]}...")

print("\n=== All tests completed ===")
