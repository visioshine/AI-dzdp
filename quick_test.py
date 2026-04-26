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

# 1. 登录获取令牌
print("Logging in...")
login_data = "username=13800138000&password=newpassword123"
status, body = http_request(
    "http://localhost:8000/token",
    method="POST",
    data=login_data,
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
)

print("Login status:", status)
if status == 200:
    token_data = json.loads(body)
    access_token = token_data['access_token']
    print("Token obtained")
    
    # 2. 提交评价
    print("Submitting review...")
    review_data = {"rating": 5, "content": "Test review"}
    status, body = http_request(
        "http://localhost:8000/merchants/7/reviews",
        method="POST",
        data=review_data,
        headers={
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
    )
    
    print("Submit status:", status)
    print("Response:", body)
