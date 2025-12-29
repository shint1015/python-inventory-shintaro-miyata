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