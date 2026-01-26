from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


# -------- Auth / User --------
class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)
    role: str = Field(default="consumer", description="consumer | farmer | admin")


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    phone: Optional[str] = None
    address: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


# -------- Product --------
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    stock: int = 0
    unit: str = "kg"
    origin: Optional[str] = None
    organic_certified: bool = False
    planting_date: Optional[datetime] = None
    harvest_date: Optional[datetime] = None
    image_url: Optional[str] = None


class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: float
    stock: int
    unit: str
    origin: Optional[str] = None
    organic_certified: bool
    farmer_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


# -------- Batch / Trace --------
class BatchCreate(BaseModel):
    product_id: int
    batch_number: str = Field(min_length=3, max_length=100)
    quantity: float
    production_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None


class BatchOut(BaseModel):
    id: int
    batch_number: str
    product_id: int
    quantity: float
    production_date: Optional[datetime] = None
    expiry_date: Optional[datetime] = None
    blockchain_hash: Optional[str] = None
    blockchain_timestamp: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TraceEventCreate(BaseModel):
    batch_id: int
    event_type: str = Field(description="planting|fertilizing|harvest|inspection|transport|warehouse|sale ...")
    event_time: datetime
    location: Optional[str] = None
    operator: Optional[str] = None
    description: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None


class TraceEventOut(BaseModel):
    id: int
    batch_id: int
    event_type: str
    event_time: datetime
    location: Optional[str] = None
    operator: Optional[str] = None
    description: Optional[str] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    blockchain_hash: Optional[str] = None
    blockchain_timestamp: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TraceTimelineOut(BaseModel):
    batch: BatchOut
    product: ProductOut
    events: List[TraceEventOut]
    chain_valid: bool
