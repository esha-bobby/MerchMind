from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.product import Product
from app.audit import audit_product, AuditResult
from app.shopify_graphql import get_shopify_client


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
    shopify_client = get_shopify_client()
    return shopify_client.fetch_products_sync()


@app.post("/api/audit", response_model=AuditResult)
def audit_product_endpoint(product: Product) -> AuditResult:
    return audit_product(product)
