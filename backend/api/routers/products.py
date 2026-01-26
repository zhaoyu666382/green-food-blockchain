from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from api.schemas import ProductCreate, ProductOut
from core.deps import get_db, get_current_user, require_role
from models import Product, User

router = APIRouter()


@router.get("", response_model=List[ProductOut])
def list_products(
    db: Session = Depends(get_db),
    q: Optional[str] = Query(default=None, description="Search by name/category"),
    category: Optional[str] = None,
    active_only: bool = True,
):
    query = db.query(Product)
    if active_only:
        query = query.filter(Product.is_active == True)  # noqa
    if q:
        like = f"%{q}%"
        query = query.filter((Product.name.ilike(like)) | (Product.category.ilike(like)))
    if category:
        query = query.filter(Product.category == category)
    return query.order_by(Product.created_at.desc()).all()


@router.post("", response_model=ProductOut)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("farmer", "admin")),
):
    product = Product(
        name=payload.name,
        description=payload.description,
        category=payload.category,
        price=payload.price,
        stock=payload.stock,
        unit=payload.unit,
        origin=payload.origin,
        organic_certified=payload.organic_certified,
        planting_date=payload.planting_date,
        harvest_date=payload.harvest_date,
        image_url=payload.image_url,
        farmer_id=user.id,
        is_active=True,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
