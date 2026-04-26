const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 8000;

const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

// Mock database
let mockUsers = [
  {
    id: 1,
    username: 'demo',
    email: 'demo@example.com',
    phone: '13800138000',
    hashed_password: 'demo123',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=1',
    bio: '热爱美食，喜欢探索新店铺',
    catchphrase: '生活就是要吃好喝好',
    gender: 'male'
  }
];

let mockTokens = {};

const MOCK_MERCHANTS = [
  {
    id: 1,
    name: "老北京涮肉",
    description: "地道的北京风味涮羊肉，传统铜锅，羊肉鲜嫩。",
    address: "朝阳区三里屯1号",
    category: "美食",
    phone: "010-12345678",
    rating: 4.8,
    reviews_count: 1250,
    image_url: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&auto=format&fit=crop",
    price: "￥120/人",
    created_at: new Date().toISOString()
  },
  {
    id: 2,
    name: "悦己SPA",
    description: "高端水疗体验，放松身心，技师手法专业。",
    address: "海淀区中关村大街2号",
    category: "休闲娱乐",
    phone: "010-87654321",
    rating: 4.9,
    reviews_count: 850,
    image_url: "https://images.unsplash.com/photo-1600334129128-685c5582fd35?w=800&auto=format&fit=crop",
    price: "￥388/人",
    created_at: new Date().toISOString()
  },
  {
    id: 3,
    name: "光影电影院",
    description: "IMAX巨幕，极致视听享受，环境舒适。",
    address: "朝阳区大望路3号",
    category: "电影",
    phone: "010-13572468",
    rating: 4.5,
    reviews_count: 3200,
    image_url: "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&auto=format&fit=crop",
    price: "￥65/人",
    created_at: new Date().toISOString()
  },
  {
    id: 4,
    name: "书香苑图书馆",
    description: "安静的学习环境，海量图书，提供免费咖啡。",
    address: "西城区阜成门外大街5号",
    category: "文化生活",
    phone: "010-24681357",
    rating: 4.7,
    reviews_count: 450,
    image_url: "https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&auto=format&fit=crop",
    price: "免费",
    created_at: new Date().toISOString()
  },
  {
    id: 5,
    name: "极速健身房",
    description: "器械齐全，专业私教，24小时营业。",
    address: "朝阳区望京SOHO 8号",
    category: "运动健康",
    phone: "010-11223344",
    rating: 4.6,
    reviews_count: 670,
    image_url: "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&auto=format&fit=crop",
    price: "￥199/月",
    created_at: new Date().toISOString()
  }
];

const MOCK_REVIEWS = [
  {
    id: 1,
    merchant_id: 1,
    user_id: 1,
    content: "羊肉真的很新鲜，汤底也很鲜美，下次还会再来！",
    rating: 5,
    created_at: new Date().toISOString(),
    author: { username: "张三", avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=zhangsan" }
  },
  {
    id: 2,
    merchant_id: 1,
    user_id: 2,
    content: "味道不错，就是人比较多，需要排队。",
    rating: 4,
    created_at: new Date().toISOString(),
    author: { username: "李四", avatar: "https://api.dicebear.com/7.x/avataaars/svg?seed=lisi" }
  }
];

// Helper to parse JSON body
function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => {
      body += chunk.toString();
    });
    req.on('end', () => {
      try {
        resolve(JSON.parse(body));
      } catch (e) {
        reject(e);
      }
    });
  });
}

// Helper to get user from token
function getUserFromToken(req) {
  const authHeader = req.headers.authorization;
  if (authHeader && authHeader.startsWith('Bearer ')) {
    const token = authHeader.substring(7);
    return mockTokens[token];
  }
  return null;
}

const server = http.createServer(async (req, res) => {
  console.log(`${req.method} ${req.url}`);

  // Set CORS headers for all responses
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  // Handle preflight OPTIONS requests
  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  // Handle register endpoint
  if (req.method === 'POST' && req.url === '/register') {
    try {
      const data = await parseBody(req);
      
      // Check if username already exists
      const existingUser = mockUsers.find(u => u.username === data.username);
      if (existingUser) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ detail: '用户名已注册' }));
        return;
      }

      // Check if email already exists
      if (data.email) {
        const existingEmail = mockUsers.find(u => u.email === data.email);
        if (existingEmail) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ detail: '邮箱已注册' }));
          return;
        }
      }

      const newUser = {
        id: mockUsers.length + 1,
        username: data.username,
        email: data.email || null,
        phone: data.phone || null,
        hashed_password: data.password,
        avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${Date.now()}`,
        bio: '',
        catchphrase: '',
        gender: 'secret'
      };
      
      mockUsers.push(newUser);
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        id: newUser.id,
        username: newUser.username,
        email: newUser.email,
        phone: newUser.phone
      }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '请求格式错误' }));
    }
    return;
  }

  // Handle login endpoint
  if (req.method === 'POST' && req.url === '/token') {
    try {
      const formData = new URLSearchParams(await parseBody(req));
      const username = formData.get('username') || (await parseBody(req)).username;
      const password = formData.get('password') || (await parseBody(req)).password;

      const user = mockUsers.find(u => 
        u.username === username || 
        u.email === username || 
        u.phone === username
      );

      if (!user || user.hashed_password !== password) {
        res.writeHead(401, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ detail: '用户名或密码错误' }));
        return;
      }

      const token = 'token_' + Date.now();
      mockTokens[token] = user;

      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        access_token: token,
        token_type: 'bearer'
      }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '请求格式错误' }));
    }
    return;
  }

  // Handle get current user endpoint
  if (req.method === 'GET' && req.url === '/users/me') {
    const user = getUserFromToken(req);
    if (!user) {
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '未授权' }));
      return;
    }

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      id: user.id,
      username: user.username,
      email: user.email,
      phone: user.phone,
      avatar: user.avatar,
      bio: user.bio,
      catchphrase: user.catchphrase,
      gender: user.gender
    }));
    return;
  }

  // Handle update current user endpoint
  if (req.method === 'PUT' && req.url === '/users/me') {
    const user = getUserFromToken(req);
    if (!user) {
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '未授权' }));
      return;
    }

    try {
      const data = await parseBody(req);
      
      // Update user fields
      Object.assign(user, data);
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        id: user.id,
        username: user.username,
        email: user.email,
        phone: user.phone,
        avatar: user.avatar,
        bio: user.bio,
        catchphrase: user.catchphrase,
        gender: user.gender
      }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '请求格式错误' }));
    }
    return;
  }

  // Handle get user stats endpoint
  if (req.method === 'GET' && req.url === '/users/me/stats') {
    const user = getUserFromToken(req);
    if (!user) {
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '未授权' }));
      return;
    }

    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      reviews: 3,
      favorites: 5,
      points: 55
    }));
    return;
  }

  // Handle get user reviews endpoint
  if (req.method === 'GET' && req.url === '/users/me/reviews') {
    const user = getUserFromToken(req);
    if (!user) {
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '未授权' }));
      return;
    }

    const userReviews = MOCK_REVIEWS.filter(r => r.user_id === user.id);
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(userReviews));
    return;
  }

  // Handle get user favorites endpoint
  if (req.method === 'GET' && req.url === '/users/me/favorites') {
    const user = getUserFromToken(req);
    if (!user) {
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '未授权' }));
      return;
    }

    // Return first 3 merchants as favorites for demo
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify(MOCK_MERCHANTS.slice(0, 3)));
    return;
  }

  // Handle password reset request endpoint
  if (req.method === 'POST' && req.url === '/password-reset-request') {
    res.setHeader('Content-Type', 'application/json');
    
    try {
      const data = await parseBody(req);
      const verificationCode = Math.floor(100000 + Math.random() * 900000).toString();
      console.log(`Password reset requested for ${data.email}, verification code: ${verificationCode}`);
      
      res.writeHead(200);
      res.end(JSON.stringify({
        message: '验证码已发送，请查收邮箱',
        email: data.email,
        verification_code: verificationCode,
        note: '邮件服务未启用，此验证码仅用于测试'
      }));
    } catch (e) {
      res.writeHead(400);
      res.end(JSON.stringify({ detail: '请求格式错误' }));
    }
    return;
  }

  // Handle password reset endpoint
  if (req.method === 'POST' && req.url === '/password-reset') {
    res.setHeader('Content-Type', 'application/json');
    
    try {
      const data = await parseBody(req);
      console.log(`Password reset for ${data.email} with code ${data.verification_code}`);
      
      res.writeHead(200);
      res.end(JSON.stringify({
        message: '密码重置成功'
      }));
    } catch (e) {
      res.writeHead(400);
      res.end(JSON.stringify({ detail: '请求格式错误' }));
    }
    return;
  }

  // Handle change password endpoint
  if (req.method === 'POST' && req.url === '/users/me/change-password') {
    const user = getUserFromToken(req);
    if (!user) {
      res.writeHead(401, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '未授权' }));
      return;
    }

    try {
      const data = await parseBody(req);
      
      // Simple check for demo purposes
      if (user.hashed_password !== data.current_password) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ detail: '当前密码错误' }));
        return;
      }
      
      user.hashed_password = data.new_password;
      
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ message: '密码修改成功' }));
    } catch (e) {
      res.writeHead(400, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '请求格式错误' }));
    }
    return;
  }

  // Handle get merchant detail endpoint
  if (req.method === 'GET' && req.url.match(/^\/merchants\/\d+$/)) {
    const merchantId = parseInt(req.url.split('/').pop());
    const merchant = MOCK_MERCHANTS.find(m => m.id === merchantId);
    
    if (!merchant) {
      res.writeHead(404, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ detail: '商家未找到' }));
      return;
    }

    const merchantReviews = MOCK_REVIEWS.filter(r => r.merchant_id === merchantId);
    
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      ...merchant,
      reviews: merchantReviews
    }));
    return;
  }

  // Handle API endpoints for merchants
  if (req.method === 'GET' && req.url.startsWith('/merchants')) {
    res.setHeader('Content-Type', 'application/json');
    
    // Parse query parameters
    const url = new URL(req.url, `http://${req.headers.host}`);
    const category = url.searchParams.get('category');
    const searchQuery = url.searchParams.get('q');
    
    let merchants = MOCK_MERCHANTS;
    
    if (category && category !== '全部') {
      merchants = merchants.filter(m => m.category === category);
    }
    
    if (searchQuery) {
      const lowerQuery = searchQuery.toLowerCase();
      merchants = merchants.filter(m => 
        m.name.toLowerCase().includes(lowerQuery) || 
        m.description.toLowerCase().includes(lowerQuery)
      );
    }
    
    res.writeHead(200);
    res.end(JSON.stringify(merchants));
    return;
  }

  // Handle static files
  let filePath = '.' + req.url;
  if (filePath === './') {
    filePath = './index.html';
  }

  const extname = String(path.extname(filePath)).toLowerCase();
  const contentType = MIME_TYPES[extname] || 'application/octet-stream';

  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/html' });
        res.end('<h1>404 Not Found</h1>', 'utf-8');
      } else {
        res.writeHead(500);
        res.end('Server Error: ' + error.code);
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
});

server.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}/`);
  console.log('Press Ctrl+C to stop the server');
});
