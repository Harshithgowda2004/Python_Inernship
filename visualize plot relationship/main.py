import matplotlib.pyplot as plt

# Sample data (you can replace with your own)
years_experience = [1, 2, 3, 4, 5, 6, 7, 8]
salary = [25000, 30000, 35000, 45000, 50000, 60000, 65000, 70000]

# Create scatter plot
plt.scatter(years_experience, salary)

# Labels and title
plt.xlabel("Years of Experience")
plt.ylabel("Salary")
plt.title("Experience vs Salary")

# Grid
plt.grid(True)

# Show plot
plt.show()
