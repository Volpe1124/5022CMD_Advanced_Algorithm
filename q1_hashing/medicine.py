"""
medicine.py
Entity class that represents one pharmacy product (a medicine).
"""


class Medicine:
    """A medicine product sold by the pharmacy."""

    CATEGORIES = ("OTC", "Prescription", "Supplement")

    def __init__(self, product_id: int, name: str, price: float,
                 stock: int, category: str = "OTC", expiry_date: str = "-"):
        self.product_id = int(product_id)    # unique key used for hashing
        self.name = str(name)                # e.g. "Paracetamol 500mg"
        self.price = round(float(price), 2)  # selling price in RM
        self.stock = int(stock)              # units currently on hand
        self.category = category             # OTC / Prescription / Supplement
        self.expiry_date = expiry_date       # "YYYY-MM-DD"

    def __str__(self):
        return (f"ID: {self.product_id} | Name: {self.name} | "
                f"Price: RM{self.price:.2f} | Stock: {self.stock} | "
                f"Category: {self.category} | Expiry: {self.expiry_date}")

    def __repr__(self):
        return f"Medicine({self.product_id}, {self.name!r})"
