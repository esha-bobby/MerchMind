import json
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.product import Product


MOCK_DATA_PATH = Path(__file__).resolve().parents[2] / "mock_data" / "products.json"

app = FastAPI(
    title="Kasparro AI Readiness Auditor API",
    description="Backend foundation for auditing Shopify product readiness for AI shopping assistants.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Kasparro API is running"}


@app.get("/api/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/products", response_model=list[Product])
def list_products() -> list[Product]:
    products_data = json.loads(MOCK_DATA_PATH.read_text())
    return [Product(**product_data) for product_data in products_data]


@app.post("/api/audit", response_model=Product)
def audit_product(product: Product) -> Product:
    return product
