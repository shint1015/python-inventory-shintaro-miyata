import json
from pathlib import Path


# 7) File Handling
INVENTORY_FILE = Path(__file__).with_name("inventory.txt")

# 3) Lists: categories
CATEGORIES = ["Electronics", "Home", "Office"]


# 6) Object-Oriented Programming
class Product:
    def __init__(self, product_id, name, price, quantity, category, brand_tuple):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.category = category
        # 3) Tuples: brand shouldn't change
        self.brand = brand_tuple

    def update(self, *, category=None, quantity=None, price=None):
        if category is not None:
            self.category = category
        if quantity is not None:
            self.quantity = quantity
        if price is not None:
            self.price = price

    def display(self):
        brand_name = self.brand[0] if self.brand else ""
        return (
            f"ID: {self.product_id} | "
            f"Name: {self.name} | "
            f"Brand: {brand_name} | "
            f"Category: {self.category} | "
            f"Quantity: {self.quantity} | "
            f"Price: ${self.price:.2f}"
        )

    def to_dict(self):
        return {
            "type": "Product",
            "id": self.product_id,
            "name": self.name,
            "brand": list(self.brand),
            "category": self.category,
            "quantity": self.quantity,
            "price": self.price,
        }
class PerishableProduct(Product):
    def __init__(self, product_id, name, price, quantity, category, brand_tuple, expiration_date):
        super().__init__(product_id, name, price, quantity, category, brand_tuple)
        self.expiration_date = expiration_date

    def display(self):
        return f"{super().display()} | Exp: {self.expiration_date}"

    def to_dict(self):
        d = super().to_dict()
        d["type"] = "PerishableProduct"
        d["expiration_date"] = self.expiration_date
        return d


def _choose_category():
    print("Select a category:")
    for i, cat in enumerate(CATEGORIES, start=1):
        print(f"  {i}. {cat}")
    while True:
        choice = input("Category number: > ").strip()
        if not choice.isdigit():
            print("Please enter a number.")
            continue
        idx = int(choice)
        if 1 <= idx <= len(CATEGORIES):
            return CATEGORIES[idx - 1]
        print("Invalid selection.")


MAINMENU = (
    '1. Add Item',
    '2. View Inventory',
    '3. Update Item',
    '4. Remove Item',
    '5. Exit'
)

selectedOption = 0

# 1) Basic Setup: inventory as dictionary
# inventory maps product name -> Product
inventory = {}

# 3) Sets: track unique product IDs
product_ids = set()


def _next_product_id():
    new_id = 100 if not product_ids else max(product_ids) + 1
    while new_id in product_ids:
        new_id += 1
    return new_id


def printMenu(menuItems):
    for item in menuItems:
        print(item)


def addItem():
    try:
        # String methods: strip/title
        product_name = input("Enter product name: > ").strip().title()
        category = _choose_category()
        brand_name = input("Enter brand name (won't change later): > ").strip().title()
        quantity = int(input("Enter quantity: > ").strip())
        price = float(input("Enter price: > ").strip())
    except ValueError:
        print("Invalid input. Please enter the correct data types.")
        return None

    if not product_name or not brand_name:
        print("Name/Brand cannot be empty.")
        return None
    if quantity < 0 or price < 0:
        print("Quantity/Price must be 0 or higher.")
        return None

    is_perishable = input("Is this perishable? (y/n): > ").strip().lower()
    exp = ""
    if is_perishable in {"y", "yes"}:
        exp = input("Enter expiration date (YYYY-MM-DD): > ").strip()
        if not exp:
            print("Expiration date cannot be empty for perishable items.")
            return None

    pid = _next_product_id()
    brand_tuple = (brand_name,)
    if exp:
        product = PerishableProduct(pid, product_name, price, quantity, category, brand_tuple, exp)
    else:
        product = Product(pid, product_name, price, quantity, category, brand_tuple)

    inventory[product_name] = product
    product_ids.add(pid)

    # 2) formatting
    print(f"Added: {product_name} (Qty={quantity}, Price=${price:.2f})")
    print("\n")
    print("Item added successfully!")
    return pid

def viewInventory():
    if not inventory:
        print("Inventory is empty.")
        return
    print("Current Inventory:")
    print("-" * 20)
    for name in sorted(inventory.keys()):
        print(inventory[name].display())


print ("Welcome to the Inventory Management System!")


while (selectedOption != 5):
    print ("=" * 43)
    printMenu(MAINMENU)
    try:
        selectedOption = int(input("Select an option: > "))
    except ValueError:
        print("\nInvalid input. Please enter a number corresponding to the menu options.")
        continue
    print("\n")
    if selectedOption == 1:
        addItem()
    elif selectedOption == 2:
        viewInventory()
    elif selectedOption == 3:
        updateItem()
    elif selectedOption == 4:
        removeItem()
    elif selectedOption == 5:
        print("Saving inventory to file...")
        saveInventoryToFile()
        print("Exiting system. Goodbye!")
    else:
        print("Invalid option. Please select a valid menu option.")
    print("\n")