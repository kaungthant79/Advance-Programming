# Assignment 03 — CHANGES

**Name:** ______________________  **Student ID:** ______________________

## 1 · What I changed

| # | Code smell in the original | What I changed it to | OOP concept applied | How I verified behaviour was unchanged |
|---|---|---|---|---|
| 1 | Products stored as bare tuples `("Laptop", 1200.0, "electronics")` and looked up by index `PRODUCTS[pi][1]` | `Product` class with `name`, `price`; `OrderItem` has-a `Product`; `Order` has-a `Customer` and has-many `OrderItem`; tuples converted to objects once in `build_catalog` / `build_orders` | Classes, composition | `python Assignment_03.py` → PASS |
| 2 | Repeated `if t == "silver" ... elif "gold" ...` for discount AND for points | `Customer` base class (tier `none`) with `SilverCustomer`, `GoldCustomer`, `PlatinumCustomer`; each sets `small_rate`, `large_rate`, `points_multiplier`. `discount_rate(subtotal)` is written once in the base class | Inheritance, polymorphism | PASS; compared all 4 orders (all 4 tiers) |
| 3 | `if cat == "food": ... else: ...` inside the totals loop | `Product.tax_rate()` overridden by `FoodProduct`; `OrderItem.line_tax()` just asks the product. No category check in `Order` | Polymorphism (stretch F) | PASS (food lines still tax 0.0) |
| 4 | `calc()` mixes maths and `print()` in one 50-line function | `Order.subtotal/discount/tax/total/points` return numbers and never print; `Order.receipt()` only formats text; `refactored_main()` does the printing | Pure functions vs modifiers; interface vs implementation | PASS; grep shows no `print` inside calculation methods |
| 5 | Magic numbers (`0.07`, `100`, `10`, `0.03`, `40`), leftover `global TAXRATE`, unvalidated data | Named constants `TAX_RATE`, `DISCOUNT_THRESHOLD`, `BULK_QTY_THRESHOLD`, `BULK_DISCOUNT_RATE`, `POINTS_DIVISOR`, `RECEIPT_WIDTH`; no `global`; constructors raise `ValueError` (qty >= 1, price >= 0, non-empty names, known tier/category, non-empty order) | Encapsulation, validation | PASS |
| 6 | Output strings built inline | `__str__` on `Product`, `OrderItem`, `Customer` | Stretch G | PASS |

## 2 · Short reflection (4–6 sentences)

Replacing the tier `if/elif` chains with a class family improved the code most: the tier rules now live in one small class each, the discount and points logic was written once instead of twice, and adding a tier means adding one subclass. Keeping the output identical forced care with floating-point arithmetic: I kept the same order of operations (accumulating `sub` and `tax` item by item, `total = sub - d + tax`), because changing the order could change the last digit and break the string comparison. The bulk discount also had to stay `>= 10` while the tier discount stays `> 100`, and the `int(total // 10)` had to be applied before the multiplier. I also kept the receipt's blank line after each order, since the self-test compares every character.

## 3 · Prompt log (Level 2 — required)

> ⚠️ Edit this table so it reflects what YOU actually did. Add any other prompts you used and how you checked the results.

| # | My prompt to the AI | What it suggested (summary) | Accept / reject / edited | How I checked it |
|---|---|---|---|---|
| 1 | "do this assignment" (uploaded Assignment_03.py and CHANGES.md) | Full refactor: Product/OrderItem/Customer-family/Order classes, named constants, pure calc methods, filled change table | Accepted / edited: ______ | Ran the self-test (PASS); read every class and traced one order by hand |
| 2 |  |  |  |  |

**Ownership statement.** *By submitting, I confirm I understand and can explain every line of code I submitted, and that this prompt log reflects my actual AI use.*

Signed: ______________________

## 4 · Before-you-submit checklist

- [x] `python Assignment_03.py` prints **PASS**.
- [x] No tuples / parallel lists left in the solution — products, orders, and items are objects (tuples only remain in the untouchable legacy data, converted at the edge).
- [x] No `if tier == ...` chains — tiers are a class family.
- [x] Calculation methods **return** values and do not `print`; printing is separate.
- [x] Constructors validate state; no leftover `global`; magic numbers are named.
- [x] The change table and reflection above are filled in.
- [ ] The prompt log is complete and the ownership statement is signed (you do this).
