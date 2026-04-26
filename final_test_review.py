import urllib.request
import urllib.parse
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

print("=== 评价提交功能测试 ===")

# 1. 注册新用户（如果需要）
print("\n1. 注册测试用户...")
register_data = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "testpassword"
}
status_code, body = http_request(
    "http://localhost:8000/register",
    method="POST",
    data=register_data
)
print(f"注册状态码: {status_code}")
if status_code == 200:
    print(f"注册成功: {body}")
elif status_code == 400 and 'already registered' in body:
    print(f"用户已存在，跳过注册: {body}")
else:
    print(f"注册失败: {body}")

# 2. 登录获取令牌
print("\n2. 用户登录...")
login_data = "username=testuser&password=testpassword"
status_code, body = http_request(
    "http://localhost:8000/token",
    method="POST",
    data=login_data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)
print(f"登录状态码: {status_code}")
if status_code == 200:
    token_data = json.loads(body)
    access_token = token_data['access_token']
    print(f"登录成功，获取到令牌: {access_token[:30]}...")
else:
    print(f"登录失败: {body}")
    exit()

# 3. 获取商家列表
print("\n3. 获取商家列表...")
status_code, body = http_request("http://localhost:8000/merchants")
print(f"获取商家列表状态码: {status_code}")
if status_code == 200:
    merchants = json.loads(body)
    if merchants:
        selected_merchant = merchants[0]
        print(f"选择第一个商家: {selected_merchant['name']} (ID: {selected_merchant['id']})")
    else:
        print("没有找到商家，需要先创建一个商家")
        
        # 4. 创建一个商家（如果没有）
        print("\n4. 创建测试商家...")
        create_merchant_data = {
            "name": "测试餐厅",
            "description": "这是一家测试餐厅",
            "address": "北京市朝阳区测试街道1号",
            "category": "美食",
            "phone": "13800138000",
            "image_url": "https://example.com/image.jpg"
        }
        status_code, body = http_request(
            "http://localhost:8000/merchants",
            method="POST",
            data=create_merchant_data,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {access_token}'
            }
        )
        print(f"创建商家状态码: {status_code}")
        if status_code == 200:
            new_merchant = json.loads(body)
            print(f"商家创建成功: {new_merchant['name']} (ID: {new_merchant['id']})")
            selected_merchant = new_merchant
        else:
            print(f"商家创建失败: {body}")
            print("使用模拟商家ID 1进行测试")
            selected_merchant = {'id': 1, 'name': '模拟商家'}
else:
    print(f"获取商家列表失败: {body}")
    print("使用模拟商家ID 1进行测试")
    selected_merchant = {'id': 1, 'name': '模拟商家'}

# 5. 提交评价
print("\n5. 提交评价...")
review_data = {
    "rating": 5,
    "content": "这家店的服务非常好，味道也不错！"
}
status_code, body = http_request(
    f"http://localhost:8000/merchants/{selected_merchant['id']}/reviews",
    method="POST",
    data=review_data,
    headers={
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
)
print(f"提交评价状态码: {status_code}")
print(f"响应内容: {body}")

if status_code == 200:
    print("\n✅ 评价提交成功！")
    print("UUID格式错误问题已经解决。")
else:
    print("\n❌ 评价提交失败！")
    if "uuid" in body.lower():
        print("❌ 仍然存在UUID格式错误问题！")
