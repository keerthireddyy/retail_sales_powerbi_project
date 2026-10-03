#!/usr/bin/env python3
"""Generate a reproducible, fictional retail orders dataset for the Power BI project.

Usage: python generate_data.py
Only Python's standard library is required.
"""

from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 42
ORDER_COUNT = 2400
CUSTOMER_COUNT = 180
START_DATE = date(2022, 1, 1)
END_DATE = date(2025, 12, 31)

random.seed(SEED)

# Each entry: category, sub-category, product name, list price, pre-discount margin.
PRODUCT_ROWS = [
    ("Office Supplies", "Binders", "Compact Ring Binder", 12.00, 0.32),
    ("Office Supplies", "Binders", "Premium Lever Binder", 24.00, 0.28),
    ("Office Supplies", "Paper", "Copy Paper Ream", 8.00, 0.24),
    ("Office Supplies", "Paper", "Recycled Paper Case", 35.00, 0.22),
    ("Office Supplies", "Storage", "Stackable Storage Box", 28.00, 0.30),
    ("Office Supplies", "Storage", "Desktop Organizer", 18.00, 0.35),
    ("Office Supplies", "Labels", "Address Label Pack", 14.00, 0.34),
    ("Office Supplies", "Labels", "Color Label Set", 9.00, 0.38),
    ("Furniture", "Chairs", "Task Chair", 145.00, 0.23),
    ("Furniture", "Chairs", "Ergonomic Chair", 320.00, 0.27),
    ("Furniture", "Tables", "Compact Writing Desk", 210.00, 0.20),
    ("Furniture", "Tables", "Conference Table", 640.00, 0.18),
    ("Furniture", "Bookcases", "Open Bookcase", 185.00, 0.22),
    ("Furniture", "Bookcases", "Five-Shelf Bookcase", 275.00, 0.21),
    ("Furniture", "Furnishings", "Floor Lamp", 85.00, 0.30),
    ("Furniture", "Furnishings", "Task Light", 42.00, 0.32),
    ("Technology", "Phones", "Cordless Phone", 95.00, 0.24),
    ("Technology", "Phones", "Business Desk Phone", 165.00, 0.26),
    ("Technology", "Accessories", "Wireless Mouse", 32.00, 0.36),
    ("Technology", "Accessories", "USB-C Dock", 125.00, 0.28),
    ("Technology", "Copiers", "Desktop Copier", 490.00, 0.17),
    ("Technology", "Copiers", "Color Copier", 780.00, 0.19),
    ("Technology", "Machines", "Laser Printer", 260.00, 0.22),
    ("Technology", "Machines", "Multifunction Printer", 520.00, 0.20),
]

GEOGRAPHIES = {
    "West": [
        ("California", "Los Angeles", "90012"),
        ("California", "San Francisco", "94103"),
        ("California", "San Diego", "92101"),
        ("Oregon", "Portland", "97205"),
        ("Oregon", "Eugene", "97401"),
        ("Washington", "Seattle", "98101"),
        ("Washington", "Spokane", "99201"),
        ("Arizona", "Phoenix", "85004"),
        ("Colorado", "Denver", "80202"),
    ],
    "Central": [
        ("Texas", "Houston", "77002"),
        ("Texas", "Dallas", "75201"),
        ("Texas", "Austin", "78701"),
        ("Illinois", "Chicago", "60601"),
        ("Minnesota", "Minneapolis", "55401"),
        ("Missouri", "St. Louis", "63101"),
        ("Wisconsin", "Milwaukee", "53202"),
    ],
    "South": [
        ("Florida", "Miami", "33130"),
        ("Florida", "Orlando", "32801"),
        ("Georgia", "Atlanta", "30303"),
        ("North Carolina", "Charlotte", "28202"),
        ("Tennessee", "Nashville", "37201"),
        ("Alabama", "Birmingham", "35203"),
    ],
    "East": [
        ("New York", "New York City", "10001"),
        ("New York", "Buffalo", "14202"),
        ("Pennsylvania", "Philadelphia", "19103"),
        ("Massachusetts", "Boston", "02108"),
        ("New Jersey", "Newark", "07102"),
        ("Virginia", "Richmond", "23219"),
    ],
}

FIRST_NAMES = [
    "Alex", "Avery", "Bailey", "Cameron", "Casey", "Charlie", "Dakota",
    "Drew", "Emerson", "Finley", "Harper", "Jamie", "Jordan", "Kai",
    "Logan", "Morgan", "Parker", "Quinn", "Reese", "Riley", "Robin",
    "Sam", "Skyler", "Taylor", "Ari", "Blake", "Devon", "Ellis", "Jules", "Rowan",
]
LAST_NAMES = [
    "Adams", "Bennett", "Brooks", "Campbell", "Carter", "Chen", "Clark",
    "Collins", "Diaz", "Edwards", "Foster", "Garcia", "Green", "Hall",
    "Harris", "Hughes", "Kim", "Lee", "Lewis", "Martin", "Miller", "Mitchell",
    "Moore", "Morgan", "Nguyen", "Patel", "Perry", "Reed", "Rivera", "Ross",
    "Shah", "Singh", "Turner", "Walker", "Wright", "Young",
]

SHIP_MODES = ["Standard Class", "Second Class", "First Class", "Same Day"]
SHIP_MODE_WEIGHTS = [0.52, 0.23, 0.18, 0.07]
SEGMENTS = ["Consumer", "Corporate", "Home Office"]
SEGMENT_WEIGHTS = [0.50, 0.31, 0.19]
REGIONS = ["West", "Central", "South", "East"]
REGION_WEIGHTS = [0.29, 0.25, 0.23, 0.23]
DISCOUNTS = [0.00, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40]
DISCOUNT_WEIGHTS = [0.23, 0.17, 0.20, 0.17, 0.12, 0.08, 0.03]
QUANTITIES = [1, 2, 3, 4, 5]
QUANTITY_WEIGHTS = [0.34, 0.29, 0.21, 0.11, 0.05]
LINE_COUNTS = [1, 2, 3, 4, 5]
LINE_COUNT_WEIGHTS = [0.28, 0.33, 0.22, 0.12, 0.05]


def build_customers() -> list[dict[str, str]]:
    customers = []
    for i in range(1, CUSTOMER_COUNT + 1):
        region = random.choices(REGIONS, weights=REGION_WEIGHTS, k=1)[0]
        state, city, postal_code = random.choice(GEOGRAPHIES[region])
        customers.append(
            {
                "Customer ID": f"C-{i:04d}",
                "Customer Name": f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}",
                "Segment": random.choices(SEGMENTS, weights=SEGMENT_WEIGHTS, k=1)[0],
                "Region": region,
                "State": state,
                "City": city,
                "Postal Code": postal_code,
            }
        )
    return customers


def seasonal_factor(order_date: date) -> float:
    # Mild retail seasonality, with a year-on-year growth trend.
    month_factors = {
        1: 0.88, 2: 0.86, 3: 0.94, 4: 0.96, 5: 0.98, 6: 1.00,
        7: 1.02, 8: 1.03, 9: 1.05, 10: 1.08, 11: 1.16, 12: 1.28,
    }
    annual_growth = 1.0 + 0.045 * (order_date.year - START_DATE.year)
    return month_factors[order_date.month] * annual_growth


def shipping_days(ship_mode: str) -> int:
    if ship_mode == "Same Day":
        return 0
    if ship_mode == "First Class":
        return random.randint(1, 2)
    if ship_mode == "Second Class":
        return random.randint(2, 4)
    return random.randint(3, 7)


def main() -> None:
    output_path = Path(__file__).resolve().parent / "data" / "orders.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    customers = build_customers()
    products = [
        {
            "Product ID": f"P-{i:03d}",
            "Category": row[0],
            "Sub-Category": row[1],
            "Product Name": row[2],
            "List Price": row[3],
            "Margin": row[4],
        }
        for i, row in enumerate(PRODUCT_ROWS, start=1)
    ]

    headers = [
        "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
        "Customer ID", "Customer Name", "Segment", "Country", "City",
        "State", "Postal Code", "Region", "Product ID", "Category",
        "Sub-Category", "Product Name", "Sales", "Quantity", "Discount", "Profit",
    ]

    date_span = (END_DATE - START_DATE).days
    row_id = 0
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()

        for order_number in range(1, ORDER_COUNT + 1):
            order_date = START_DATE + timedelta(days=random.randint(0, date_span))
            customer = random.choice(customers)
            ship_mode = random.choices(SHIP_MODES, weights=SHIP_MODE_WEIGHTS, k=1)[0]
            ship_date = order_date + timedelta(days=shipping_days(ship_mode))
            order_id = f"ORD-{order_date.year}-{order_number:05d}"
            line_count = random.choices(LINE_COUNTS, weights=LINE_COUNT_WEIGHTS, k=1)[0]
            selected_products = random.sample(products, k=line_count)

            for product in selected_products:
                row_id += 1
                quantity = random.choices(QUANTITIES, weights=QUANTITY_WEIGHTS, k=1)[0]
                discount = random.choices(DISCOUNTS, weights=DISCOUNT_WEIGHTS, k=1)[0]
                price_noise = random.uniform(0.86, 1.16)
                gross_sales = (
                    product["List Price"]
                    * quantity
                    * price_noise
                    * seasonal_factor(order_date)
                )
                sales = gross_sales * (1.0 - discount)
                cost = gross_sales * (1.0 - product["Margin"])
                profit = sales - cost

                writer.writerow(
                    {
                        "Row ID": row_id,
                        "Order ID": order_id,
                        "Order Date": order_date.isoformat(),
                        "Ship Date": ship_date.isoformat(),
                        "Ship Mode": ship_mode,
                        "Customer ID": customer["Customer ID"],
                        "Customer Name": customer["Customer Name"],
                        "Segment": customer["Segment"],
                        "Country": "United States",
                        "City": customer["City"],
                        "State": customer["State"],
                        "Postal Code": customer["Postal Code"],
                        "Region": customer["Region"],
                        "Product ID": product["Product ID"],
                        "Category": product["Category"],
                        "Sub-Category": product["Sub-Category"],
                        "Product Name": product["Product Name"],
                        "Sales": f"{sales:.2f}",
                        "Quantity": quantity,
                        "Discount": f"{discount:.2f}",
                        "Profit": f"{profit:.2f}",
                    }
                )

    print(f"Created {row_id:,} order lines from {ORDER_COUNT:,} orders: {output_path}")


if __name__ == "__main__":
    main()
