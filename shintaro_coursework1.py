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

def loadInventoryFromFile():
    if not INVENTORY_FILE.exists():
        return
    try:
        data = json.loads(INVENTORY_FILE.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print("Warning: inventory file is corrupted. Starting empty.")
        return

    for rec in data:
        pid = int(rec.get("id", 0))
        name = str(rec.get("name", "")).strip()
        if not name or pid <= 0:
            continue
        brand_tuple = tuple(rec.get("brand", []))
        category = str(rec.get("category", ""))
        quantity = int(rec.get("quantity", 0))
        price = float(rec.get("price", 0.0))

        if rec.get("type") == "PerishableProduct":
            exp = str(rec.get("expiration_date", ""))
            product = PerishableProduct(pid, name, price, quantity, category, brand_tuple, exp)
        else:
            product = Product(pid, name, price, quantity, category, brand_tuple)

        inventory[name] = product
        product_ids.add(pid)


def saveInventoryToFile():
    data = [inventory[name].to_dict() for name in sorted(inventory.keys())]
    INVENTORY_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


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

def updateItem():
    print("Update Item selected.")
    product_name = input("Enter product name to update: > ").strip().title()
    if product_name not in inventory:
        print("Item not found in inventory.")
        return False
    try:
        change_cat = input("Change category? (y/n): > ").strip().lower()
        category = _choose_category() if change_cat in {"y", "yes"} else None
        quantity_text = input("Enter new quantity (blank to keep): > ").strip()
        price_text = input("Enter new price (blank to keep): > ").strip()
        quantity = int(quantity_text) if quantity_text != "" else None
        price = float(price_text) if price_text != "" else None
    except ValueError:
        print("Invalid input. Please enter the correct data types.")
        return False

    if quantity is not None and quantity < 0:
        print("Quantity must be 0 or higher.")
        return False
    if price is not None and price < 0:
        print("Price must be 0 or higher.")
        return False

    # brand is intentionally NOT updated (stored as tuple)
    item = inventory[product_name]
    item.update(category=category, quantity=quantity, price=price)
    print("\n")
    print("Inventory updated successfully!")
    return True

def removeItem():
    print("Remove Item selected.")
    product_name = input("Enter product name to remove: > ").strip().title()
    print("\n")
    if product_name in inventory:
        pid = inventory[product_name].product_id
        del inventory[product_name]
        product_ids.discard(pid)
        print("Item removed successfully.")
        return True
    else:
        print("Item not found in inventory.")
        return False

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