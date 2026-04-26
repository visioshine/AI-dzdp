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
test_merchants = [
    {
        "name": "Sichuan Restaurant",
        "description": "Authentic Sichuan cuisine with spicy dishes",
        "address": "456 Test Street, Beijing",
        "category": "Food",
        "phone": "13800138001",
        "image_url": "https://picsum.photos/id/1020/600/400"
    },
    {
        "name": "Coffee Shop",
        "description": "Cozy coffee shop with specialty drinks",
        "address": "789 Test Street, Beijing",
        "category": "Food",
        "phone": "13800138002",
        "image_url": "https://picsum.photos/id/1021/600/400"
    },
    {
        "name": "Cinema",
        "description": "Modern cinema with IMAX screens",
        "address": "101 Test Street, Beijing",
        "category": "Movie",
        "phone": "13800138003",
        "image_url": "https://picsum.photos/id/1022/600/400"
    },
    {
        "name": "Gym",
        "description": "24-hour gym with modern equipment",
        "address": "202 Test Street, Beijing",
        "category": "Sports",
        "phone": "13800138004",
        "image_url": "https://picsum.photos/id/1023/600/400"
    }
]

print("=== Creating More Test Merchants ===")

# 创建商家
for merchant in test_merchants:
    print(f"\nCreating merchant: {merchant['name']}")
    status_code, body = http_request(
        "http://localhost:8000/merchants",
        method="POST",
        data=merchant
    )
    
    print(f"Status Code: {status_code}")
    if status_code == 200:
        print(f"Merchant {merchant['name']} created successfully!")
    else:
        print(f"Failed to create merchant {merchant['name']}!")
        print(f"Response: {body}")

# 检查商家列表
print("\n=== Checking Merchant List ===")
status_code, body = http_request("http://localhost:8000/merchants")

print(f"Status Code: {status_code}")
if status_code == 200:
    merchants = json.loads(body)
    print(f"Total merchants: {len(merchants)}")
    for merchant in merchants:
        print(f"- {merchant['name']} (ID: {merchant['id']})")
else:
    print(f"Failed to get merchant list!")
    print(f"Response: {body}")

print("\n=== All merchants created ===")
