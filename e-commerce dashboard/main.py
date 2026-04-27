import matplotlib.pyplot as plt

# -----------------------------
# Sample Data (replace with real later)
# -----------------------------
months = ["Jan", "Feb", "Mar", "Apr", "May"]
revenue = [20000, 25000, 30000, 28000, 35000]

age_groups = ["18-25", "26-35", "36-45", "46+"]
customers = [120, 200, 150, 80]

categories = ["Electronics", "Clothing", "Home", "Sports"]
purchases = [300, 500, 200, 150]

# -----------------------------
# Create Dashboard (3 plots)
# -----------------------------
plt.figure(figsize=(12, 8))

# 1️⃣ Revenue Trend (Line Chart)
plt.subplot(2, 2, 1)
plt.plot(months, revenue, marker='o')
plt.title("Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.grid(True)

# 2️⃣ Customer Demographics (Bar Chart)
plt.subplot(2, 2, 2)
plt.bar(age_groups, customers)
plt.title("Customer Age Distribution")
plt.xlabel("Age Group")
plt.ylabel("Number of Customers")
plt.grid(axis='y')

# 3️⃣ Purchasing Behavior (Pie Chart)
plt.subplot(2, 2, 3)
plt.pie(purchases, labels=categories, autopct='%1.1f%%')
plt.title("Purchase Categories")

# Layout adjustment
plt.tight_layout()

# Show dashboard
plt.show()
