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

print("=== Testing Personal Center Features ===")

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
    
    # 2. 获取用户统计数据
    print("\n2. Get User Stats...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/stats",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    print(f"Response: {body}")
    
    if status_code == 200:
        stats = json.loads(body)
        print(f"Reviews: {stats.get('reviews', 0)}")
        print(f"Favorites: {stats.get('favorites', 0)}")
        print(f"Points: {stats.get('points', 0)}")
    
    # 3. 获取用户的评价列表
    print("\n3. Get User Reviews...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/reviews",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    print(f"Response: {body}")
    
    if status_code == 200:
        reviews = json.loads(body)
        print(f"Total reviews: {len(reviews)}")
    
    # 4. 获取用户的收藏列表
    print("\n4. Get User Favorites...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/favorites",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    print(f"Response: {body}")
    
    if status_code == 200:
        favorites = json.loads(body)
        print(f"Total favorites: {len(favorites)}")
    
    # 5. 测试添加收藏功能
    print("\n5. Test Add Favorite...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/favorites/1",
        method="POST",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    print(f"Response: {body}")
    
    # 6. 再次获取收藏列表，验证是否添加成功
    print("\n6. Get Favorites Again...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/favorites",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        favorites = json.loads(body)
        print(f"Total favorites after adding: {len(favorites)}")
    
    # 7. 测试移除收藏功能
    print("\n7. Test Remove Favorite...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/favorites/1",
        method="DELETE",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    print(f"Response: {body}")
    
    # 8. 再次获取收藏列表，验证是否移除成功
    print("\n8. Get Favorites Again...")
    status_code, body = http_request(
        "http://localhost:8000/users/me/favorites",
        headers={
            'Authorization': f'Bearer {access_token}'
        }
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        favorites = json.loads(body)
        print(f"Total favorites after removing: {len(favorites)}")
        
else:
    print(f"Login failed: {body}")
    exit()

print("\n=== All tests completed ===")
