"""
Load MOCK_DATA.csv into the Product table and ensure a superuser exists.

Run from the project root (with venv activated):

    python utils/load_mock_data.py
"""

from __future__ import annotations

import csv
import os
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path

# Project root (parent of utils/)
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "searchlab.settings")

import django

django.setup()

from django.contrib.auth import get_user_model  # noqa: E402

from product.models import Product  # noqa: E402

CSV_PATH = BASE_DIR / "MOCK_DATA.csv"
SUPERUSER_USERNAME = "admin"
SUPERUSER_PASSWORD = "1234"
SUPERUSER_EMAIL = "admin@example.com"


def create_superuser() -> None:
    User = get_user_model()
    user, created = User.objects.get_or_create(
        username=SUPERUSER_USERNAME,
        defaults={
            "email": SUPERUSER_EMAIL,
            "is_staff": True,
            "is_superuser": True,
        },
    )
    user.email = SUPERUSER_EMAIL
    user.is_staff = True
    user.is_superuser = True
    user.set_password(SUPERUSER_PASSWORD)
    user.save()

    if created:
        print(f"Created superuser '{SUPERUSER_USERNAME}'.")
    else:
        print(f"Updated superuser '{SUPERUSER_USERNAME}' password/permissions.")


def load_products() -> None:
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"CSV not found: {CSV_PATH}")

    created_count = 0
    skipped_count = 0

    with CSV_PATH.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"product_name", "price", "description"}
        if not required.issubset(set(reader.fieldnames or [])):
            raise ValueError(
                f"CSV must include columns: {', '.join(sorted(required))}"
            )

        for row in reader:
            name = (row.get("product_name") or "").strip()
            description = (row.get("description") or "").strip()
            raw_price = (row.get("price") or "").strip()

            if not name:
                skipped_count += 1
                continue

            try:
                price = Decimal(raw_price)
            except (InvalidOperation, TypeError):
                print(f"Skipping row with invalid price: {name!r} -> {raw_price!r}")
                skipped_count += 1
                continue

            _, created = Product.objects.get_or_create(
                product_name=name,
                defaults={
                    "price": price,
                    "description": description,
                },
            )
            if created:
                created_count += 1
            else:
                skipped_count += 1

    print(
        f"Products: {created_count} created, "
        f"{skipped_count} skipped (duplicates/invalid), "
        f"{Product.objects.count()} total in DB."
    )


def main() -> None:
    create_superuser()
    load_products()
    print("Done.")


if __name__ == "__main__":
    main()
