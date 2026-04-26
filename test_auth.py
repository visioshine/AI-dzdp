import requests
import json

# 测试注册
print("=== 测试注册 ===")
register_url = "http://localhost:8000/register"
register_data = {
    "username": "testuser",
    "email": "641077621@qq.com",
    "password": "testpassword"
}

response = requests.post(register_url, json=register_data)
print(f"状态码: {response.status_code}")
print(f"响应头: {response.headers}")
print(f"响应内容: {response.text}")

# 测试登录
print("\n=== 测试登录 ===")
login_url = "http://localhost:8000/token"
login_data = {
    "username": "testuser",
    "password": "testpassword"
}

response = requests.post(login_url, data=login_data)
print(f"状态码: {response.status_code}")
print(f"响应头: {response.headers}")
print(f"响应内容: {response.text}")
