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

# 测试商家数据
test_merchant = {
    "name": "Test Restaurant",
    "description": "A test restaurant",
    "address": "123 Test Street, Beijing",
    "category": "Food",
    "phone": "13800138000",
    "image_url": "https://picsum.photos/id/1019/600/400"
}

print("=== Creating Test Merchant ===")

# 创建商家
status_code, body = http_request(
    "http://localhost:8000/merchants",
    method="POST",
    data=test_merchant
)

print(f"Status Code: {status_code}")
print(f"Response: {body}")

if status_code == 200:
    print("Merchant created successfully!")
else:
    print("Failed to create merchant!")

# 检查商家列表
print("\n=== Checking Merchant List ===")
status_code, body = http_request("http://localhost:8000/merchants")

print(f"Status Code: {status_code}")
print(f"Response: {body}")
