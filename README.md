# 绿色食品交易平台（区块链溯源示例）

本仓库是一个**面向学生、教学友好**的绿色食品交易与区块链溯源平台示例项目。
项目以“绿色食品 + 区块链溯源”为核心思想，后端基于 **FastAPI**，通过本地轻量级区块链实现食品批次与流转信息的可信存证。

后端主要功能包括：

* 用户注册与 JWT 登录认证
* 产品管理（农户 / 管理员）
* 食品批次创建（数据锚定至区块链）
* 溯源事件记录（上链存证）
* 基于 `batch_number` 的公众溯源时间线查询

> ⚠️ 说明：
> 当前使用的是**本地轻量级区块链实现**，主要用于教学演示与课程设计。
> 在后续阶段可替换为 **Hyperledger Fabric / IPFS / 联盟链** 等真实区块链方案。

---

## 项目结构说明

```
green-food-blockchain-main/
├── backend/                      # FastAPI 后端服务
│   ├── app.py                    # 项目入口
│   ├── config.py                 # 配置文件（支持 .env）
│   ├── database.py               # SQLAlchemy 数据库连接
│   ├── models.py                 # ORM 数据模型
│   ├── api/
│   │   ├── router.py             # API 总路由
│   │   ├── schemas.py            # Pydantic 数据校验模型
│   │   └── routers/
│   │       ├── auth.py            # 用户注册 / 登录
│   │       ├── products.py        # 产品管理
│   │       ├── batches.py         # 批次管理
│   │       └── trace.py           # 溯源相关接口
│   ├── core/
│   │   ├── deps.py               # 认证依赖
│   │   └── security.py           # 密码加密 / JWT 工具
│   ├── services/
│   │   └── blockchain_service.py # 区块链存储与锚定逻辑
│   └── requirements.txt          # Python 依赖列表
├── blockchain/
│   └── blockchain.py             # 本地 PoW 区块链实现
└── frontend/                     # Vue3 前端模板（管理员 / 农户 / 消费者）
```

---

## 快速开始（后端）

### 1️⃣ 创建虚拟环境并安装依赖

```bash
cd green-food-blockchain-main/backend
python -m venv .venv

# Windows 激活虚拟环境
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

---

### 2️⃣ 配置环境变量（可选）

默认配置已写在 `backend/config.py` 中，可直接运行。
如果用于正式部署，建议在 `.env` 文件中修改：

* `SECRET_KEY`（JWT 密钥）

---

### 3️⃣ 启动后端服务

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

启动后可访问：

* 📘 Swagger 接口文档
  `http://localhost:8000/docs`

相关数据文件：

* 📂 SQLite 数据库：
  `backend/green_food.db`

* ⛓️ 区块链账本文件：
  `backend/data/blockchain_chain.json`

---

## 示例 API 调用（curl）

### 用户注册（农户角色）

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"farmer1","email":"farmer1@example.com","password":"123456","role":"farmer"}'
```

---

### 用户登录

```bash
TOKEN=$(curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=farmer1&password=123456" | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

echo $TOKEN
```

---

### 创建产品

```bash
curl -X POST http://localhost:8000/api/products \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Organic Spinach","category":"vegetable","price":9.9,"stock":50,"unit":"kg","origin":"Jiangxi"}'
```

---

### 创建食品批次（写入区块链）

```bash
curl -X POST http://localhost:8000/api/batches \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id":1,"batch_number":"BATCH-2026-0001","quantity":20}'
```

---

### 添加溯源事件（上链存证）

```bash
curl -X POST http://localhost:8000/api/trace/events \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"batch_id":1,"event_type":"inspection","event_time":"2026-01-01T10:00:00","location":"Lab A","description":"农残检测合格"}'
```

---

### 公众溯源时间线查询

```bash
curl http://localhost:8000/api/trace/timeline/BATCH-2026-0001
```

---

## 后续可扩展方向（Roadmap）

* 订单 / 支付 / 物流模块集成
* 基于 `batch_number` 的二维码生成
* 使用 Hyperledger Fabric 替换本地区块链
* 支持图片 / 检测报告等溯源附件上传
* 推荐系统（独立微服务）

