from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas import BatchCreate, BatchOut
from core.deps import get_db, require_role
from models import Batch, Product, User
from services.blockchain_service import BlockchainService

router = APIRouter()

_bc = BlockchainService()


@router.post("", response_model=BatchOut)
def create_batch(
    payload: BatchCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("farmer", "admin")),
):
    product = db.query(Product).filter(Product.id == payload.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if user.role.value == "farmer" and product.farmer_id != user.id:
        raise HTTPException(status_code=403, detail="You can only create batches for your own products")

    if db.query(Batch).filter(Batch.batch_number == payload.batch_number).first():
        raise HTTPException(status_code=400, detail="batch_number already exists")

    # Anchor to blockchain
    anchor = _bc.anchor(
        {
            "type": "batch_create",
            "batch_number": payload.batch_number,
            "product_id": payload.product_id,
            "farmer_id": product.farmer_id,
            "quantity": payload.quantity,
        }
    )

    batch = Batch(
        batch_number=payload.batch_number,
        product_id=payload.product_id,
        quantity=payload.quantity,
        production_date=payload.production_date,
        expiry_date=payload.expiry_date,
        blockchain_hash=anchor["block_hash"],
        blockchain_timestamp=anchor["timestamp"],
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


@router.get("", response_model=List[BatchOut])
def list_batches(db: Session = Depends(get_db)):
    return db.query(Batch).order_by(Batch.created_at.desc()).all()


@router.get("/{batch_id}", response_model=BatchOut)
def get_batch(batch_id: int, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.id == batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch
