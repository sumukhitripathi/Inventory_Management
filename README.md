# InventoryOS

InventoryOS is a Flask-based inventory management web application for tracking products, stock levels, categories, prices, and SKUs. It includes a dashboard, product management screens, inventory search and filtering, low-stock status labels, and CSV export.

## Features

- Dashboard with total items, product count, category count, low-stock alerts, and total inventory value
- Add new products with SKU, category, quantity, price, and description
- View all products in an inventory table
- Filter inventory by product/SKU, category, and stock status
- Search products by name or SKU
- Update product quantity, price, SKU, category, and description
- Delete products with a confirmation modal
- Export the current inventory to CSV
- Flash messages for success, warning, and error states

## Tech Stack

- Python
- Flask
- Jinja2 templates
- Tailwind CSS via CDN
- JavaScript for shared UI behavior

## Project Structure

```text
.
+-- app.py                  # Main Flask web application
+-- main.py                 # Console-based inventory prototype
+-- requirements.txt        # Python dependencies
+-- static/
|   +-- js/
|       +-- app.js          # Shared frontend JavaScript
+-- templates/
    +-- base.html           # Shared layout, navigation, modal, flash UI
    +-- dashboard.html      # Dashboard page
    +-- inventory.html      # Inventory table and filters
    +-- add_product.html    # Add product form
    +-- update_product.html # Update product form
    +-- search.html         # Search page
```

## Getting Started

### 1. Create a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```powershell
pip install -r requirements.txt
```

The Flask app loads environment variables with `python-dotenv`. If it is not already installed in your environment, install it with:

```powershell
pip install python-dotenv
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
INVENTORY_OS_SECRET_KEY=replace-with-a-secure-secret-key
```

This key is used by Flask for flash messages and session signing.

### 4. Run the Flask app

```powershell
python app.py
```

## Main Routes

| Route | Description |
| --- | --- |
| `/` | Dashboard overview |
| `/inventory` | View, search, and filter inventory |
| `/add` | Add a new product |
| `/update/<product_name>` | Update an existing product |
| `/delete/<product_name>` | Delete a product using POST |
| `/search` | Search products by name or SKU |
| `/save` | Export current inventory as `inventory_export.csv` |

## Data Storage

The current application stores inventory data in an in-memory Python dictionary inside `app.py`. This means changes are available only while the Flask server is running. Restarting the server resets the inventory back to the sample data defined in the code.

For production use, replace the in-memory dictionary with persistent storage such as SQLite, PostgreSQL, MySQL, or another database.

## CSV Export

Use the export button in the app bar or dashboard to download the current inventory as a CSV file. The export includes:

- Product Name
- SKU
- Category
- Quantity
- Price
- Description

## Console Prototype

`main.py` contains a simple command-line inventory program. It is separate from the Flask app and can be run with:

```powershell
python main.py
```

The web app in `app.py` is the primary application.