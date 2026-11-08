from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

from .config import RAW_DIR


def generate_data(output_dir: Path = RAW_DIR, scale: int = 1, seed: int = 42) -> dict[str, pd.DataFrame]:
    """Generate deterministic synthetic e-commerce source tables.

    `scale=1` creates a quick sample. Larger values increase the row counts.
    The generated data is synthetic and contains no real customer information.
    """
    if scale < 1:
        raise ValueError("scale must be >= 1")

    rng = np.random.default_rng(seed)
    fake = Faker()
    Faker.seed(seed)
    output_dir.mkdir(parents=True, exist_ok=True)

    n_customers = 500 * scale
    n_products = 100 * scale
    n_orders = 2_000 * scale
    n_items = 5_000 * scale

    customers = pd.DataFrame({
        "customer_id": np.arange(1, n_customers + 1, dtype=np.int64),
        "customer_name": [fake.name() for _ in range(n_customers)],
        "city": rng.choice(["Pune", "Mumbai", "Nashik", "Aurangabad", "Nagpur"], n_customers),
        "region": rng.choice(["West", "North", "South", "East"], n_customers),
        "signup_date": pd.to_datetime("2023-01-01") + pd.to_timedelta(rng.integers(0, 900, n_customers), unit="D"),
    })

    products = pd.DataFrame({
        "product_id": np.arange(1, n_products + 1, dtype=np.int64),
        "product_name": [f"Product_{i:04d}" for i in range(1, n_products + 1)],
        "category": rng.choice(["Electronics", "Fashion", "Home", "Beauty", "Sports"], n_products),
        "unit_price": np.round(rng.uniform(100, 20_000, n_products), 2),
    })

    orders = pd.DataFrame({
        "order_id": np.arange(1, n_orders + 1, dtype=np.int64),
        "customer_id": rng.integers(1, n_customers + 1, n_orders, dtype=np.int64),
        "order_date": pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 600, n_orders), unit="D"),
        "order_status": rng.choice(["COMPLETED", "PENDING", "CANCELLED"], n_orders, p=[0.75, 0.15, 0.10]),
    })

    order_ids = rng.integers(1, n_orders + 1, n_items, dtype=np.int64)
    product_ids = rng.integers(1, n_products + 1, n_items, dtype=np.int64)
    quantity = rng.integers(1, 6, n_items, dtype=np.int64)
    price_lookup = products.set_index("product_id")["unit_price"]
    item_prices = price_lookup.loc[product_ids].to_numpy()
    order_items = pd.DataFrame({
        "order_item_id": np.arange(1, n_items + 1, dtype=np.int64),
        "order_id": order_ids,
        "product_id": product_ids,
        "quantity": quantity,
        "unit_price": item_prices,
        "line_amount": np.round(quantity * item_prices, 2),
    })

    payment_ids = np.arange(1, n_orders + 1, dtype=np.int64)
    payments = pd.DataFrame({
        "payment_id": payment_ids,
        "order_id": np.arange(1, n_orders + 1, dtype=np.int64),
        "payment_method": rng.choice(["CARD", "UPI", "NET_BANKING", "COD"], n_orders),
        "payment_status": rng.choice(["SUCCESS", "FAILED", "PENDING"], n_orders, p=[0.88, 0.07, 0.05]),
        "amount": np.round(rng.uniform(100, 50_000, n_orders), 2),
    })

    tables = {
        "customers": customers,
        "products": products,
        "orders": orders,
        "order_items": order_items,
        "payments": payments,
    }
    for name, frame in tables.items():
        frame.to_csv(output_dir / f"{name}.csv", index=False)
    return tables


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic YottaFlex challenge data")
    parser.add_argument("--scale", type=int, default=1, help="Multiply base row counts; use 50+ for 100k+ total rows")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    generated = generate_data(scale=args.scale, seed=args.seed)
    print("Generated rows:", {name: len(df) for name, df in generated.items()})
