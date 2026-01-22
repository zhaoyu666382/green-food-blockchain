from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging
from config import settings

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="绿色食品交易平台API",
    description="基于区块链的绿色食品溯源与交易平台",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 日志中间件
@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"请求路径: {request.url.path} | 方法: {request.method}")
    start_time = datetime.now()
    
    response = await call_next(request)
    
    process_time = (datetime.now() - start_time).total_seconds()
    logger.info(f"完成请求: {request.url.path} | 耗时: {process_time:.3f}秒 | 状态码: {response.status_code}")
    
    return response

# 健康检查接口
@app.get("/health", tags=["系统"])
async def health_check():
    """
    健康检查接口
    返回系统运行状态
    """
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "service": "绿色食品交易平台",
        "version": "1.0.0"
    }

# 根路径
@app.get("/", tags=["系统"])
async def root():
    """
    API根路径
    """
    return {
        "message": "欢迎使用绿色食品交易平台API",
        "docs": "/docs",
        "health": "/health"
    }

# 用户相关接口（示例）
@app.get("/api/users", tags=["用户管理"])
async def get_users():
    """
    获取用户列表
    """
    return {"message": "用户列表接口"}

@app.post("/api/users/register", tags=["用户管理"])
async def register_user():
    """
    用户注册接口
    """
    return {"message": "用户注册接口"}

# 产品相关接口（示例）
@app.get("/api/products", tags=["产品管理"])
async def get_products():
    """
    获取产品列表
    """
    return {"message": "产品列表接口"}

@app.post("/api/products", tags=["产品管理"])
async def create_product():
    """
    创建产品接口
    """
    return {"message": "创建产品接口"}

# 溯源相关接口（示例）
@app.get("/api/trace/{batch_id}", tags=["区块链溯源"])
async def get_trace_info(batch_id: str):
    """
    获取批次溯源信息
    """
    return {
        "batch_id": batch_id,
        "message": "溯源信息接口"
    }

# 订单相关接口（示例）
@app.get("/api/orders", tags=["订单管理"])
async def get_orders():
    """
    获取订单列表
    """
    return {"message": "订单列表接口"}

@app.post("/api/orders", tags=["订单管理"])
async def create_order():
    """
    创建订单接口
    """
    return {"message": "创建订单接口"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
