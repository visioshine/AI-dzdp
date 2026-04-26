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

print("=== Testing Profile Features ===")

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
    
    # 2. 测试获取用户评价列表
    print("\n2. Test Get User Reviews...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/reviews",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        reviews = json.loads(body)
        print(f"Total reviews: {len(reviews)}")
        print("✅ Get reviews successful!")
    else:
        print(f"❌ Get reviews failed: {body}")
    
    # 3. 测试获取用户收藏列表
    print("\n3. Test Get User Favorites...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/favorites",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        favorites = json.loads(body)
        print(f"Total favorites: {len(favorites)}")
        print("✅ Get favorites successful!")
    else:
        print(f"❌ Get favorites failed: {body}")
    
    # 4. 测试更新用户信息
    print("\n4. Test Update User Profile...")
    update_data = {
        "username": "testuserupdated",
        "phone": "13800138001",
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=updated"
    }
    status_code, body = http_request(
        "http://localhost:8000/users/me",
        method="PUT",
        data=update_data,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        updated_user = json.loads(body)
        print(f"Updated username: {updated_user['username']}")
        print(f"Updated phone: {updated_user['phone']}")
        print("✅ Update profile successful!")
    else:
        print(f"❌ Update profile failed: {body}")
    
    # 5. 将用户名改回原来的，以便下次测试
    print("\n5. Restore Original Username...")
    restore_data = {
        "username": "13800138000"
    }
    status_code, body = http_request(
        "http://localhost:8000/users/me",
        method="PUT",
        data=restore_data,
        headers={
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        print("✅ Username restored!")
    else:
        print(f"❌ Failed to restore username: {body}")
        
else:
    print(f"Login failed: {body}")
    exit()

print("\n=== All tests completed ===")
