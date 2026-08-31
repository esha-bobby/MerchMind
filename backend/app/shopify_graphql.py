"""
Shopify GraphQL API client for fetching product data.

This module provides an abstraction layer for Shopify's GraphQL API.
Currently uses mock data, but can be easily swapped to real API calls
by adding httpx and configuring Shopify credentials.
"""

from typing import Optional, Any
from pydantic import BaseModel

from app.models.product import Product


class ShopifyVariant(BaseModel):
    """Represents a Shopify product variant (size/color combination)."""
    id: str
    title: str
    options: dict[str, str]  # e.g., {"Size": "M", "Color": "Black"}
    price: float


class ShopifyProduct(BaseModel):
    """Represents a product as returned by Shopify GraphQL API."""
    id: str
    title: str
    description: str
    category: Optional[str] = None
    variants: list[ShopifyVariant]
    images: list[str]  # URLs
    reviews_count: int = 0
    return_policy: Optional[str] = None


# Mock Shopify GraphQL response data
MOCK_SHOPIFY_PRODUCTS = [
    {
        "id": "gid://shopify/Product/1",
        "title": "Nice Shoes",
        "description": "Comfortable and stylish shoes for everyone.",
        "category": "shoes",
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/1",
                "title": "Default",
                "options": {},
                "price": 59.99,
            }
        ],
        "images": [],
        "reviews_count": 0,
        "return_policy": None,
    },
    {
        "id": "gid://shopify/Product/2",
        "title": "Everyday Tote Bag",
        "description": "A useful bag for daily activities.",
        "category": "bags",
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/2a",
                "title": "Black",
                "options": {"Color": "Black"},
                "price": 34.99,
            },
            {
                "id": "gid://shopify/ProductVariant/2b",
                "title": "Blue",
                "options": {"Color": "Blue"},
                "price": 34.99,
            },
        ],
        "images": [],
        "reviews_count": 0,
        "return_policy": None,
    },
    {
        "id": "gid://shopify/Product/3",
        "title": "Fresh Face Cream",
        "description": "A gentle cream for soft, healthy-looking skin.",
        "category": "skincare",
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/3",
                "title": "Default",
                "options": {},
                "price": 24.99,
            }
        ],
        "images": [],
        "reviews_count": 0,
        "return_policy": "30-day returns",
    },
    {
        "id": "gid://shopify/Product/4",
        "title": "Classic Cotton T-Shirt",
        "description": "A comfortable everyday shirt with a regular fit.",
        "category": "clothing",
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/4a",
                "title": "White / S",
                "options": {"Color": "White", "Size": "S"},
                "price": 22.00,
            },
            {
                "id": "gid://shopify/ProductVariant/4b",
                "title": "White / M",
                "options": {"Color": "White", "Size": "M"},
                "price": 22.00,
            },
            {
                "id": "gid://shopify/ProductVariant/4c",
                "title": "White / L",
                "options": {"Color": "White", "Size": "L"},
                "price": 22.00,
            },
            {
                "id": "gid://shopify/ProductVariant/4d",
                "title": "White / XL",
                "options": {"Color": "White", "Size": "XL"},
                "price": 22.00,
            },
            {
                "id": "gid://shopify/ProductVariant/4e",
                "title": "Black / S",
                "options": {"Color": "Black", "Size": "S"},
                "price": 22.00,
            },
            {
                "id": "gid://shopify/ProductVariant/4f",
                "title": "Black / M",
                "options": {"Color": "Black", "Size": "M"},
                "price": 22.00,
            },
            {
                "id": "gid://shopify/ProductVariant/4g",
                "title": "Black / L",
                "options": {"Color": "Black", "Size": "L"},
                "price": 22.00,
            },
            {
                "id": "gid://shopify/ProductVariant/4h",
                "title": "Black / XL",
                "options": {"Color": "Black", "Size": "XL"},
                "price": 22.00,
            },
        ],
        "images": [],
        "reviews_count": 18,
        "return_policy": None,
    },
    {
        "id": "gid://shopify/Product/5",
        "title": "Minimalist Wristwatch",
        "description": "A simple watch with a clean face and adjustable strap.",
        "category": "accessories",
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/5a",
                "title": "Silver",
                "options": {"Color": "Silver"},
                "price": 48.50,
            },
            {
                "id": "gid://shopify/ProductVariant/5b",
                "title": "Brown",
                "options": {"Color": "Brown"},
                "price": 48.50,
            },
        ],
        "images": [],
        "reviews_count": 27,
        "return_policy": "30-day returns",
    },
    {
        "id": "gid://shopify/Product/6",
        "title": "Women's Lightweight Running Shoes",
        "description": "Lightweight running shoes designed for everyday training and road runs. The breathable upper helps keep feet comfortable, while the cushioned sole supports each step.",
        "category": "shoes",
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/6a",
                "title": "Black / 6",
                "options": {"Color": "Black", "Size": "6"},
                "price": 89.99,
            },
            {
                "id": "gid://shopify/ProductVariant/6b",
                "title": "Black / 7",
                "options": {"Color": "Black", "Size": "7"},
                "price": 89.99,
            },
            {
                "id": "gid://shopify/ProductVariant/6c",
                "title": "Black / 8",
                "options": {"Color": "Black", "Size": "8"},
                "price": 89.99,
            },
            {
                "id": "gid://shopify/ProductVariant/6d",
                "title": "Black / 9",
                "options": {"Color": "Black", "Size": "9"},
                "price": 89.99,
            },
            {
                "id": "gid://shopify/ProductVariant/6e",
                "title": "Black / 10",
                "options": {"Color": "Black", "Size": "10"},
                "price": 89.99,
            },
            {
                "id": "gid://shopify/ProductVariant/6f",
                "title": "White / 6",
                "options": {"Color": "White", "Size": "6"},
                "price": 89.99,
            },
            {
                "id": "gid://shopify/ProductVariant/6g",
                "title": "White / 7",
                "options": {"Color": "White", "Size": "7"},
                "price": 89.99,
            },
            {
                "id": "gid://shopify/ProductVariant/6h",
                "title": "White / 8",
                "options": {"Color": "White", "Size": "8"},
                "price": 89.99,
            },
            {
                "id": "gid://shopify/ProductVariant/6i",
                "title": "White / 9",
                "options": {"Color": "White", "Size": "9"},
                "price": 89.99,
            },
            {
                "id": "gid://shopify/ProductVariant/6j",
                "title": "White / 10",
                "options": {"Color": "White", "Size": "10"},
                "price": 89.99,
            },
        ],
        "images": [],
        "reviews_count": 42,
        "return_policy": "30-day returns",
    },
    {
        "id": "gid://shopify/Product/7",
        "title": "Water-Resistant Commuter Backpack",
        "description": "A structured commuter backpack with a padded laptop compartment, two interior pockets, and adjustable shoulder straps. Fits laptops up to 15 inches.",
        "category": "bags",
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/7a",
                "title": "Navy",
                "options": {"Color": "Navy"},
                "price": 74.00,
            },
            {
                "id": "gid://shopify/ProductVariant/7b",
                "title": "Black",
                "options": {"Color": "Black"},
                "price": 74.00,
            },
        ],
        "images": [],
        "reviews_count": 36,
        "return_policy": "30-day returns",
    },
    {
        "id": "gid://shopify/Product/8",
        "title": "Daily Hydrating Face Moisturizer",
        "description": "A fragrance-free moisturizer for normal and dry skin. Use after cleansing in the morning and evening.",
        "category": "skincare",
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/8",
                "title": "Default",
                "options": {},
                "price": 28.00,
            }
        ],
        "images": [],
        "reviews_count": 51,
        "return_policy": "30-day returns",
    },
    {
        "id": "gid://shopify/Product/9",
        "title": "Women's Linen Button-Down Shirt",
        "description": "A relaxed button-down shirt for warm-weather outfits. It has a curved hem, long sleeves, and a relaxed fit.",
        "category": "clothing",
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/9a",
                "title": "White / XS",
                "options": {"Color": "White", "Size": "XS"},
                "price": 64.00,
            },
            {
                "id": "gid://shopify/ProductVariant/9b",
                "title": "White / S",
                "options": {"Color": "White", "Size": "S"},
                "price": 64.00,
            },
            {
                "id": "gid://shopify/ProductVariant/9c",
                "title": "Sage / M",
                "options": {"Color": "Sage", "Size": "M"},
                "price": 64.00,
            },
            {
                "id": "gid://shopify/ProductVariant/9d",
                "title": "Sage / L",
                "options": {"Color": "Sage", "Size": "L"},
                "price": 64.00,
            },
            {
                "id": "gid://shopify/ProductVariant/9e",
                "title": "Blue / XL",
                "options": {"Color": "Blue", "Size": "XL"},
                "price": 64.00,
            },
        ],
        "images": [],
        "reviews_count": 63,
        "return_policy": "60-day returns",
    },
    {
        "id": "gid://shopify/Product/10",
        "title": "Portable Bluetooth Speaker",
        "description": "A compact wireless speaker for indoor and outdoor listening. It connects to phones and tablets through Bluetooth, includes a USB-C charging cable, and plays for up to 12 hours on one charge.",
        "category": "electronics",
        "variants": [
            {
                "id": "gid://shopify/ProductVariant/10a",
                "title": "Black",
                "options": {"Color": "Black"},
                "price": 79.00,
            },
            {
                "id": "gid://shopify/ProductVariant/10b",
                "title": "Red",
                "options": {"Color": "Red"},
                "price": 79.00,
            },
        ],
        "images": [],
        "reviews_count": 88,
        "return_policy": "30-day returns",
    },
]


def _extract_unique_options(variants: list[dict]) -> dict[str, list[str]]:
    """Extract unique option names and values from variants."""
    options_map: dict[str, set[str]] = {}
    
    for variant in variants:
        for key, value in variant.get("options", {}).items():
            if key not in options_map:
                options_map[key] = set()
            options_map[key].add(value)
    
    # Convert sets to sorted lists
    return {k: sorted(list(v)) for k, v in options_map.items()}


def _convert_shopify_to_product(shopify_product: dict[str, Any]) -> Product:
    """Convert Shopify GraphQL product format to internal Product model."""
    variants = shopify_product.get("variants", [])
    
    # Extract sizes and colors from variants
    options = _extract_unique_options(variants)
    
    # Get the minimum price from variants
    prices = [v.get("price", 0) for v in variants]
    price = min(prices) if prices else None
    
    # Extract material if present in variants
    material = None
    # In a real Shopify setup, material might come from product metafields
    
    return Product(
        id=shopify_product["id"].split("/")[-1],  # Convert gid to simple id
        title=shopify_product["title"],
        description=shopify_product["description"],
        category=shopify_product.get("category"),
        price=price,
        material=material,
        sizes=options.get("Size"),
        colors=options.get("Color"),
        reviews=shopify_product.get("reviews_count"),
        return_policy=shopify_product.get("return_policy"),
    )


class ShopifyGraphQLClient:
    """
    Client for Shopify GraphQL API.
    
    Currently uses mock data, but the structure is ready for real API integration.
    To switch to real API:
    1. Add httpx to requirements.txt
    2. Configure SHOPIFY_STORE_NAME and SHOPIFY_ACCESS_TOKEN environment variables
    3. Replace mock data fetching with real GraphQL queries
    """
    
    def __init__(self, store_name: Optional[str] = None, access_token: Optional[str] = None):
        """
        Initialize Shopify client.
        
        Args:
            store_name: Shopify store name (e.g., 'my-store')
            access_token: Shopify access token for authentication
        """
        self.store_name = store_name
        self.access_token = access_token
        self.use_mock = True  # Currently always using mock data
    
    async def fetch_products(self, limit: int = 250) -> list[Product]:
        """
        Fetch products from Shopify GraphQL API.
        
        Args:
            limit: Maximum number of products to fetch
            
        Returns:
            List of Product objects
        """
        if self.use_mock:
            # Mock data implementation
            shopify_products = MOCK_SHOPIFY_PRODUCTS[:limit]
        else:
            # Real API implementation (future)
            # import httpx
            # query = """
            # query {
            #   products(first: $limit) {
            #     edges {
            #       node {
            #         id
            #         title
            #         description
            #         ...
            #       }
            #     }
            #   }
            # }
            # """
            # async with httpx.AsyncClient() as client:
            #     response = await client.post(...)
            shopify_products = []
        
        # Convert Shopify products to internal Product model
        products = [_convert_shopify_to_product(sp) for sp in shopify_products]
        
        return products
    
    def fetch_products_sync(self, limit: int = 250) -> list[Product]:
        """Synchronous version of fetch_products (for FastAPI compatibility)."""
        if self.use_mock:
            shopify_products = MOCK_SHOPIFY_PRODUCTS[:limit]
        else:
            shopify_products = []
        
        products = [_convert_shopify_to_product(sp) for sp in shopify_products]
        
        return products


# Global client instance
_shopify_client: Optional[ShopifyGraphQLClient] = None


def get_shopify_client() -> ShopifyGraphQLClient:
    """Get or create the global Shopify client."""
    global _shopify_client
    if _shopify_client is None:
        _shopify_client = ShopifyGraphQLClient()
    return _shopify_client
