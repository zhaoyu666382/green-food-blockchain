# 绿色食品交易平台

## 项目简介

基于区块链的绿色食品溯源与交易平台，实现从种植到销售的全流程透明化。通过 Hyperledger Fabric 整合全流程数据，引入 ZKP 与 IPFS 保障数据真实与隐私合规，实现可信溯源。

**开发团队**：赵钰（后端+区块链） + 彭依娜（前端三端）

**指导老师**：王同罕

**所属学校**：东华理工大学信息工程学院

## 技术栈

- **后端**：FastAPI + SQLAlchemy
- **数据库**：SQLite (开发) / PostgreSQL (生产)
- **区块链**：自研轻量级区块链 / Hyperledger Fabric
- **前端**：Vue3 + Vite + Element Plus

## 项目结构

```
green-food-platform/
├── backend/                    # 后端代码
│   ├── app.py                 # FastAPI主应用
│   ├── config.py              # 配置文件
│   ├── database.py            # 数据库连接
│   ├── models.py              # 数据模型
│   ├── .env                   # 环境变量
│   └── requirements.txt       # Python依赖
├── frontend/                  # 前端代码
│   ├── consumer/             # 用户端
│   ├── farmer/               # 农户端
│   └── admin/                # 管理后台
├── blockchain/               # 区块链代码
│   └── blockchain.py         # 区块链核心
├── docs/                     # 文档
│   └── api-v0.md            # API文档
└── scripts/                  # 部署脚本
```


## 团队分工

- **赵钰**：后端开发、区块链搭建、项目架构
- **彭依娜**：前端三端开发、UI设计
