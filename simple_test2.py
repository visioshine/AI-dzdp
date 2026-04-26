import socket
import json

# 简单的 HTTP POST 函数
def http_post(host, path, data, content_type='application/json'):
    # 如果是 JSON 数据，转换为字符串
    if content_type == 'application/json':
        data_str = json.dumps(data)
    else:
        data_str = data
    
    # 创建请求
    request = f"POST {path} HTTP/1.1\r\n"
    request += f"Host: {host}\r\n"
    request += f"Content-Type: {content_type}\r\n"
    request += f"Content-Length: {len(data_str)}\r\n"
    request += "\r\n"
    request += data_str
    
    # 发送请求
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, 8000))
    sock.sendall(request.encode('utf-8'))
    
    # 接收响应
    response = b''
    while True:
        data = sock.recv(1024)
        if not data:
            break
        response += data
    sock.close()
    
    # 解析响应
    headers, body = response.split(b'\r\n\r\n', 1)
    status_code = headers.split(b' ')[1].decode('utf-8')
    
    return status_code, body.decode('utf-8')

# 测试注册
print("=== 测试注册 ===")
register_data = {
    "username": "testuser",
    "email": "641077621@qq.com",
    "password": "testpassword"
}

status_code, body = http_post("localhost", "/register", register_data)
print(f"状态码: {status_code}")
print(f"响应内容: {body}")

# 测试登录
print("\n=== 测试登录 ===")
login_data = "username=testuser&password=testpassword"

status_code, body = http_post("localhost", "/token", login_data, 'application/x-www-form-urlencoded')
print(f"状态码: {status_code}")
print(f"响应内容: {body}")
