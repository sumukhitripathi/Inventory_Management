import csv
# Basic Inventory Management System Logic (Not required for Flask app, but included for understanding)
# Inventory dictionary to store products (product_name: [quantity, price])

inventory = {}

def add_product():
    name = input("Enter product name: ")
    quantity = int(input("Enter quantity: "))
    price = float(input("Enter price per unit: "))
    
    if name in inventory:
        inventory[name][0] += quantity
        inventory[name] = [quantity, price]
    
    print(f"Product '{name}' added successfully!\n")

def view_inventory():
    if not inventory:
        print("Inventory is empty.")
        return
    print("Current Inventory:")
    print("Name\tQuantity\tPrice")
    for name, details in inventory.items():
        print(f"{name}\t{details[0]}\t${details[1]:.2f}")
    print()

def update_product():
    name = input("Enter product name to update: ")
    if name in inventory:
        quantity = int(input("Enter new quantity: "))
        inventory[name][0] = quantity
        print(f"Updated {name} stock to {quantity}\n")
    else:
        print("Product not found!\n")

def delete_product():
    name = input("Enter product name to delete: ")
    if name in inventory:
        del inventory[name]
        print(f"Deleted '{name}' from inventory\n")
    else:
        print("Product not found!\n")

def search_product():
    name = input("Enter product name to search: ")
    if name in inventory:
        print(f"{name}: Quantity={inventory[name][0]}, Price=${inventory[name][1]:.2f}\n")
    else:
        print("Product not found!\n")

# Complete the below function ------------------
def save_inventory():
    with open("inventory.csv","w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Quantity", "Price"])
        for product_name, details in inventory.items():
            row = [product_name,details[0],details[1]]
            writer.writerow(row)
    print("Inventory saved to inventory.csv\n")

# ----------------------------------------------

if __name__ == "__main__":
    
    while True:
        print("1. Add Product\n2. View Inventory\n3. Update Stock\n4. Delete Product\n5. Search Product\n6. Save & Exit")
        choice = input("Enter your choice: ")
    
        if choice == "1":
            add_product()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            search_product()
        elif choice == "6":
            save_inventory()
            print("Exiting program...")
            break
        else:
            print("Invalid choice! Please try again.\n")
