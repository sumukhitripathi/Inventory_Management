"""
InventoryOS - Flask Inventory Management System
================================================
A web-based inventory system built with Flask.
Stores data in memory (dictionary) and supports CSV export.
"""

import csv
import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from io import StringIO, BytesIO
from dotenv import load_dotenv

load_dotenv()

# ── App Setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.secret_key = os.getenv("INVENTORY_OS_SECRET_KEY")  # Required for flash messages
#Can use keys for database connections, when added in future, right now a dummy memory dictionary used

# ── In-Memory Inventory Store ────────────────────────────────────────────────
# Structure: { product_name: { "quantity": int, "price": float, "sku": str, "category": str, "description": str } }
inventory = {
    "MacBook Pro M2 - Space Gray": {
        "quantity": 3,
        "price": 2499.00,
        "sku": "APPLE-MBP-2023-01",
        "category": "Electronics",
        "description": "Apple MacBook Pro with M2 chip, 16GB RAM, 512GB SSD."
    },
    "Magic Mouse - Gen 3": {
        "quantity": 42,
        "price": 79.00,
        "sku": "APPLE-MM3-WHT",
        "category": "Electronics",
        "description": "Apple Magic Mouse 3rd generation, white finish."
    },
    "Ergonomic Mesh Chair": {
        "quantity": 1,
        "price": 450.00,
        "sku": "FUR-CHAIR-MESH-01",
        "category": "Furniture",
        "description": "High-back ergonomic mesh office chair with lumbar support."
    },
    "High-Speed Laser Printer": {
        "quantity": 12,
        "price": 899.00,
        "sku": "OFF-PRT-LSR-99",
        "category": "Office Supplies",
        "description": "Monochrome laser printer, 40 ppm, duplex printing."
    },
    "4K Curved Monitor 32\"": {
        "quantity": 8,
        "price": 599.00,
        "sku": "DISP-4K-CRV-01",
        "category": "Electronics",
        "description": "32-inch 4K UHD curved display with USB-C connectivity."
    },
}

# ── Helper Functions ──────────────────────────────────────────────────────────

def get_dashboard_stats():
    """Calculate summary statistics for the dashboard."""
    total_items = sum(p["quantity"] for p in inventory.values())
    low_stock = sum(1 for p in inventory.values() if p["quantity"] <= 5)
    total_value = sum(p["quantity"] * p["price"] for p in inventory.values())
    categories = len(set(p["category"] for p in inventory.values()))
    return {
        "total_items": total_items,
        "low_stock": low_stock,
        "total_value": total_value,
        "categories": categories,
        "product_count": len(inventory),
    }

def get_stock_status(quantity):
    """Return a stock status label based on quantity."""
    if quantity == 0:
        return "Out of Stock"
    elif quantity <= 5:
        return "Low Stock"
    else:
        return "In Stock"
app.jinja_env.globals['get_stock_status'] = get_stock_status

# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def dashboard():
    """Homepage — shows summary stats and recent inventory."""
    stats = get_dashboard_stats()
    # Get the 5 most recently added items for the recent activity section
    recent = list(inventory.items())[-5:][::-1]
    return render_template("dashboard.html", stats=stats, recent=recent)


@app.route("/inventory")
def view_inventory():
    """View all products in a sortable table."""
    # Support basic filtering by category and status
    category_filter = request.args.get("category", "")
    status_filter = request.args.get("status", "")
    search_query = request.args.get("q", "")

    products = list(inventory.items())

    # Apply filters
    if category_filter:
        products = [(n, p) for n, p in products if p["category"] == category_filter]
    if status_filter:
        products = [(n, p) for n, p in products if get_stock_status(p["quantity"]) == status_filter]
    if search_query:
        q = search_query.lower()
        products = [(n, p) for n, p in products if q in n.lower() or q in p["sku"].lower()]

    # Collect all unique categories for the filter dropdown
    all_categories = sorted(set(p["category"] for p in inventory.values()))
    stats = get_dashboard_stats()

    return render_template(
        "inventory.html",
        products=products,
        all_categories=all_categories,
        stats=stats,
        get_stock_status=get_stock_status,
        category_filter=category_filter,
        status_filter=status_filter,
        search_query=search_query,
    )


@app.route("/add", methods=["GET", "POST"])
def add_product():
    """Add a new product — GET shows the form, POST processes it."""
    if request.method == "POST":
        # Read form fields
        name = request.form.get("name", "").strip()
        sku = request.form.get("sku", "").strip()
        category = request.form.get("category", "").strip()
        description = request.form.get("description", "").strip()

        # Validate required fields
        try:
            quantity = int(request.form.get("quantity", 0))
            price = float(request.form.get("price", 0.0))
        except ValueError:
            flash("Quantity must be a whole number and Price must be a valid number.", "error")
            return redirect(url_for("add_product"))

        if not name:
            flash("Product name is required.", "error")
            return redirect(url_for("add_product"))
        if not sku:
            flash("SKU number is required.", "error")
            return redirect(url_for("add_product"))
        if category == "Select Category" or not category:
            flash("Please select a valid category.", "error")
            return redirect(url_for("add_product"))
        if quantity < 0:
            flash("Quantity cannot be negative.", "error")
            return redirect(url_for("add_product"))
        if price < 0:
            flash("Price cannot be negative.", "error")
            return redirect(url_for("add_product"))

        # If product already exists, update quantity (merge)
        if name in inventory:
            inventory[name]["quantity"] += quantity
            flash(f"Product '{name}' already exists — quantity updated to {inventory[name]['quantity']}.", "warning")
        else:
            inventory[name] = {
                "quantity": quantity,
                "price": price,
                "sku": sku,
                "category": category,
                "description": description,
            }
            flash(f"Product '{name}' has been successfully added to inventory.", "success")

        return redirect(url_for("add_product"))

    # GET — render the blank form
    return render_template("add_product.html")


@app.route("/update/<path:product_name>", methods=["GET", "POST"])
def update_product(product_name):
    """Update an existing product's details."""
    if product_name not in inventory:
        flash(f"Product '{product_name}' not found.", "error")
        return redirect(url_for("view_inventory"))

    product = inventory[product_name]

    if request.method == "POST":
        try:
            new_quantity = int(request.form.get("quantity", product["quantity"]))
            new_price = float(request.form.get("price", product["price"]))
        except ValueError:
            flash("Invalid quantity or price value.", "error")
            return redirect(url_for("update_product", product_name=product_name))

        if new_quantity < 0 or new_price < 0:
            flash("Quantity and price cannot be negative.", "error")
            return redirect(url_for("update_product", product_name=product_name))

        # Apply updates
        inventory[product_name]["quantity"] = new_quantity
        inventory[product_name]["price"] = new_price
        inventory[product_name]["sku"] = request.form.get("sku", product["sku"]).strip()
        inventory[product_name]["category"] = request.form.get("category", product["category"]).strip()
        inventory[product_name]["description"] = request.form.get("description", product["description"]).strip()

        flash(f"Product '{product_name}' has been updated successfully.", "success")
        return redirect(url_for("view_inventory"))

    return render_template("update_product.html", product_name=product_name, product=product)


@app.route("/delete/<path:product_name>", methods=["POST"])
def delete_product(product_name):
    """Delete a product — only accepts POST (form submission) for safety."""
    if product_name in inventory:
        del inventory[product_name]
        flash(f"Product '{product_name}' has been deleted from inventory.", "success")
    else:
        flash(f"Product '{product_name}' not found.", "error")
    return redirect(url_for("view_inventory"))


@app.route("/search")
def search_product():
    """Search inventory by name or SKU."""
    query = request.args.get("q", "").strip()
    category_filter = request.args.get("category", "")
    status_filter = request.args.get("status", "")

    results = []
    if query or category_filter or status_filter:
        for name, product in inventory.items():
            q_lower = query.lower()
            name_match = q_lower in name.lower() if query else True
            sku_match = q_lower in product["sku"].lower() if query else True
            cat_match = product["category"] == category_filter if category_filter else True
            status_match = get_stock_status(product["quantity"]) == status_filter if status_filter else True

            if (name_match or sku_match) and cat_match and status_match:
                results.append((name, product))

    all_categories = sorted(set(p["category"] for p in inventory.values()))

    return render_template(
        "search.html",
        results=results,
        query=query,
        all_categories=all_categories,
        get_stock_status=get_stock_status,
        category_filter=category_filter,
        status_filter=status_filter,
        searched=(query != "" or category_filter != "" or status_filter != ""),
    )


@app.route("/save")
def save_inventory():
    """Export current inventory to a CSV file and offer it as a download."""
    output = StringIO()
    writer = csv.writer(output)

    # Write header row
    writer.writerow(["Product Name", "SKU", "Category", "Quantity", "Price (USD)", "Description"])

    # Write each product
    for name, details in inventory.items():
        writer.writerow([
            name,
            details["sku"],
            details["category"],
            details["quantity"],
            f"{details['price']:.2f}",
            details["description"],
        ])

    # Convert to bytes for download
    byte_output = BytesIO(output.getvalue().encode("utf-8"))
    byte_output.seek(0)

    flash("Inventory exported successfully as CSV.", "success")
    return send_file(
        byte_output,
        mimetype="text/csv",
        as_attachment=True,
        download_name="inventory_export.csv",
    )


# ── Entry Point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True)
