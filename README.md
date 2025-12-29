# Inventory Management System (Python)

Simple menu-driven inventory manager. You can add/view/update/remove products, and the inventory is saved to a file so it loads again next time.

## How to run

From this folder:

```bash
python shintaro_coursework1.py
```

## Features implemented (checklist)

-   [x] Inventory stored in a dictionary
-   [x] User input to add items (name/quantity/price) with validation
-   [x] Categories stored as a list and selected when adding/updating
-   [x] Brand stored as a tuple (treated as non-changeable)
-   [x] Unique product IDs tracked using a set
-   [x] Menu loop with conditional statements (View/Update/Remove/Exit)
-   [x] Functions for add/view/update/remove
-   [x] OOP: `Product` class (name/price/quantity) + display/update methods
-   [x] Inheritance: `PerishableProduct` subclass with expiration date
-   [x] File handling: load inventory on start, save on exit (`inventory.txt`)

## Limitations / known issues

-   Category is selected by number (not typed exactly like the sample output).
-   Product names are normalized with `.title()`, so exact casing may change.
-   Inventory file format is JSON stored in `inventory.txt`; if the file is corrupted, the program starts with an empty inventory.
