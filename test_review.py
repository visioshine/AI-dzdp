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

# 测试流程
print("=== 测试评价提交功能 ===")

# 1. 注册新用户（如果需要）
print("\n1. 注册新用户...")
register_data = {
    "username": "testreviewuser",
    "email": "testreviewuser@example.com",
    "password": "testpassword"
}
status_code, body = http_request(
    "http://localhost:8000/register",
    method="POST",
    data=register_data
)
print(f"注册状态码: {status_code}")

# 2. 登录获取令牌
print("\n2. 用户登录...")
login_data = "username=testreviewuser&password=testpassword"
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
    print(f"获取到令牌: {access_token}")
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
        print(f"选择商家: {selected_merchant['name']} (ID: {selected_merchant['id']})")
    else:
        print("没有找到商家")
        exit()
else:
    print(f"获取商家列表失败: {body}")
    exit()

# 4. 提交评价
print("\n4. 提交评价...")
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
else:
    print("\n❌ 评价提交失败！")
