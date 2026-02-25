from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import mysql.connector
from config import DB_CONFIG
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey123"

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

@app.route("/")
def home():
    return redirect("/products")

@app.route("/products")
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("index.html", products=products)

# 🛒 ADD TO CART (SESSION MODE)
@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
            (user_id, product_id, quantity)
        )
        conn.commit()
        return jsonify({"message": "Product added to cart"})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

    finally:
        cursor.close()
        conn.close()

# 🛒 VIEW CART
@app.route("/cart/<int:user_id>", methods=["GET"])
def view_cart(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            c.id AS cart_id,
            p.name,
            p.price,
            c.quantity,
            (p.price * c.quantity) AS subtotal
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (user_id,))

    cart_items = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(cart_items)

# 📦 PLACE ORDER
@app.route("/place_order", methods=["POST"])
def place_order():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Not logged in"}), 401
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # 1️⃣ Get cart items
        cursor.execute("""
            SELECT c.product_id, c.quantity, p.price
            FROM cart c
            JOIN products p ON c.product_id = p.id
            WHERE c.user_id = %s
        """, (user_id,))
        
        cart_items = cursor.fetchall()

        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400

        # 2️⃣ Calculate total
        total_amount = sum(item["price"] * item["quantity"] for item in cart_items)

        # 3️⃣ Insert into orders
        cursor.execute(
            "INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s)",
            (user_id, total_amount, "Pending")
        )
        conn.commit()

        order_id = cursor.lastrowid

        # 4️⃣ Insert into order_items
        for item in cart_items:
            subtotal = item["price"] * item["quantity"]

            cursor.execute("""
                INSERT INTO order_items (order_id, product_id, quantity, price, subtotal)
                VALUES (%s, %s, %s, %s, %s)
            """, (order_id, item["product_id"], item["quantity"], item["price"], subtotal))

        conn.commit()

        # 5️⃣ Clear cart
        cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))
        conn.commit()

        return jsonify({
            "message": "Order placed successfully",
            "order_id": order_id,
            "total_amount": total_amount
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cursor.close()
        conn.close()

# 📜 VIEW ORDERS
@app.route("/orders/<int:user_id>", methods=["GET"])
def view_orders(user_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            o.id AS order_id,
            o.total_amount,
            o.status,
            o.created_at,
            p.name AS product_name,
            oi.quantity,
            oi.price,
            oi.subtotal
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.user_id = %s
        ORDER BY o.created_at DESC
    """, (user_id,))

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(orders)

# 🛒 CART PAGE (Simple Mode)
@app.route("/cart")
def cart_page():
    user_id = session.get("user_id")

    if not user_id:
    	return redirect("/products")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            c.id AS cart_id,
            p.name,
            p.price,
            c.quantity,
            (p.price * c.quantity) AS subtotal
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = %s
    """, (user_id,))

    cart_items = cursor.fetchall()

    total = sum(item["subtotal"] for item in cart_items)

    cursor.close()
    conn.close()

    return render_template("cart.html", cart_items=cart_items, total=total)

# 🔐 LOGIN PAGE (HTML)
@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            return redirect("/products")
        else:
            return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# 📝 REGISTER PAGE (HTML)
@app.route("/register", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
                (name, email, hashed_password),
            )
            conn.commit()
            return redirect("/login")

        except:
            return render_template("register.html", error="Email already exists")

        finally:
            cursor.close()
            conn.close()

    return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")

# ❌ REMOVE FROM CART
@app.route("/remove_from_cart/<int:cart_id>", methods=["POST"])
def remove_from_cart(cart_id):
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM cart WHERE id = %s AND user_id = %s",
        (cart_id, user_id)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return redirect("/cart")

# 📦 ORDER HISTORY PAGE
@app.route("/orders")
def orders_page():
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            o.id AS order_id,
            o.total_amount,
            o.status,
            o.created_at,
            p.name AS product_name,
            oi.quantity,
            oi.price,
            oi.subtotal
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.user_id = %s
        ORDER BY o.created_at DESC
    """, (user_id,))

    orders = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("orders.html", orders=orders)

# 🔄 UPDATE CART QUANTITY
@app.route("/update_quantity/<int:cart_id>/<string:action>", methods=["POST"])
def update_quantity(cart_id, action):
    user_id = session.get("user_id")

    if not user_id:
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get current quantity
    cursor.execute(
        "SELECT quantity FROM cart WHERE id = %s AND user_id = %s",
        (cart_id, user_id)
    )
    item = cursor.fetchone()

    if not item:
        cursor.close()
        conn.close()
        return redirect("/cart")

    current_qty = item["quantity"]

    if action == "increase":
        new_qty = current_qty + 1
    elif action == "decrease":
        new_qty = current_qty - 1
    else:
        new_qty = current_qty

    if new_qty <= 0:
        cursor.execute(
            "DELETE FROM cart WHERE id = %s AND user_id = %s",
            (cart_id, user_id)
        )
    else:
        cursor.execute(
            "UPDATE cart SET quantity = %s WHERE id = %s AND user_id = %s",
            (new_qty, cart_id, user_id)
        )

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/cart")

if __name__ == "__main__":
    app.run(debug=True)