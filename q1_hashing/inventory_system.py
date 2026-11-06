"""
inventory_system.py
Command-line Pharmacy Inventory System built on the HashTable.

Features: insert, search (with hash table vs array timing), edit, delete,
list all products. Run:  python inventory_system.py
"""
import time

from hash_table import HashTable
from medicine import Medicine

TABLE_SIZE = 101   # prime number -> keys spread more evenly

PREDEFINED = [
    (1001, "Paracetamol 500mg", 5.90, 120, "OTC", "2027-08-31"),
    (1002, "Ibuprofen 200mg", 8.50, 80, "OTC", "2027-03-15"),
    (1003, "Amoxicillin 250mg", 15.00, 45, "Prescription", "2026-12-31"),
    (1004, "Cetirizine 10mg", 7.20, 60, "OTC", "2027-05-20"),
    (1005, "Vitamin C 1000mg", 25.90, 150, "Supplement", "2028-01-10"),
    (1006, "Omeprazole 20mg", 18.40, 35, "Prescription", "2027-02-28"),
    (1007, "Loratadine 10mg", 9.80, 70, "OTC", "2027-09-30"),
    (1008, "Metformin 500mg", 12.60, 90, "Prescription", "2027-06-30"),
    (1102, "Salbutamol Inhaler", 22.00, 25, "Prescription", "2027-04-30"),
    (1203, "Fish Oil 1000mg", 39.90, 55, "Supplement", "2028-03-31"),
    (1304, "Antacid Tablets", 6.50, 100, "OTC", "2027-11-30"),
    (2001, "Zinc 15mg", 19.90, 65, "Supplement", "2028-02-28"),
]


class PharmacyInventory:
    """Keeps the same records in a hash table and in a plain 1-D array."""

    def __init__(self, capacity=TABLE_SIZE):
        self.table = HashTable(capacity)
        self.array = []                     # one-dimensional array (Python list)

    def insert(self, med: Medicine):
        slot = self.table.put(med.product_id, med)
        for i, m in enumerate(self.array):   # keep array in sync (update case)
            if m.product_id == med.product_id:
                self.array[i] = med
                break
        else:
            self.array.append(med)
        return slot

    def search_hash(self, product_id):
        return self.table.get(product_id)

    def search_array(self, product_id):
        for med in self.array:               # linear search, O(n)
            if med.product_id == product_id:
                return med
        return None

    def delete(self, product_id):
        removed = self.table.remove(product_id)
        self.array = [m for m in self.array if m.product_id != product_id]
        return removed


# ---------------------------------------------------------------------- #
# Input helpers (validation so the program never crashes on bad input)
# ---------------------------------------------------------------------- #
def ask_int(prompt, minimum=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                print(f"  Please enter a number >= {minimum}.")
                continue
            return value
        except ValueError:
            print("  Invalid number, please try again.")


def ask_float(prompt, minimum=0.0):
    while True:
        try:
            value = float(input(prompt).strip())
            if value < minimum:
                print(f"  Please enter a value >= {minimum}.")
                continue
            return value
        except ValueError:
            print("  Invalid amount, please try again.")


def ask_category():
    options = ", ".join(f"{i + 1}={c}" for i, c in enumerate(Medicine.CATEGORIES))
    while True:
        choice = input(f"Enter Category ({options}): ").strip()
        if choice in ("1", "2", "3"):
            return Medicine.CATEGORIES[int(choice) - 1]
        print("  Please choose 1, 2 or 3.")


TIMING_RUNS = 10_000   # one search takes < 1 microsecond, so we repeat it
                       # many times and report the average to remove noise


def timed(func, *args):
    """Run func(*args) TIMING_RUNS times; return (result, avg time in ns)."""
    result = func(*args)
    start = time.perf_counter_ns()
    for _ in range(TIMING_RUNS):
        func(*args)
    elapsed = time.perf_counter_ns() - start
    return result, elapsed / TIMING_RUNS


# ---------------------------------------------------------------------- #
# Menu actions
# ---------------------------------------------------------------------- #
def do_insert(inv):
    pid = ask_int("Enter Product ID: ", 1)
    if pid in inv.table:
        print(f"Product ID {pid} already exists. Use Edit to change it.")
        return
    name = input("Enter Product Name: ").strip() or "Unnamed"
    price = ask_float("Enter Price (RM): ")
    stock = ask_int("Enter Stock Quantity: ", 0)
    category = ask_category()
    expiry = input("Enter Expiry Date (YYYY-MM-DD): ").strip() or "-"
    slot = inv.insert(Medicine(pid, name, price, stock, category, expiry))
    home = inv.table._hash(pid)
    note = "" if slot == home else f" (home slot [{home}] occupied -> probed {inv.table.last_probes} slots)"
    print(f"Product inserted successfully into slot [{slot}]{note}")


def do_search(inv):
    pid = ask_int("Enter Product ID to search: ")
    med, t_hash = timed(inv.search_hash, pid)
    probes = inv.table.last_probes
    _, t_array = timed(inv.search_array, pid)
    if med:
        print("Product Found!")
        print(med)
        print(f"Stored in slot [{inv.table.slot_of(pid)}], probes needed: {probes}")
    else:
        print(f"Product ID {pid} not found.")
    print(f"Search completed in {t_hash:>8,.1f} ns (Hash Table, avg of {TIMING_RUNS:,} runs)")
    print(f"Search completed in {t_array:>8,.1f} ns (Array - same record, avg of {TIMING_RUNS:,} runs)")


def do_edit(inv):
    pid = ask_int("Enter Product ID to edit: ")
    med = inv.search_hash(pid)
    if not med:
        print(f"Product ID {pid} not found.")
        return
    print("Current:", med)
    print("Press Enter to keep the current value.")
    name = input(f"New Name [{med.name}]: ").strip()
    price = input(f"New Price [{med.price:.2f}]: ").strip()
    stock = input(f"New Stock [{med.stock}]: ").strip()
    try:
        if name:
            med.name = name
        if price:
            med.price = round(float(price), 2)
        if stock:
            med.stock = int(stock)
        print("Product updated:", med)
    except ValueError:
        print("Invalid value entered - record left unchanged for that field.")


def do_delete(inv):
    pid = ask_int("Enter Product ID to delete: ")
    if inv.delete(pid):
        print(f"Product {pid} deleted (slot marked as tombstone).")
    else:
        print(f"Product ID {pid} not found.")


def do_list(inv):
    print(f"\n{'Slot':>5}  {'ID':>5}  {'Name':<22}{'Price(RM)':>10}{'Stock':>7}  Category")
    print("-" * 66)
    for slot, _, med in inv.table.items():
        print(f"{slot:>5}  {med.product_id:>5}  {med.name:<22}{med.price:>10.2f}"
              f"{med.stock:>7}  {med.category}")
    print(f"Records: {len(inv.table)} | Capacity: {inv.table.capacity} | "
          f"Load factor: {inv.table.load_factor:.2f}")


def main():
    inv = PharmacyInventory()
    for rec in PREDEFINED:
        inv.insert(Medicine(*rec))
    print(f"{len(PREDEFINED)} pre-defined products loaded into a hash table "
          f"of size {inv.table.capacity}.")

    actions = {"1": do_insert, "2": do_search, "3": do_edit,
               "4": do_delete, "5": do_list}
    while True:
        print("\n==== Pharmacy Inventory System ====")
        print("1. Insert Product\n2. Search Product\n3. Edit Product\n"
              "4. Delete Product\n5. List All Products\n6. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "6":
            print("Exiting Inventory System. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(inv)
        else:
            print("Invalid choice, please enter 1-6.")


if __name__ == "__main__":
    main()
