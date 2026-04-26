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
    price: "￥120/人"
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
    price: "￥388/人"
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
    price: "￥65/人"
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
    price: "免费"
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
    price: "￥199/月"
  }
];

const MOCK_REVIEWS = [
  {
    id: 1,
    merchant_id: 1,
    user: "张三",
    rating: 5,
    content: "羊肉真的很新鲜，汤底也很鲜美，下次还会再来！",
    date: "2024-03-20"
  },
  {
    id: 2,
    merchant_id: 1,
    user: "李四",
    rating: 4,
    content: "味道不错，就是人比较多，需要排队。",
    date: "2024-03-15"
  },
  {
    id: 3,
    merchant_id: 2,
    user: "王五",
    rating: 5,
    content: "非常放松的一次体验，技师很专业，环境也很好。",
    date: "2024-03-22"
  }
];
