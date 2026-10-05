import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# ============================================================
# PROJECT 2
# MULTI-CHANNEL DIGITAL MARKETING ROAS DATASET
# ============================================================

# ------------------------------------------------------------
# 1. Setup
# ------------------------------------------------------------

num_orders = 25000
num_customers = 4500

np.random.seed(42)
random.seed(42)

# ------------------------------------------------------------
# 2. Customer Master
# ------------------------------------------------------------

customer_ids = [
    f"CUST-{1000 + i}"
    for i in range(num_customers)
]

# ------------------------------------------------------------
# 3. Product Catalog
# ------------------------------------------------------------

product_catalog = {

    "PROD-01": {
        "Name": "Wireless Ergonomic Mouse",
        "Category": "Electronics",
        "Cost": 1200,
        "Price": 2499,
        "Weight_Kg": 0.2,
        "SupplierID": "SUP-01"
    },

    "PROD-02": {
        "Name": "Mechanical RGB Keyboard",
        "Category": "Electronics",
        "Cost": 2800,
        "Price": 5999,
        "Weight_Kg": 0.9,
        "SupplierID": "SUP-02"
    },

    "PROD-03": {
        "Name": "4K Ultra-Wide Monitor",
        "Category": "Electronics",
        "Cost": 18000,
        "Price": 29999,
        "Weight_Kg": 5.4,
        "SupplierID": "SUP-03"
    },

    "PROD-04": {
        "Name": "Leather Minimalist Wallet",
        "Category": "Accessories",
        "Cost": 400,
        "Price": 1499,
        "Weight_Kg": 0.1,
        "SupplierID": "SUP-04"
    },

    "PROD-05": {
        "Name": "Waterproof Sports Backpack",
        "Category": "Apparel",
        "Cost": 900,
        "Price": 2899,
        "Weight_Kg": 0.6,
        "SupplierID": "SUP-05"
    },

    "PROD-06": {
        "Name": "Bamboo Desk Organizer",
        "Category": "Home Decor",
        "Cost": 350,
        "Price": 999,
        "Weight_Kg": 0.8,
        "SupplierID": "SUP-06"
    }
}

# ------------------------------------------------------------
# 4. Supplier Lead Times
# ------------------------------------------------------------

supplier_lead_times = {
    "SUP-01": 7,
    "SUP-02": 12,
    "SUP-03": 18,
    "SUP-04": 6,
    "SUP-05": 10,
    "SUP-06": 14
}

# ------------------------------------------------------------
# 5. Order Statuses
# ------------------------------------------------------------

statuses = [
    "Delivered",
    "Delivered",
    "Delivered",
    "Shipped",
    "Cancelled",
    "Returned",
    "Refunded"
]

# ------------------------------------------------------------
# 6. Date Range
# ------------------------------------------------------------

start_date = datetime(2024, 1, 1)

# ------------------------------------------------------------
# 7. Create Orders
# ------------------------------------------------------------

order_data = []

product_ids = list(product_catalog.keys())

for i in range(num_orders):

    order_id = f"ORD-{50000 + i}"

    cust_id = random.choice(customer_ids)

    prod_id = random.choice(product_ids)

    product = product_catalog[prod_id]

    # --------------------------------------------------------
    # Quantity
    # --------------------------------------------------------

    qty = np.random.choice(
        [1, 2, 3, 4, 5],
        p=[0.70, 0.18, 0.07, 0.03, 0.02]
    )

    # --------------------------------------------------------
    # Product Financials
    # --------------------------------------------------------

    unit_price = product["Price"]

    unit_cost = product["Cost"]

    gross_revenue = unit_price * qty

    # --------------------------------------------------------
    # Discount
    # --------------------------------------------------------

    discount_rate = np.random.choice(
        [0.0, 0.05, 0.10, 0.15, np.nan],
        p=[0.60, 0.15, 0.10, 0.05, 0.10]
    )

    if np.isnan(discount_rate):
        discount_amt = 0
    else:
        discount_amt = gross_revenue * discount_rate

    net_revenue = gross_revenue - discount_amt

    # --------------------------------------------------------
    # Order Date
    # --------------------------------------------------------

    days_offset = random.randint(0, 730)

    order_date = start_date + timedelta(days=days_offset)

    # --------------------------------------------------------
    # Order Status
    # --------------------------------------------------------

    status = np.random.choice(
        statuses,
        p=[0.80, 0.05, 0.03, 0.05, 0.03, 0.02, 0.02]
    )

    # ========================================================
    # INVENTORY LOGIC
    # ========================================================

    # Base stock level differs by product
    base_stock = {
        "PROD-01": 180,
        "PROD-02": 140,
        "PROD-03": 60,
        "PROD-04": 250,
        "PROD-05": 200,
        "PROD-06": 220
    }

    # --------------------------------------------------------
    # Current Stock
    # --------------------------------------------------------

    current_stock = max(
        0,
        int(
            np.random.normal(
                base_stock[prod_id],
                base_stock[prod_id] * 0.30
            )
        )
    )

    # --------------------------------------------------------
    # Lead Time
    # --------------------------------------------------------

    lead_time_days = supplier_lead_times[
        product["SupplierID"]
    ]

    # --------------------------------------------------------
    # Simulated Average Daily Demand
    # --------------------------------------------------------

    avg_daily_demand = {
        "PROD-01": 8,
        "PROD-02": 6,
        "PROD-03": 2,
        "PROD-04": 12,
        "PROD-05": 9,
        "PROD-06": 10
    }[prod_id]

    # --------------------------------------------------------
    # Safety Stock
    # --------------------------------------------------------

    safety_stock = int(
        avg_daily_demand * random.uniform(3, 8)
    )

    # --------------------------------------------------------
    # Reorder Point
    #
    # Reorder Point =
    # Average Daily Demand × Lead Time
    # + Safety Stock
    # --------------------------------------------------------

    reorder_point = int(
        avg_daily_demand * lead_time_days
        + safety_stock
    )

    # --------------------------------------------------------
    # Inventory Status
    # --------------------------------------------------------

    if current_stock == 0:

        inventory_status = "Stockout"

    elif current_stock <= reorder_point:

        inventory_status = "Reorder Required"

    elif current_stock > reorder_point * 2.5:

        inventory_status = "Overstock"

    else:

        inventory_status = "Healthy"

    # --------------------------------------------------------
    # Supplier
    # --------------------------------------------------------

    supplier_id = product["SupplierID"]

    # --------------------------------------------------------
    # Append Row
    # --------------------------------------------------------

    order_data.append([

        order_id,
        cust_id,
        prod_id,
        product["Name"],
        product["Category"],
        qty,
        unit_price,
        unit_cost,
        discount_rate,
        round(net_revenue, 2),

        # Inventory fields
        current_stock,
        reorder_point,
        safety_stock,
        lead_time_days,
        supplier_id,

        order_date,
        inventory_status
    ])


# ============================================================
# 8. Create DataFrame
# ============================================================

df_orders = pd.DataFrame(
    order_data,
    columns=[
        "OrderID",
        "CustomerID",
        "ProductID",
        "ProductName",
        "Category",
        "Quantity",
        "UnitPrice",
        "UnitCost",
        "DiscountRate",
        "NetRevenue",
        "CurrentStock",
        "ReorderPoint",
        "SafetyStock",
        "LeadTimeDays",
        "SupplierID",
        "OrderDate",
        "InventoryStatus"
    ]
)



# ============================================================
# 8A. ADD SIMULATED MARKETING & KPI SUPPORT COLUMNS
# ============================================================
# Synthetic portfolio-demo fields (not real campaign measurements).
# Each source row is treated as an attributed order event.

marketing_channels = ["Shopify Web", "Amazon Marketplace", "Instagram Ads", "Google PPC"]
df_orders["MarketingChannel"] = np.random.choice(marketing_channels, size=len(df_orders))
df_orders["Region"] = np.random.choice(["North", "South", "East", "West"], size=len(df_orders))

campaign_map = {
    "Shopify Web": [("SW-01", "Storefront Discovery"), ("SW-02", "Seasonal Storefront"), ("SW-03", "Product Launch")],
    "Amazon Marketplace": [("AM-01", "Sponsored Products"), ("AM-02", "Marketplace Deals"), ("AM-03", "Category Promotion")],
    "Instagram Ads": [("IG-01", "Product Awareness"), ("IG-02", "Seasonal Promotion"), ("IG-03", "Retargeting")],
    "Google PPC": [("GP-01", "Brand Search"), ("GP-02", "Product Search"), ("GP-03", "Shopping Campaign")],
}
picked_campaigns = [random.choice(campaign_map[ch]) for ch in df_orders["MarketingChannel"]]
df_orders["CampaignID"] = [x[0] for x in picked_campaigns]
df_orders["CampaignName"] = [x[1] for x in picked_campaigns]

# Simulated ad spend allocated to each order row.
spend_ranges = {
    "Shopify Web": (20, 180),
    "Amazon Marketplace": (30, 220),
    "Instagram Ads": (25, 250),
    "Google PPC": (35, 300),
}
df_orders["AdSpend"] = [
    round(random.uniform(*spend_ranges[ch]), 2) for ch in df_orders["MarketingChannel"]
]

# Synthetic funnel counts for demo purposes; each row represents an order event.
df_orders["Impressions"] = np.random.randint(40, 401, size=len(df_orders))
ctr_by_channel = {"Shopify Web": 0.045, "Amazon Marketplace": 0.055, "Instagram Ads": 0.035, "Google PPC": 0.065}
cart_rate_by_channel = {"Shopify Web": 0.24, "Amazon Marketplace": 0.30, "Instagram Ads": 0.18, "Google PPC": 0.27}
df_orders["Clicks"] = [
    max(1, int(np.random.binomial(int(imp), ctr_by_channel[ch])))
    for imp, ch in zip(df_orders["Impressions"], df_orders["MarketingChannel"])
]
df_orders["AddToCart"] = [
    int(np.random.binomial(int(clk), cart_rate_by_channel[ch]))
    for clk, ch in zip(df_orders["Clicks"], df_orders["MarketingChannel"])
]
df_orders["Purchases"] = 1

# New customer flag: 1 on each customer's earliest order date.
first_order_dates = df_orders.groupby("CustomerID")["OrderDate"].transform("min")
df_orders["NewCustomerFlag"] = df_orders["OrderDate"].eq(first_order_dates).astype(int)

# Calculated order-line financial fields.
df_orders["COGS"] = (df_orders["Quantity"] * df_orders["UnitCost"]).round(2)
df_orders["ProfitAfterAds"] = (df_orders["NetRevenue"] - df_orders["COGS"] - df_orders["AdSpend"]).round(2)
df_orders["AttributedRevenue"] = df_orders["NetRevenue"]

# ============================================================
# 9. Inject Duplicate Records
# ============================================================

duplicates = df_orders.sample(
    n=120,
    random_state=42
)

df_orders = pd.concat(
    [df_orders, duplicates],
    ignore_index=True
)


# ============================================================
# 10. Inject Additional Data Quality Problems
# ============================================================

# ------------------------------------------------------------
# Missing Supplier IDs
# ------------------------------------------------------------

missing_supplier_indices = np.random.choice(
    df_orders.index,
    size=100,
    replace=False
)

df_orders.loc[
    missing_supplier_indices,
    "SupplierID"
] = np.nan


# ------------------------------------------------------------
# Missing Lead Times
# ------------------------------------------------------------

missing_lead_indices = np.random.choice(
    df_orders.index,
    size=80,
    replace=False
)

df_orders.loc[
    missing_lead_indices,
    "LeadTimeDays"
] = np.nan


# ------------------------------------------------------------
# Missing Reorder Points
# ------------------------------------------------------------

missing_reorder_indices = np.random.choice(
    df_orders.index,
    size=100,
    replace=False
)

df_orders.loc[
    missing_reorder_indices,
    "ReorderPoint"
] = np.nan


# ------------------------------------------------------------
# Create a few extreme inventory values
# ------------------------------------------------------------

outlier_indices = np.random.choice(
    df_orders.index,
    size=50,
    replace=False
)

df_orders.loc[
    outlier_indices,
    "CurrentStock"
] = np.random.randint(
    1000,
    3000,
    size=len(outlier_indices)
)


# ============================================================
# 11. Shuffle Data
# ============================================================

df_orders = df_orders.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)


# ============================================================
# 12. Export
# ============================================================

file_name = "Marketing_ROAS_Campaign_Performance_Master.csv"

df_orders.to_csv(
    file_name,
    index=False
)


# ============================================================
# 13. Validation
# ============================================================

print("==============================================")
print("SUPPLY CHAIN DATASET GENERATED SUCCESSFULLY")
print("==============================================")

print(f"Rows: {len(df_orders):,}")
print(f"Columns: {len(df_orders.columns)}")

print("\nColumns:")
for col in df_orders.columns:
    print("-", col)

print("\nInventory Status Distribution:")
print(
    df_orders["InventoryStatus"]
    .value_counts()
)

print("\nMissing Values:")
print(
    df_orders.isnull()
    .sum()
)

print("\nSample Data:")
print(
    df_orders.head()
)

print("\n==============================================")
print(f"File created: {file_name}")
print("==============================================")