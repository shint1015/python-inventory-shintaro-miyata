# Inventory Management System (Python)

Simple menu-driven inventory manager. You can add/view/update/remove products, and the inventory is saved to a file so it loads again next time.

## How to run

From this folder:

```bash
python shintaro_coursework1.py
```

## Limitations / known issues

-   Category is selected by number (not typed exactly like the sample output).
-   Product names are normalized with `.title()`, so exact casing may change.
-   Inventory file format is JSON stored in `inventory.txt`; if the file is corrupted, the program starts with an empty inventory.
# python-inventory-shintaro-miyata
