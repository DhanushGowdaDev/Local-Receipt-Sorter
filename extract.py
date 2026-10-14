"""Local receipt/invoice extraction: Gemma vision model via Ollama + validation."""
import os
import re
from datetime import date, datetime
from pathlib import Path
from typing import Literal, Optional

import fitz  # PyMuPDF
import ollama
from pydantic import BaseModel, Field

# Any vision-capable Ollama model works. Try gemma3:4b first, then 12b if your RAM allows.
MODEL = os.getenv("RECEIPT_MODEL", "gemma3:4b")


class Receipt(BaseModel):
    vendor: Optional[str] = Field(None, description="Business that issued the document")
    date: Optional[str] = Field(None, description="Issue date as YYYY-MM-DD")
    invoice_number: Optional[str] = None
    currency: Optional[str] = Field(None, description="ISO 4217 code, e.g. INR, USD, EUR")
    subtotal: Optional[float] = Field(None, description="Amount before tax")
    tax: Optional[float] = Field(None, description="Total tax (GST/VAT/sales tax)")
    total: Optional[float] = Field(None, description="Final amount paid or due")
    category: Literal[
        "software", "travel", "meals", "office", "equipment",
        "marketing", "professional_services", "utilities", "other",
    ] = "other"


PROMPT = (
    "Read this receipt or invoice and fill in every field you can. "
    "vendor: the business name, usually in the logo or header, or in a 'sold by' / 'billed from' section. "
    "date: the invoice or order date, converted to YYYY-MM-DD. If it looks like 04/10/2026, read it as "
    "day/month/year unless the document clearly uses another order. "
    "currency: infer it from symbols such as \u20b9 (INR), $ (USD), \u20ac (EUR), \u00a3 (GBP), "
    "or from the country and language on the page. "
    "Amounts are plain numbers with no symbols or thousands separators. "
    "tax is the total tax charged (for Indian GST, CGST+SGST or IGST combined). "
    "Use null only when the information truly is not on the page."
)


def to_images(path: Path) -> list[bytes]:
    """PDFs become PNGs of their first two pages; images are passed through."""
    if path.suffix.lower() == ".pdf":
        doc = fitz.open(path)
        return [doc[i].get_pixmap(dpi=150).tobytes("png") for i in range(min(2, len(doc)))]
    return [path.read_bytes()]


def extract(path: Path) -> Receipt:
    resp = ollama.chat(
        model=MODEL,
        messages=[{"role": "user", "content": PROMPT, "images": to_images(Path(path))}],
        format=Receipt.model_json_schema(),  # constrains output to the schema
        options={"temperature": 0},
    )
    return Receipt.model_validate_json(resp["message"]["content"])


def check(r: Receipt) -> list[str]:
    """Rule-based flags. Small models rate their own confidence poorly, so we verify instead."""
    flags = []
    for f in ("vendor", "date", "total", "currency"):
        if getattr(r, f) in (None, ""):
            flags.append(f"missing {f}")
    if r.date:
        try:
            d = datetime.strptime(r.date, "%Y-%m-%d").date()
            if d > date.today():
                flags.append("date is in the future")
        except ValueError:
            flags.append("date not YYYY-MM-DD")
    if r.total is not None and r.total <= 0:
        flags.append("total is not positive")
    if None not in (r.subtotal, r.tax, r.total) and abs(r.subtotal + r.tax - r.total) > 0.05:
        flags.append("subtotal + tax does not equal total")
    return flags


def suggested_name(r: Receipt, original: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", (r.vendor or "unknown").lower()).strip("-")
    total = f"{r.total:.2f}" if r.total is not None else "na"
    return f"{r.date or 'undated'}_{slug}_{total}{Path(original).suffix.lower()}"