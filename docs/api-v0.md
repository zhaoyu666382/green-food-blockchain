# 绿色食品交易平台 API 文档 V0.1

## 基本信息

- **基础URL**: `http://localhost:8000`
- **版本**: 1.0.0
- **文档生成时间**: 2025-01-22

## 自动生成文档

访问 Swagger UI 查看完整的交互式API文档：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 接口列表

### 1. 系统接口

#### 1.1 健康检查
```
GET /health
```

**响应示例**:
```json
{
  "status": "ok",
  "timestamp": "2025-01-22T10:30:00",
  "service": "绿色食品交易平台",
  "version": "1.0.0"
}
```

#### 1.2 根路径
```
GET /
```

**响应示例**:
```json
{
  "message": "欢迎使用绿色食品交易平台API",
  "docs": "/docs",
  "health": "/health"
}
```

---

### 2. 用户管理接口

#### 2.1 用户注册
```
POST /api/users/register
```

**请求体**:
```json
{
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "password": "password123",
  "phone": "13800138000",
  "role": "consumer"
}
```

**响应示例**:
```json
{
  "id": 1,
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "role": "consumer",
  "created_at": "2025-01-22T10:30:00"
}
```

#### 2.2 用户登录
```
POST /api/users/login
```

**请求体**:
```json
{
  "username": "zhangsan",
  "password": "password123"
}
```

**响应示例**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "zhangsan",
    "role": "consumer"
  }
}
```

#### 2.3 获取用户列表
```
GET /api/users
```

**查询参数**:
- `page`: 页码（默认1）
- `size`: 每页数量（默认10）
- `role`: 角色筛选（可选）

**响应示例**:
```json
{
  "total": 100,
  "page": 1,
  "size": 10,
  "data": [
    {
      "id": 1,
      "username": "zhangsan",
      "email": "zhangsan@example.com",
      "role": "consumer"
    }
  ]
}
```

---

### 3. 产品管理接口

#### 3.1 获取产品列表
```
GET /api/products
```

**查询参数**:
- `page`: 页码
- `size`: 每页数量
- `category`: 分类筛选
- `organic_certified`: 是否有机认证

**响应示例**:
```json
{
  "total": 50,
  "data": [
    {
      "id": 1,
      "name": "有机白菜",
      "description": "新鲜有机白菜",
      "category": "叶菜类",
      "price": 8.5,
      "stock": 100,
      "unit": "kg",
      "organic_certified": true,
      "origin": "江西南昌"
    }
  ]
}
```

#### 3.2 创建产品
```
POST /api/products
```

**请求头**:
```
Authorization: Bearer <token>
```

**请求体**:
```json
{
  "name": "有机白菜",
  "description": "新鲜有机白菜",
  "category": "叶菜类",
  "price": 8.5,
  "stock": 100,
  "unit": "kg",
  "origin": "江西南昌",
  "organic_certified": true,
  "planting_date": "2025-01-01"
}
```

#### 3.3 获取产品详情
```
GET /api/products/{id}
```

#### 3.4 更新产品
```
PUT /api/products/{id}
```

#### 3.5 删除产品
```
DELETE /api/products/{id}
```

---

### 4. 区块链溯源接口

#### 4.1 获取批次溯源信息
```
GET /api/trace/{batch_id}
```

**响应示例**:
```json
{
  "batch_id": "BATCH-2025-001",
  "product_name": "有机白菜",
  "blockchain_hash": "a3f5d8c2b1e4...",
  "trace_events": [
    {
      "event_type": "种植",
      "event_time": "2025-01-01T08:00:00",
      "location": "江西省南昌市",
      "operator": "张三",
      "description": "开始种植",
      "blockchain_hash": "b2c4e6f8a1d3..."
    },
    {
      "event_type": "采摘",
      "event_time": "2025-01-20T10:00:00",
      "location": "江西省南昌市",
      "operator": "李四",
      "description": "完成采摘"
    }
  ]
}
```

#### 4.2 添加溯源事件
```
POST /api/trace/event
```

**请求体**:
```json
{
  "batch_id": "BATCH-2025-001",
  "event_type": "运输",
  "location": "南昌-赣州",
  "operator": "王五",
  "description": "冷链运输",
  "temperature": 4.5,
  "humidity": 85.0
}
```

#### 4.3 扫码溯源
```
GET /api/trace/scan/{qr_code}
```

---

### 5. 订单管理接口

#### 5.1 创建订单
```
POST /api/orders
```

**请求体**:
```json
{
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    }
  ],
  "receiver_name": "张三",
  "receiver_phone": "13800138000",
  "receiver_address": "江西省南昌市XX路XX号"
}
```

#### 5.2 获取订单列表
```
GET /api/orders
```

#### 5.3 获取订单详情
```
GET /api/orders/{id}
```

#### 5.4 更新订单状态
```
PUT /api/orders/{id}/status
```

**请求体**:
```json
{
  "status": "shipped",
  "tracking_number": "SF1234567890"
}
```

---

## 状态码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 201 | 创建成功 |
| 400 | 请求参数错误 |
| 401 | 未授权 |
| 403 | 禁止访问 |
| 404 | 资源不存在 |
| 500 | 服务器错误 |

## 错误响应格式

```json
{
  "detail": "错误信息描述"
}
```

## 认证说明

需要认证的接口需要在请求头中携带JWT token：

```
Authorization: Bearer <your_token_here>
```

## 接口变更记录

### V0.1 (2025-01-22)
- 初始版本
- 实现健康检查接口
- 定义核心API结构

### 待实现功能
- [ ] 用户认证与授权
- [ ] 产品CRUD完整实现
- [ ] 文件上传接口
- [ ] 支付接口
- [ ] 推荐系统接口
- [ ] 病虫害识别接口

## 注意事项

1. 所有时间格式统一使用ISO 8601格式
2. 所有金额单位为人民币（元）
3. 分页从第1页开始
4. 删除操作为软删除，不会真正删除数据

---

**文档维护**: 赵钰  
**最后更新**: 2025-01-22
