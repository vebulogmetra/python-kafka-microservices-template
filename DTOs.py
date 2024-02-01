from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class OrderDetails(BaseModel):
    price: float
    quantity: int


class OrderModel(BaseModel):
    user_id: str
    order_id: str
    user_email: str
    order_details: OrderDetails
    created_at: Optional[datetime | str] = None
    status: Optional[str] = "not confirmed"
