"""
================================================================================
 Assignment 03 — Refactor the Messy Store System
 192-201 Advanced Computer Programming with Generative AI
 Week 5 — OOP Design & Refactoring   |   Faculty of IT (International), Siam University
 Lecturer: Hrang Kap Lian
================================================================================

 Maps to: CLO1 (object-oriented design) and CLO5 (responsible, verified AI use)
 Weight:  10 Points     AI-use level: Level 2 (AI-assisted + PROMPT LOG required)

--------------------------------------------------------------------------------
 THE TASK
--------------------------------------------------------------------------------
 You are given ONE working program that is badly written. Do NOT add features and
 do NOT change what it does. REFACTOR it: reshape the code into a clean,
 object-oriented design while producing the EXACT SAME output.

   The one rule of refactoring:  same behaviour, cleaner code.
   If the output changes, it is no longer a refactor — it is a bug.

 How to run:
   python Assignment_03.py
 It prints PASS when your refactor reproduces the original output exactly,
 or FAIL with the first line that differs.

--------------------------------------------------------------------------------
 WHAT YOU WILL PRACTISE (use ALL of these)
--------------------------------------------------------------------------------
   Week 2  Model data as CLASSES with attributes and methods (not tuples/lists).
   Week 3  ENCAPSULATION — validate object state in the constructor.
   Week 4  INHERITANCE & POLYMORPHISM — replace the `if tier == ...` chains
           with a family of classes.
   Week 5  COMPOSITION (has-a) — an Order has-a customer and has-many items;
           an item has-a product.
   Week 5  PURE FUNCTIONS vs MODIFIERS — calculation methods RETURN values and
           print nothing; keep them separate from the receipt printing.
   Week 5  INTERFACE vs IMPLEMENTATION — separate WHAT the receipt shows from
           HOW the totals are computed.

--------------------------------------------------------------------------------
 RULES
--------------------------------------------------------------------------------
 1. Behaviour must stay identical — the self-test must print PASS.
 2. Refactor only. No new discounts, no prettier receipts, no extra products.
 3. You choose the class design — there is no single correct answer.
 4. Level-2 AI use: you may use AI to explain/suggest/refactor, but YOU verify
    every change and you keep a PROMPT LOG (in CHANGES.md).
 5. Work in small steps: change one thing -> run -> keep it green.

--------------------------------------------------------------------------------
 THE SCENARIO
--------------------------------------------------------------------------------
 A small online store prints a receipt per order and a grand total. Business rules:
   - Tax: electronics & stationery = 7%; food = tax-free.
   - Membership discount on the subtotal:
         tier      subtotal<=100   subtotal>100
         none        0%              0%
         silver      2%              5%
         gold        5%              10%
         platinum    10%             15%
   - Bulk discount: 10+ items in total -> add another 3% of the subtotal.
   - total = subtotal - discount + tax
   - points = int(total // 10) * tier_multiplier   (none x1, silver x2, gold x3, platinum x5)
 You do not change these rules — you express them cleanly.

--------------------------------------------------------------------------------
 YOUR TASKS  (see the rubric at the bottom)
--------------------------------------------------------------------------------
   A. (required) Model the domain with classes + composition
                 e.g. Product, OrderItem (has-a Product), Customer, Order.
   B. (required) Encapsulate & validate state in constructors (e.g. qty >= 1).
   C. (required) Replace the tier `if/elif` chains (discount AND points) with
                 polymorphism — a class family, no `if tier == ...`.
   D. (required) Separate calculation from printing: pure methods return numbers.
   E. (required) Kill magic numbers (name them) and remove the leftover `global`.
   F. (stretch)  Let each product decide its own tax — no `if category` in totals.
   G. (stretch)  Add a sensible __str__ where it helps.

--------------------------------------------------------------------------------
 SUBMIT
--------------------------------------------------------------------------------
   1) This file, Assignment_03.py, with your refactor (self-test prints PASS).
   2) CHANGES.md — your written explanation of each change + your prompt log.
================================================================================
"""

import io
import contextlib


# ==============================================================================
#  LEGACY STORE SYSTEM  —  messy but working.   DO NOT EDIT THIS SECTION.
#  Read it, understand it, and use its output as the correct behaviour.
# ==============================================================================
PRODUCTS = [
    ("Laptop", 1200.0, "electronics"),
    ("Headphones", 200.0, "electronics"),
    ("Coffee Beans", 15.0, "food"),
    ("Notebook", 5.0, "stationery"),
    ("Water Bottle", 10.0, "food"),
    ("Monitor", 300.0, "electronics"),
    ("Pen", 2.0, "stationery"),
]
TAXRATE = 0.07
foodtax = 0.0
ORDERS = [
    ("Alice", "gold", [(0, 1), (1, 2), (2, 3)]),
    ("Bob", "none", [(3, 10), (6, 5)]),
    ("Charlie", "platinum", [(5, 2), (4, 6), (2, 2)]),
    ("Dana", "silver", [(1, 1), (3, 3), (6, 10)]),
]


def calc(o):
    global TAXRATE
    n = o[0]; t = o[1]; items = o[2]
    sub = 0.0; tax = 0.0
    print("Receipt for " + n + " (" + t + ")")
    print("-" * 40)
    for it in items:
        pi = it[0]; q = it[1]
        p = PRODUCTS[pi][1]; nm = PRODUCTS[pi][0]; cat = PRODUCTS[pi][2]
        line = p * q
        sub = sub + line
        if cat == "food":
            tax = tax + line * foodtax
        else:
            tax = tax + line * TAXRATE
        print(nm + " x" + str(q) + " = " + str(line))
    d = 0.0
    if t == "none":
        d = 0.0
    elif t == "silver":
        if sub > 100: d = sub * 0.05
        else: d = sub * 0.02
    elif t == "gold":
        if sub > 100: d = sub * 0.10
        else: d = sub * 0.05
    elif t == "platinum":
        if sub > 100: d = sub * 0.15
        else: d = sub * 0.10
    totalqty = 0
    for it in items:
        totalqty = totalqty + it[1]
    if totalqty >= 10:
        d = d + sub * 0.03
    total = sub - d + tax
    pts = 0
    if t == "none": pts = int(total // 10)
    elif t == "silver": pts = int(total // 10) * 2
    elif t == "gold": pts = int(total // 10) * 3
    elif t == "platinum": pts = int(total // 10) * 5
    print("-" * 40)
    print("Subtotal: " + str(round(sub, 2)))
    print("Discount: " + str(round(d, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(total, 2)))
    print("Points earned: " + str(pts))
    print("")
    return total


def legacy_main():
    grand = 0.0
    for o in ORDERS:
        grand = grand + calc(o)
    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


# ==============================================================================
#  BEHAVIOUR LOCK  —  DO NOT EDIT.
#  Captures the exact output of the legacy program as the target you must match.
# ==============================================================================
def capture(fn):
    """Run fn() and return everything it printed, as a string."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn()
    return buf.getvalue()


GOLDEN_OUTPUT = capture(legacy_main)


# ==============================================================================
#  YOUR REFACTORED SOLUTION  —  WRITE YOUR CODE BELOW.
#  Design your own classes. A suggested skeleton is commented out — change freely.
#  Your program must define refactored_main() which PRINTS the same output.
# ==============================================================================

# --- named constants (replace the magic numbers) ---
TAX_RATE           = 0.07
FOOD_TAX_RATE      = 0.0
FOOD_CATEGORY      = "food"
DISCOUNT_THRESHOLD = 100
BULK_QTY_THRESHOLD = 10
BULK_DISCOUNT_RATE = 0.03
POINTS_DIVISOR     = 10
RECEIPT_WIDTH      = 40


# ------------------------------------------------------------------------------
#  Products  (Task A, F: each product decides its own tax -> polymorphism)
# ------------------------------------------------------------------------------
class Product:
    """A sellable product. Standard products are taxed at TAX_RATE."""
    category = "general"

    def __init__(self, name, price):
        if not name:
            raise ValueError("Product name must not be empty")
        if price < 0:
            raise ValueError("Price must be >= 0, got " + str(price))
        self.name = name
        self.price = price

    def tax_rate(self):
        return TAX_RATE

    def __str__(self):
        return self.name + " (" + self.category + ") @ " + str(self.price)


class ElectronicsProduct(Product):
    category = "electronics"


class StationeryProduct(Product):
    category = "stationery"


class FoodProduct(Product):
    category = FOOD_CATEGORY

    def tax_rate(self):
        return FOOD_TAX_RATE


PRODUCT_CLASSES = {cls.category: cls for cls in
                   (ElectronicsProduct, StationeryProduct, FoodProduct)}


def make_product(name, price, category):
    """Look up the right Product subclass for a category name."""
    if category not in PRODUCT_CLASSES:
        raise ValueError("Unknown category: " + category)
    return PRODUCT_CLASSES[category](name, price)


# ------------------------------------------------------------------------------
#  OrderItem  (has-a Product)   (Task A, B)
# ------------------------------------------------------------------------------
class OrderItem:
    def __init__(self, product, quantity):
        if quantity < 1:
            raise ValueError("Quantity must be >= 1, got " + str(quantity))
        self.product = product
        self.quantity = quantity

    def line_total(self):
        return self.product.price * self.quantity

    def line_tax(self):
        return self.line_total() * self.product.tax_rate()

    def __str__(self):
        return self.product.name + " x" + str(self.quantity) + " = " + str(self.line_total())


# ------------------------------------------------------------------------------
#  Customers: tier class family  (Task C — polymorphism, no `if tier == ...`)
# ------------------------------------------------------------------------------
class Customer:
    """Base tier ('none'). Subclasses only override the class attributes."""
    tier_name = "none"
    small_rate = 0.0          # discount rate when subtotal <= DISCOUNT_THRESHOLD
    large_rate = 0.0          # discount rate when subtotal >  DISCOUNT_THRESHOLD
    points_multiplier = 1

    def __init__(self, name):
        if not name:
            raise ValueError("Customer name must not be empty")
        self.name = name

    def discount_rate(self, subtotal):
        if subtotal > DISCOUNT_THRESHOLD:
            return self.large_rate
        return self.small_rate

    def __str__(self):
        return self.name + " (" + self.tier_name + ")"


class SilverCustomer(Customer):
    tier_name = "silver"
    small_rate, large_rate, points_multiplier = 0.02, 0.05, 2


class GoldCustomer(Customer):
    tier_name = "gold"
    small_rate, large_rate, points_multiplier = 0.05, 0.10, 3


class PlatinumCustomer(Customer):
    tier_name = "platinum"
    small_rate, large_rate, points_multiplier = 0.10, 0.15, 5


TIER_CLASSES = {cls.tier_name: cls for cls in
                (Customer, SilverCustomer, GoldCustomer, PlatinumCustomer)}


def make_customer(name, tier):
    if tier not in TIER_CLASSES:
        raise ValueError("Unknown tier: " + tier)
    return TIER_CLASSES[tier](name)


# ------------------------------------------------------------------------------
#  Order  (has-a Customer, has-many OrderItem)   (Task A, D)
#  Calculation methods are pure: they return numbers and never print.
# ------------------------------------------------------------------------------
class Order:
    def __init__(self, customer, items):
        if not items:
            raise ValueError("An order needs at least one item")
        self.customer = customer
        self.items = list(items)

    # ---- pure calculations ----
    def subtotal(self):
        total = 0.0
        for item in self.items:
            total = total + item.line_total()
        return total

    def total_quantity(self):
        return sum(item.quantity for item in self.items)

    def discount(self):
        sub = self.subtotal()
        d = sub * self.customer.discount_rate(sub)
        if self.total_quantity() >= BULK_QTY_THRESHOLD:
            d = d + sub * BULK_DISCOUNT_RATE
        return d

    def tax(self):
        total = 0.0
        for item in self.items:
            total = total + item.line_tax()
        return total

    def total(self):
        return self.subtotal() - self.discount() + self.tax()

    def points(self):
        return int(self.total() // POINTS_DIVISOR) * self.customer.points_multiplier

    # ---- presentation (uses the calculations, does no maths of its own) ----
    def receipt(self):
        rule = "-" * RECEIPT_WIDTH
        lines = ["Receipt for " + str(self.customer), rule]
        lines += [str(item) for item in self.items]
        lines += [
            rule,
            "Subtotal: " + str(round(self.subtotal(), 2)),
            "Discount: " + str(round(self.discount(), 2)),
            "Tax: " + str(round(self.tax(), 2)),
            "Total: " + str(round(self.total(), 2)),
            "Points earned: " + str(self.points()),
        ]
        return "\n".join(lines)


# ------------------------------------------------------------------------------
#  Building objects from the legacy data (tuples -> objects, once, at the edge)
# ------------------------------------------------------------------------------
def build_catalog(raw_products):
    return [make_product(name, price, cat) for name, price, cat in raw_products]


def build_orders(raw_orders, catalog):
    orders = []
    for name, tier, raw_items in raw_orders:
        items = [OrderItem(catalog[index], qty) for index, qty in raw_items]
        orders.append(Order(make_customer(name, tier), items))
    return orders


def refactored_main():
    """Print every receipt and the grand total — same output as legacy_main()."""
    catalog = build_catalog(PRODUCTS)
    orders = build_orders(ORDERS, catalog)
    grand = 0.0
    for order in orders:
        print(order.receipt())
        print("")
        grand = grand + order.total()
    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


# ==============================================================================
#  SELF-TEST  —  DO NOT EDIT.   Run:  python Assignment_03.py
# ==============================================================================
def _check():
    try:
        your_output = capture(refactored_main)
    except NotImplementedError:
        print("Solution not implemented yet.\n")
        print("Below is the TARGET output your refactor must reproduce exactly:\n")
        print(GOLDEN_OUTPUT)
        return

    if your_output == GOLDEN_OUTPUT:
        print("PASS - behaviour is unchanged. Your refactor is safe.\n")
    else:
        print("FAIL - the output changed, so this is not yet a valid refactor.\n")
        g = GOLDEN_OUTPUT.splitlines()
        y = your_output.splitlines()
        for i in range(max(len(g), len(y))):
            gl = g[i] if i < len(g) else "<no line>"
            yl = y[i] if i < len(y) else "<no line>"
            if gl != yl:
                print("First difference at line " + str(i + 1) + ":")
                print("  expected: " + repr(gl))
                print("  yours:    " + repr(yl))
                break


if __name__ == "__main__":
    _check()


# ==============================================================================
#  RUBRIC (10 pts)
#   Behaviour preserved (self-test PASS) .................. 2
#   Domain modelling & composition ....................... 2
#   Polymorphism (tier discount & points, no if/elif) .... 1.5
#   Pure calculation vs I/O separation ................... 1.5
#   Encapsulation & validation ........................... 1
#   Clean code (names, no magic numbers, DRY, no global).. 1
#   CHANGES.md explanation (per-change, before->after) ...  0.5
#   CHANGES.md prompt log (Level-2) ......................  0.5
#  NOTE: passing the test alone is only 20/100 — most marks are for the DESIGN
#        and for explaining and verifying your changes. 
# ==============================================================================
