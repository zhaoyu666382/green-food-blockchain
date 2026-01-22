from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, Enum, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class UserRole(enum.Enum):
    """用户角色枚举"""
    CONSUMER = "consumer"  # 消费者
    FARMER = "farmer"      # 农户
    ADMIN = "admin"        # 管理员

class OrderStatus(enum.Enum):
    """订单状态枚举"""
    PENDING = "pending"         # 待支付
    PAID = "paid"              # 已支付
    SHIPPED = "shipped"        # 已发货
    DELIVERED = "delivered"    # 已送达
    COMPLETED = "completed"    # 已完成
    CANCELLED = "cancelled"    # 已取消

class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.CONSUMER)
    phone = Column(String(20))
    address = Column(Text)
    avatar = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    products = relationship("Product", back_populates="farmer")
    orders = relationship("Order", back_populates="user")

class Product(Base):
    """产品模型"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    category = Column(String(50))  # 蔬菜类别
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    unit = Column(String(20), default="kg")  # 单位：kg, 斤, 个
    image_url = Column(String(255))
    farmer_id = Column(Integer, ForeignKey("users.id"))
    
    # 产品属性
    origin = Column(String(100))  # 产地
    organic_certified = Column(Boolean, default=False)  # 是否有机认证
    planting_date = Column(DateTime)  # 种植日期
    harvest_date = Column(DateTime)   # 采摘日期
    
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    farmer = relationship("User", back_populates="products")
    batches = relationship("Batch", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class Batch(Base):
    """批次模型（用于溯源）"""
    __tablename__ = "batches"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_number = Column(String(100), unique=True, nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    
    # 批次信息
    quantity = Column(Float)  # 数量
    production_date = Column(DateTime)  # 生产日期
    expiry_date = Column(DateTime)      # 过期日期
    
    # 区块链信息
    blockchain_hash = Column(String(255))  # 区块链哈希
    blockchain_timestamp = Column(DateTime)
    
    qr_code = Column(String(255))  # 二维码路径
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    product = relationship("Product", back_populates="batches")
    trace_events = relationship("TraceEvent", back_populates="batch")

class TraceEvent(Base):
    """溯源事件模型"""
    __tablename__ = "trace_events"
    
    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("batches.id"))
    
    event_type = Column(String(50))  # 事件类型：种植、施肥、采摘、检测、运输等
    event_time = Column(DateTime, nullable=False)
    location = Column(String(200))   # 地点
    operator = Column(String(100))   # 操作人
    description = Column(Text)       # 描述
    
    # 环境数据
    temperature = Column(Float)      # 温度
    humidity = Column(Float)         # 湿度
    
    # 附件
    images = Column(Text)  # JSON格式存储图片URLs
    documents = Column(Text)  # JSON格式存储文档URLs
    
    # 区块链信息
    blockchain_hash = Column(String(255))
    blockchain_timestamp = Column(DateTime)
    
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    batch = relationship("Batch", back_populates="trace_events")

class Order(Base):
    """订单模型"""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(100), unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # 订单信息
    total_amount = Column(Float, nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    payment_method = Column(String(50))  # 支付方式
    
    # 收货信息
    receiver_name = Column(String(100))
    receiver_phone = Column(String(20))
    receiver_address = Column(Text)
    
    # 物流信息
    shipping_company = Column(String(100))
    tracking_number = Column(String(100))
    shipped_at = Column(DateTime)
    delivered_at = Column(DateTime)
    
    # 备注
    remark = Column(Text)
    
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # 关系
    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    """订单项模型"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    created_at = Column(DateTime, default=datetime.now)
    
    # 关系
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")
