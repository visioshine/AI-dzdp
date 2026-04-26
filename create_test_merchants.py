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
        "name": "海底捞火锅",
        "description": "正宗四川火锅，服务一流",
        "address": "北京市朝阳区建国路88号",
        "category": "美食",
        "phone": "010-12345678",
        "image_url": "https://picsum.photos/id/1019/600/400"
    },
    {
        "name": "星巴克咖啡",
        "description": "全球连锁咖啡品牌，环境舒适",
        "address": "北京市海淀区中关村大街1号",
        "category": "美食",
        "phone": "010-87654321",
        "image_url": "https://picsum.photos/id/1020/600/400"
    },
    {
        "name": "万达影城",
        "description": "现代化影城，IMAX厅效果震撼",
        "address": "北京市朝阳区建国路93号万达购物中心5层",
        "category": "电影",
        "phone": "010-135792468",
        "image_url": "https://picsum.photos/id/1021/600/400"
    },
    {
        "name": "健身房",
        "description": "24小时营业，设备齐全",
        "address": "北京市西城区西单北大街131号",
        "category": "运动健康",
        "phone": "010-246813579",
        "image_url": "https://picsum.photos/id/1022/600/400"
    }
]

print("=== 创建测试商家 ===")

# 创建商家for merchant in test_merchants:
for merchant in test_merchants:
    print(f"\n创建商家: {merchant['name']}")
    status_code, body = http_request(
        "http://localhost:8000/merchants",
        method="POST",
        data=merchant
    )
    
    print(f"状态码: {status_code}")
    print(f"响应内容: {body}")
    
    if status_code == 200:
        print(f"✅ 商家 {merchant['name']} 创建成功！")
    else:
        print(f"❌ 商家 {merchant['name']} 创建失败！")

print("\n=== 所有商家创建完成 ===")
