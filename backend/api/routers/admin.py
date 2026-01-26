from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.deps import get_db, require_role
from models import User, Product, Batch, TraceEvent

router = APIRouter()


@router.get("/stats")
def stats(db: Session = Depends(get_db), user: User = Depends(require_role("admin"))):
    """系统统计（管理员）"""
    users = db.query(User).count()
    products = db.query(Product).count()
    batches = db.query(Batch).count()
    events = db.query(TraceEvent).count()
    return {"users": users, "products": products, "batches": batches, "events": events}


@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    user: User = Depends(require_role("admin")),
    q: Optional[str] = Query(default=None, description="按用户名/邮箱搜索"),
):
    query = db.query(User)
    if q:
        like = f"%{q}%"
        query = query.filter((User.username.ilike(like)) | (User.email.ilike(like)))
    # 只返回必要字段（避免泄露密码等）
    rows = query.order_by(User.created_at.desc()).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role.value if hasattr(u.role, "value") else str(u.role),
            "is_active": u.is_active,
            "created_at": u.created_at,
        }
        for u in rows
    ]
