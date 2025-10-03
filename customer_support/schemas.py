"""Pydantic schemas for structured agent responses."""

from typing import List
from pydantic import BaseModel, Field


class OrderItem(BaseModel):
    """Individual item in an order."""
    
    product_name: str = Field(description="Name of the product")
    quantity: int = Field(description="Quantity ordered")
    price: float = Field(description="Price per unit")


class OrderInfo(BaseModel):
    """Order information schema - returned by order_lookup agent."""
    
    order_id: str = Field(description="Unique order identifier")
    customer_name: str = Field(description="Customer name")
    order_date: str = Field(description="Order date (YYYY-MM-DD)")
    status: str = Field(description="Order status (pending/shipped/delivered/cancelled)")
    items: List[OrderItem] = Field(description="List of items in the order")
    total_amount: float = Field(description="Total order amount")
    shipping_address: str = Field(description="Shipping address")
    tracking_number: str = Field(description="Tracking number if shipped", default="N/A")


class RefundResult(BaseModel):
    """Refund processing result - returned by refund_processor agent."""
    
    refund_id: str = Field(description="Unique refund identifier")
    order_id: str = Field(description="Associated order ID")
    status: str = Field(description="Refund status (approved/rejected/pending)")
    refund_amount: float = Field(description="Refund amount")
    reason: str = Field(description="Reason for refund decision")
    processing_time: str = Field(description="Expected processing time")
    refund_method: str = Field(description="Refund method (original payment/store credit)")
