"""
Audit service for checking product readiness for AI shopping assistants.
"""

from typing import Optional
from pydantic import BaseModel

from app.models.product import Product


class FieldStatus(BaseModel):
    """Status of a single product field."""
    field_name: str
    present: bool
    quality: str  # "good", "vague", "missing"
    feedback: Optional[str] = None


class AuditResult(BaseModel):
    """Complete audit report for a product."""
    product_id: str
    product_title: str
    readiness_score: float  # 0-100
    field_checks: list[FieldStatus]
    description_quality: str  # "clear", "vague", "missing"
    missing_critical_fields: list[str]
    recommendations: list[str]
    summary: str


# Vague language patterns to detect poor descriptions
VAGUE_WORDS = {
    "nice", "good", "great", "beautiful", "perfect", "amazing",
    "wonderful", "lovely", "premium", "quality", "nice quality",
    "high quality", "best", "awesome", "fantastic", "excellent"
}

# Fields that are typically important for AI shopping assistants
CRITICAL_FIELDS = ["title", "description", "price", "category"]
IMPORTANT_FIELDS = ["material", "sizes", "colors", "return_policy"]


def _is_vague_description(description: Optional[str]) -> bool:
    """Check if description contains vague language without specifics."""
    if not description:
        return True
    
    description_lower = description.lower()
    
    # Count vague words
    vague_count = sum(1 for word in VAGUE_WORDS if word in description_lower)
    
    # Check for specific information indicators
    has_dimensions = any(word in description_lower for word in ["cm", "inch", "mm", "width", "height", "length"])
    has_material_info = any(word in description_lower for word in ["cotton", "polyester", "leather", "silk", "wood", "plastic", "metal", "steel"])
    has_quantity_info = any(word in description_lower for word in ["pack", "set", "count", "quantity", "pieces"])
    has_color_info = "color" in description_lower or any(color in description_lower for color in ["black", "white", "blue", "red", "green"])
    
    has_specifics = has_dimensions or has_material_info or has_quantity_info or has_color_info
    
    # If mostly vague words and no specific details, it's vague
    if vague_count >= 2 and not has_specifics:
        return True
    
    # If description is too short (less than 30 chars) and has vague words
    if len(description) < 30 and vague_count > 0:
        return True
    
    return False


def _check_field_quality(field_name: str, value: Optional[any]) -> FieldStatus:
    """Check quality of a single field."""
    if value is None or (isinstance(value, str) and not value.strip()):
        return FieldStatus(
            field_name=field_name,
            present=False,
            quality="missing",
            feedback=f"Missing {field_name}"
        )
    
    # Special checks for description field
    if field_name == "description" and isinstance(value, str):
        if _is_vague_description(value):
            return FieldStatus(
                field_name=field_name,
                present=True,
                quality="vague",
                feedback="Description is too vague. Include specifics like material, dimensions, features, or use cases."
            )
    
    return FieldStatus(
        field_name=field_name,
        present=True,
        quality="good",
        feedback=None
    )


def audit_product(product: Product) -> AuditResult:
    """
    Audit a product for AI readiness.
    
    Returns:
        AuditResult with score, field checks, and recommendations.
    """
    field_checks = []
    missing_fields = []
    vague_fields = []
    
    # Check critical fields
    for field in CRITICAL_FIELDS:
        value = getattr(product, field, None)
        status = _check_field_quality(field, value)
        field_checks.append(status)
        
        if status.quality == "missing":
            missing_fields.append(field)
        elif status.quality == "vague":
            vague_fields.append(field)
    
    # Check important fields
    for field in IMPORTANT_FIELDS:
        value = getattr(product, field, None)
        status = _check_field_quality(field, value)
        field_checks.append(status)
    
    # Determine description quality
    desc_status = next((s for s in field_checks if s.field_name == "description"), None)
    if desc_status:
        description_quality = desc_status.quality if desc_status.quality in ["clear", "vague", "missing"] else "clear"
    else:
        description_quality = "missing"
    
    # Calculate readiness score (0-100)
    score = 100
    
    # Deduct for missing critical fields
    score -= len(missing_fields) * 20
    
    # Deduct for vague fields
    score -= len(vague_fields) * 15
    
    # Check for missing important fields (less severe)
    for field in IMPORTANT_FIELDS:
        status = next((s for s in field_checks if s.field_name == field), None)
        if status and status.quality == "missing":
            score -= 5
    
    score = max(0, min(100, score))  # Clamp to 0-100
    
    # Generate recommendations
    recommendations = []
    
    if missing_fields:
        recommendations.append(f"Add missing critical fields: {', '.join(missing_fields)}")
    
    if vague_fields:
        for field in vague_fields:
            status = next((s for s in field_checks if s.field_name == field), None)
            if status and status.feedback:
                recommendations.append(status.feedback)
    
    # Check for missing important fields
    missing_important = []
    for field in IMPORTANT_FIELDS:
        status = next((s for s in field_checks if s.field_name == field), None)
        if status and status.quality == "missing":
            missing_important.append(field)
    
    if missing_important:
        recommendations.append(f"Consider adding: {', '.join(missing_important)}")
    
    if not recommendations:
        recommendations.append("Product description is AI-ready!")
    
    # Generate summary
    if score >= 80:
        summary = "Excellent AI readiness. Product has clear, complete information."
    elif score >= 60:
        summary = "Good AI readiness. Add missing details to improve clarity."
    elif score >= 40:
        summary = "Fair AI readiness. Significant improvements needed."
    else:
        summary = "Poor AI readiness. Critical information is missing or vague."
    
    return AuditResult(
        product_id=product.id,
        product_title=product.title,
        readiness_score=score,
        field_checks=field_checks,
        description_quality=description_quality,
        missing_critical_fields=missing_fields,
        recommendations=recommendations,
        summary=summary
    )
