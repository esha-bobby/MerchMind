from typing import List, Optional

from pydantic import BaseModel, Field


class Product(BaseModel):
    id: str
    title: str
    description: str
    category: Optional[str] = None
    price: Optional[float] = Field(default=None, ge=0)
    material: Optional[str] = None
    sizes: Optional[List[str]] = None
    colors: Optional[List[str]] = None
    reviews: Optional[int] = Field(default=None, ge=0)
    return_policy: Optional[str] = None
