import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Harshith@11",
    database="inventory_db"
)

cursor = conn.cursor()

print("Connected to database!")

# 🔹 Add Product Function
def add_product():
    name = input("Enter product name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price: "))

    query = "INSERT INTO products (name, quantity, price) VALUES (%s, %s, %s)"
    values = (name, quantity, price)

    cursor.execute(query, values)
    conn.commit()

    print("Product added successfully!")

# 🔹 Show All Products
def show_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    print("\nAll Products:")
    for product in products:
        print(product)

# 🔹 Menu
while True:
    print("\n1. Add Product")
    print("2. Show Products")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        add_product()

    elif choice == "2":
        show_products()

    elif choice == "3":
        break

    else:
        print("Invalid choice")

conn.close()