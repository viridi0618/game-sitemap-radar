from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


PROJECT_ROOT = Path(__file__).resolve().parents[2]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def url_hash(url: str) -> str:
    return hashlib.sha256(url.encode("utf-8")).hexdigest()


def normalize_domain(domain_or_url: str) -> str:
    value = domain_or_url.strip()
    if "://" in value:
        parsed = urlparse(value)
        value = parsed.netloc
    return value.lower().strip("/")


def domain_base_url(domain: str) -> str:
    clean = normalize_domain(domain)
    return f"https://{clean}"


def ensure_dirs() -> None:
    (PROJECT_ROOT / "data").mkdir(exist_ok=True)
    (PROJECT_ROOT / "outputs").mkdir(exist_ok=True)
    (PROJECT_ROOT / "config").mkdir(exist_ok=True)


def parse_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

