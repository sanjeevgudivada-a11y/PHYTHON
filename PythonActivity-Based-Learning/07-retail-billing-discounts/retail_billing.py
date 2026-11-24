# =====================================================================
# Case Study 7 : Retail Billing with Multiple Discount Rules
# ---------------------------------------------------------------------
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, pattern generation,
#                 lists, nested lists, tuples, tuple operations,
#                 unpacking.
# =====================================================================

# ---------------------------- Product tables -------------------------
# nested list: (product name, category, unit price)
PRODUCTS = [
    ("Rice 5kg", "Grocery", 450),
    ("Soap Bar", "Grocery", 60),
    ("USB Cable", "Electronics", 350),
    ("Earphones", "Electronics", 1200),
    ("T-Shirt", "Apparel", 600),
    ("Jacket", "Apparel", 1800),
    ("Notebook", "Stationery", 120),
    ("Pen Set", "Stationery", 150),
]

# category tax rates: (category, rate)
CAT_RATES = [
    ("Grocery", 0.00),
    ("Electronics", 0.18),
    ("Apparel", 0.05),
    ("Stationery", 0.12),
]

# threshold discounts checked from the highest threshold: (min subtotal, rate)
DISCOUNT_THRESHOLDS = [
    (20000, 0.20),
    (10000, 0.15),
    (5000, 0.10),
    (0, 0.00),
]

MAX_CONCESSION = 3000   # total discount can never exceed this

# ------------------------------- Test data ---------------------------
# cart = list of (product name, quantity)
cart_one = [
    ("Rice 5kg", 2), ("USB Cable", 1), ("T-Shirt", 3),
    ("Earphones", 1), ("Pen Set", 2), ("Jacket", 1),
]

cart_two = [
    ("T-Shirt", 10), ("Earphones", 15),
]

cart_three = [
    ("Rice 5kg", 1), ("Milk Pack", 2), ("Soap Bar", -1), ("Pen Set", 3),
]

# nested list: (description, cart)
batches = [
    ("Cart 1 - Mixed basket crossing the 10% threshold", cart_one),
    ("Cart 2 - Large basket where the cap limits the concession", cart_two),
    ("Cart 3 - Invalid lines and a below-threshold basket", cart_three),
]

# ---------------------------- Program banner -------------------------
title = "RETAIL BILLING WITH MULTIPLE DISCOUNT RULES"
print("=" * 76)
left_pad = (76 - 2 - len(title)) // 2
right_pad = 76 - 2 - len(title) - left_pad
print("=" + " " * left_pad + title + " " * right_pad + "=")
print("=" * 76)
print("Discount on subtotal: >=20000 20% | >=10000 15% | >=5000 10%")
print("Maximum concession on any bill: Rs " + str(MAX_CONCESSION))
print("Tax after proportional discount: Grocery 0% | Electronics 18%")
print("                                Apparel 5% | Stationery 12%")

# --------------------------- Main processing -------------------------
case_number = 0
for cart_title, cart in batches:
    case_number = case_number + 1
    print()
    print("=== TEST CASE " + str(case_number) + ": " + cart_title + " ===")
    print("-" * 76)
    invoice_no = "INV-" + str(100 + case_number)

    # -------- scan the cart --------
    lines = []          # (name, category, qty, rate, amount)
    subtotal = 0.0
    invalid_count = 0

    for product_name, qty in cart:
        price = 0
        category = ""
        found = False
        for p_name, p_cat, p_price in PRODUCTS:
            if p_name == product_name:
                found = True
                category = p_cat
                price = p_price

        if not found:
            invalid_count = invalid_count + 1
            print("  ERROR: unknown product '" + product_name
                  + "' - line skipped")
        elif qty <= 0:
            invalid_count = invalid_count + 1
            print("  ERROR: quantity " + str(qty) + " for '" + product_name
                  + "' must be positive - line skipped")
        else:
            amount = price * qty
            lines = lines + [(product_name, category, qty, price, amount)]
            subtotal = subtotal + amount

    if len(lines) == 0:
        print("No billable items - invoice " + invoice_no + " not issued")
        continue

    # -------- threshold discount, capped --------
    discount_rate = 0.0
    for threshold, rate in DISCOUNT_THRESHOLDS:
        if subtotal >= threshold:
            discount_rate = rate
            break
    raw_discount = subtotal * discount_rate
    discount = raw_discount
    capped = False
    if discount > MAX_CONCESSION:
        discount = MAX_CONCESSION
        capped = True

    # -------- per-category tax on the discounted share --------
    cat_totals = []     # accumulator list (category, tax so far)
    for cat, c_rate in CAT_RATES:
        cat_totals = cat_totals + [(cat, 0.0)]

    itemised_tax = 0.0
    for name, category, qty, rate, amount in lines:
        share = 0.0
        if subtotal > 0:
            share = discount * amount / subtotal
        taxable = amount - share
        line_tax = 0.0
        for cat, c_rate in CAT_RATES:
            if cat == category:
                line_tax = taxable * c_rate
        itemised_tax = itemised_tax + line_tax
        # add the tax of this line into its category accumulator
        updated = []
        for cat, running in cat_totals:
            if cat == category:
                running = running + line_tax
            updated = updated + [(cat, running)]
        cat_totals = updated

    grand_total = subtotal - discount + itemised_tax

    # -------- print the invoice --------
    print()
    print("INVOICE " + invoice_no + "  -  " + cart_title)
    print("=" * 76)
    print(f"  {'Item':<16}{'Category':<14}{'Qty':>5}{'Rate':>9}{'Amount':>11}")
    print("  " + "-" * 55)
    for name, category, qty, rate, amount in lines:
        print(f"  {name:<16}{category:<14}{qty:>5}{rate:>9.2f}{amount:>11.2f}")
    print("  " + "-" * 55)
    print(f"  {'Subtotal':<46}{subtotal:>12.2f}")

    disc_label = "Discount (" + str(int(discount_rate * 100)) + "% threshold)"
    if capped:
        disc_label = ("Discount capped at max "
                      + str(MAX_CONCESSION) + " (rule gave "
                      + str(round(raw_discount)) + ")")
    print(f"  {disc_label:<46}{0 - discount:>12.2f}")
    print(f"  {'Net taxable value':<46}{subtotal - discount:>12.2f}")
    print("  " + "-" * 55)
    for cat, running in cat_totals:
        label = "Tax on " + cat
        print(f"  {label:<46}{running:>12.2f}")
    print("  " + "=" * 76)
    print(f"  {'GRAND TOTAL':<46}{grand_total:>12.2f}")
    print("=" * 76)
    if invalid_count > 0:
        print("  Lines skipped: " + str(invalid_count))

# ------------------------- Pattern generation ------------------------
print()
print("PATTERN - barcode:")
for row in range(1, 9):
    bar = ""
    for col in range(1, 34):
        if (col * 3 + row * 2) % 7 < 3:
            bar = bar + "#"
        else:
            bar = bar + " "
    print("  " + bar)
print("End of retail billing report.")
