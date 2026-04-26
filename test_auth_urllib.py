import urllib.request
import urllib.parse
import json

# 测试注册
print("=== 测试注册 ===")
register_url = "http://localhost:8000/register"
register_data = {
    "username": "testuser",
    "email": "641077621@qq.com",
    "password": "testpassword"
}

json_data = json.dumps(register_data).encode('utf-8')
headers = {'Content-Type': 'application/json'}

try:
    req = urllib.request.Request(register_url, data=json_data, headers=headers)
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        response_content = response.read().decode('utf-8')
        print(f"状态码: {status_code}")
        print(f"响应内容: {response_content}")
        try:
            json_response = json.loads(response_content)
            print(f"JSON响应: {json_response}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
except urllib.error.HTTPError as e:
    status_code = e.code
    response_content = e.read().decode('utf-8')
    print(f"HTTP错误 - 状态码: {status_code}")
    print(f"响应内容: {response_content}")
except Exception as e:
    print(f"请求错误: {e}")

# 测试登录
print("\n=== 测试登录 ===")
login_url = "http://localhost:8000/token"
login_data = {
    "username": "testuser",
    "password": "testpassword"
}

form_data = urllib.parse.urlencode(login_data).encode('utf-8')
headers = {'Content-Type': 'application/x-www-form-urlencoded'}

try:
    req = urllib.request.Request(login_url, data=form_data, headers=headers)
    with urllib.request.urlopen(req) as response:
        status_code = response.getcode()
        response_content = response.read().decode('utf-8')
        print(f"状态码: {status_code}")
        print(f"响应内容: {response_content}")
        try:
            json_response = json.loads(response_content)
            print(f"JSON响应: {json_response}")
        except json.JSONDecodeError as e:
            print(f"JSON解析错误: {e}")
except urllib.error.HTTPError as e:
    status_code = e.code
    response_content = e.read().decode('utf-8')
    print(f"HTTP错误 - 状态码: {status_code}")
    print(f"响应内容: {response_content}")
except Exception as e:
    print(f"请求错误: {e}")
