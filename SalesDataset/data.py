import numpy as np

# -----------------------------
# DATASET (5 products × 12 months)
# -----------------------------
sales = np.array([
    [200, 220, 250, 270, 300, 320, 310, 330, 350, 370, 390, 410],
    [150, 160, 170, 180, 175, 165, 160, 155, 150, 145, 140, 135],
    [300, 320, 340, 360, 380, 400, 420, 440, 460, 480, 500, 520],
    [100, 120, 140, 130, 150, 170, 160, 180, 200, 220, 240, 260],
    [250, 240, 230, 220, 210, 200, 190, 180, 170, 160, 150, 140]
])

# -----------------------------
# SALES ANALYSIS
# -----------------------------

# Total yearly sales per product
yearly_sales = np.sum(sales, axis=1)
print("Yearly Sales per Product:", yearly_sales)

# Monthly total sales
monthly_sales = np.sum(sales, axis=0)
print("Monthly Sales:", monthly_sales)

# Best-selling product
best_product = np.argmax(yearly_sales)
print("Best Selling Product (index):", best_product)

# Best sales month
best_month = np.argmax(monthly_sales)
print("Best Sales Month (index):", best_month)

# -----------------------------
# STATISTICAL ANALYSIS
# -----------------------------

# Mean sales per product
mean_sales = np.mean(sales, axis=1)
print("Mean Sales per Product:", mean_sales)

# Standard deviation
std_sales = np.std(sales, axis=1)
print("Standard Deviation:", std_sales)

# Growth percentage between months
growth = np.diff(sales) / sales[:, :-1] * 100
print("Growth %:\n", growth)

# -----------------------------
# BUSINESS INSIGHTS
# -----------------------------

# Declining products (last < first)
declining_products = np.where(sales[:, -1] < sales[:, 0])[0]
print("Declining Products:", declining_products)

# Top 3 sales months
top_3_months = np.argsort(monthly_sales)[-3:]
print("Top 3 Sales Months:", top_3_months)

# Predict next month sales using avg growth
avg_growth = np.mean(growth, axis=1)
next_month_sales = sales[:, -1] * (1 + avg_growth / 100)

print("Predicted Next Month Sales:", next_month_sales)
