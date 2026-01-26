from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas import TraceEventCreate, TraceEventOut, TraceTimelineOut, BatchOut, ProductOut
from core.deps import get_db, require_role
from models import TraceEvent, Batch, Product, User
from services.blockchain_service import BlockchainService

router = APIRouter()

_bc = BlockchainService()


@router.post("/events", response_model=TraceEventOut)
def create_trace_event(
    payload: TraceEventCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_role("farmer", "admin")),
):
    batch = db.query(Batch).filter(Batch.id == payload.batch_id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    product = db.query(Product).filter(Product.id == batch.product_id).first()
    if user.role.value == "farmer" and product and product.farmer_id != user.id:
        raise HTTPException(status_code=403, detail="You can only add events for your own batches")

    anchor = _bc.anchor(
        {
            "type": "trace_event",
            "batch_number": batch.batch_number,
            "event_type": payload.event_type,
            "event_time": payload.event_time.isoformat(),
            "location": payload.location,
            "operator": payload.operator or user.username,
        }
    )

    event = TraceEvent(
        batch_id=payload.batch_id,
        event_type=payload.event_type,
        event_time=payload.event_time,
        location=payload.location,
        operator=payload.operator or user.username,
        description=payload.description,
        temperature=payload.temperature,
        humidity=payload.humidity,
        blockchain_hash=anchor["block_hash"],
        blockchain_timestamp=anchor["timestamp"],
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


@router.get("/timeline/{batch_number}", response_model=TraceTimelineOut)
def trace_timeline(batch_number: str, db: Session = Depends(get_db)):
    batch = db.query(Batch).filter(Batch.batch_number == batch_number).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    product = db.query(Product).filter(Product.id == batch.product_id).first()
    events = (
        db.query(TraceEvent)
        .filter(TraceEvent.batch_id == batch.id)
        .order_by(TraceEvent.event_time.asc())
        .all()
    )

    return TraceTimelineOut(
        batch=batch,
        product=product,
        events=events,
        chain_valid=_bc.verify_chain(),
    )
