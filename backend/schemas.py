from __future__ import annotations
from typing import Optional, List
from pydantic import BaseModel, Field

# Each model here maps to a Mongo collection named after the class (lowercased)

class Testimonial(BaseModel):
    name: str
    role: Optional[str] = None
    message: str
    rating: int = Field(ge=1, le=5, default=5)

class Service(BaseModel):
    title: str
    description: str
    category: Optional[str] = None
    price_from: Optional[float] = None

class Course(BaseModel):
    title: str
    summary: str
    level: Optional[str] = None
    price: Optional[float] = None
    tags: Optional[List[str]] = None

class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True

class AuditRequest(BaseModel):
    website_url: str
    email: str
    message: Optional[str] = None
