from fastapi import APIRouter

from api.routers import auth, products, batches, trace, admin

api_router = APIRouter(prefix="/api")

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(products.router, prefix="/products", tags=["产品"])
api_router.include_router(batches.router, prefix="/batches", tags=["批次"])
api_router.include_router(trace.router, prefix="/trace", tags=["溯源"])

api_router.include_router(admin.router, prefix="/admin", tags=["管理"])
