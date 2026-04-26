-- ==========================================
-- 初始化数据脚本
-- ==========================================

-- 1. 初始化角色
INSERT INTO public.roles (role_name, description) VALUES
('admin', '系统管理员'),
('merchant', '商家管理员'),
('user', '普通用户')
ON CONFLICT (role_name) DO NOTHING;

-- 2. 初始化评价标签
INSERT INTO public.review_tags (tag_name, category) VALUES
('口味赞', '美食'),
('服务周到', '服务'),
('环境优雅', '环境'),
('性价比高', '综合'),
('交通便利', '位置'),
('技师专业', '休闲娱乐')
ON CONFLICT (tag_name) DO NOTHING;

-- 3. 初始化数据字典 (商家状态示例)
INSERT INTO public.data_dictionaries (dict_code, dict_label, dict_value, sort_order, is_system) VALUES
('MERCHANT_STATUS', '待审核', 'pending', 1, true),
('MERCHANT_STATUS', '正常营业', 'active', 2, true),
('MERCHANT_STATUS', '暂停营业', 'closed', 3, true),
('MERCHANT_STATUS', '审核拒绝', 'rejected', 4, true)
ON CONFLICT (dict_code, dict_value) DO NOTHING;

-- 4. 初始化系统配置
INSERT INTO public.system_configs (config_key, config_value, description) VALUES
('SITE_NAME', '大众生活', '网站名称'),
('MAX_REVIEW_IMAGES', '9', '单条评价最大图片数量'),
('ENABLE_AUTO_AUDIT', 'false', '是否开启商家自动审核')
ON CONFLICT (config_key) DO NOTHING;

-- 5. 初始化商家数据 (显式指定 ID 并包含地理位置信息)
INSERT INTO public.merchants (id, name, description, address, category, phone, rating, reviews_count, image_url, price, status, location)
VALUES 
(1, '老北京涮肉', '地道的北京风味涮羊肉，传统铜锅，羊肉鲜嫩。', '朝阳区三里屯1号', '美食', '010-12345678', 4.8, 1250, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=800&auto=format&fit=crop', '￥120/人', 'active', ST_GeographyFromText('POINT(116.4551 39.9385)')),
(2, '悦己SPA', '高端水疗体验，放松身心，技师手法专业。', '海淀区中关村大街2号', '休闲娱乐', '010-87654321', 4.9, 850, 'https://images.unsplash.com/photo-1600334129128-685c5582fd35?w=800&auto=format&fit=crop', '￥388/人', 'active', ST_GeographyFromText('POINT(116.3214 39.9813)')),
(3, '光影电影院', 'IMAX巨幕，极致视听享受，环境舒适。', '朝阳区大望路3号', '电影', '010-13572468', 4.5, 3200, 'https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=800&auto=format&fit=crop', '￥65/人', 'active', ST_GeographyFromText('POINT(116.4801 39.9135)')),
(4, '书香苑图书馆', '安静的学习环境，海量图书，提供免费咖啡。', '西城区阜成门外大街5号', '文化生活', '010-24681357', 4.7, 450, 'https://images.unsplash.com/photo-1507842217343-583bb7270b66?w=800&auto=format&fit=crop', '免费', 'active', ST_GeographyFromText('POINT(116.3532 39.9211)')),
(5, '极速健身房', '器械齐全，专业私教，24小时营业。', '朝阳区望京SOHO 8号', '运动健康', '010-11223344', 4.6, 670, 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&auto=format&fit=crop', '￥199/月', 'active', ST_GeographyFromText('POINT(116.4812 40.0012)'))
ON CONFLICT (id) DO UPDATE SET 
    name = EXCLUDED.name,
    description = EXCLUDED.description,
    address = EXCLUDED.address,
    category = EXCLUDED.category,
    phone = EXCLUDED.phone,
    rating = EXCLUDED.rating,
    reviews_count = EXCLUDED.reviews_count,
    image_url = EXCLUDED.image_url,
    price = EXCLUDED.price,
    status = EXCLUDED.status,
    location = EXCLUDED.location;

-- 重置 ID 自增序列
SELECT setval('merchants_id_seq', (SELECT MAX(id) FROM merchants));
