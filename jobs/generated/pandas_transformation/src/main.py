"""Deterministically generated from a reviewed Python notebook."""

# Notebook code cell 2
import pandas as pd

sales = pd.DataFrame(
    {
        "product": ["notebook", "keyboard", "notebook"],
        "quantity": [2, 1, 3],
        "unit_price": [12.50, 45.00, 12.50],
    }
)
sales

# Notebook code cell 3
revenue_by_product = (
    sales.assign(revenue=sales["quantity"] * sales["unit_price"])
    .groupby("product", as_index=False)["revenue"]
    .sum()
    .sort_values("revenue", ascending=False)
)
revenue_by_product
