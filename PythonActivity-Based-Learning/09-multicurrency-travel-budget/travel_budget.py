# =====================================================================
# Case Study 9 : Multi-Currency Travel Budget Analysis
# ---------------------------------------------------------------------
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, pattern generation,
#                 lists, nested lists, tuples, tuple operations,
#                 unpacking.
# =====================================================================

# ----------------------------- Currency data -------------------------
# exchange_rates: 1 INR buys `rate` units of the foreign currency
exchange_rates = [
    ("Thailand", "THB", 0.42),
    ("Japan", "JPY", 1.75),
    ("UAE", "AED", 0.044),
    ("USA", "USD", 0.012),
]

# itineraries: nested list of (country, [(item, local price), ...])
itineraries = [
    ("Thailand",
     [("Hotel 3 nights", 6000), ("Food tour", 1500), ("Temple passes", 500)]),
    ("Japan",
     [("Rail pass", 30000), ("Hotel 2 nights", 26000), ("Museums", 4000)]),
    ("UAE",
     [("Desert safari", 850), ("Hotel 2 nights", 1100),
      ("Airport transfer", 250)]),
    ("USA",
     [("City tour", 300), ("Hotel 3 nights", 1050), ("Museum", 80)]),
]

# test cases: (title, budget in INR, [countries to visit])
test_cases = [
    ("Grand tour within budget", 120000, ["Thailand", "Japan", "UAE"]),
    ("One leg exceeds the pot", 60000, ["Thailand", "USA", "Japan"]),
    ("Single expensive leg", 120000, ["USA"]),
]

FEE_RATE = 2          # bank conversion fee, percent of the INR value

# ---------------------------- Program banner -------------------------
title = "MULTI-CURRENCY TRAVEL BUDGET ANALYSIS"
print("=" * 74)
left_pad = (74 - 2 - len(title)) // 2
right_pad = 74 - 2 - len(title) - left_pad
print("=" + " " * left_pad + title + " " * right_pad + "=")
print("=" * 74)
print("Local price is converted with: INR = local / rate")
print("A 2% bank fee is added on the INR value of every leg")
print("A leg is covered only when its cost fits the remaining budget")

# --------------------------- Rate table ------------------------------
print()
print("CURRENCY RATES (foreign units per INR 1):")
for country, code, rate in exchange_rates:
    print(f"  {country:<12} {code:<5} 1 INR = {rate} {code}")

# --------------------------- Main processing -------------------------
case_number = 0
for title_text, budget, legs in test_cases:
    case_number = case_number + 1
    print()
    print("=== TEST CASE " + str(case_number) + ": " + title_text + " ===")
    print("-" * 74)
    print(f"  Budget: Rs {budget:,.2f}    Bank fee: {FEE_RATE}%")

    remaining = budget
    covered = 0
    skipped = 0
    total_spent = 0.0

    for country in legs:
        # ---- locate the exchange rate for this country ----
        rate = -1.0
        for rc, code, r in exchange_rates:
            if rc == country:
                rate = r
                currency = code
        # ---- locate the itinerary and sum the local prices ----
        local_total = 0.0
        items = []
        for ic, item_list in itineraries:
            if ic == country:
                items = item_list
        print()
        print("--- " + country + " ---")
        for item_name, local_price in items:
            local_total = local_total + local_price
            print(f"  {item_name + ' = ' + str(local_price) + ' ' + currency:<40}"
                  f"{local_price:>12,.2f}")
        print(f"  {'Local total':<40}{local_total:>12,.2f} {currency}")

        # ---- conversion and fee ----
        inr_value = local_total / rate
        fee = inr_value * FEE_RATE / 100
        country_cost = inr_value + fee
        print(f"  {'Converted INR':<40}{inr_value:>12,.2f}")
        print(f"  {'Bank fee (' + str(FEE_RATE) + '%)':<40}{fee:>12,.2f}")
        print(f"  {'COUNTRY COST':<40}{country_cost:>12,.2f}")

        # ---- affordability decision ----
        if country_cost <= remaining:
            remaining = remaining - country_cost
            total_spent = total_spent + country_cost
            covered = covered + 1
            print(f"  STATUS: COVERED - budget left Rs {remaining:,.2f}")
        else:
            short_by = country_cost - remaining
            skipped = skipped + 1
            print(f"  STATUS: SKIPPED - need Rs {country_cost:,.2f} but only "
                  f"Rs {remaining:,.2f} left (short Rs {short_by:,.2f})")

    # -------- trip summary --------
    print()
    print("-" * 74)
    print(f"  {'Countries covered':<40}{covered:>4} of {len(legs)}")
    print(f"  {'Total spent':<40}{total_spent:>16,.2f}")
    print(f"  {'Budget left':<40}{remaining:>16,.2f}")
    print("  Legs skipped: " + str(skipped))
    print("-" * 74)

# ------------------------- Pattern generation ------------------------
print()
print("PATTERN - passport stamp:")
for row in range(1, 6):
    line = ""
    for col in range(1, 6):
        distance = abs(row - 3) + abs(col - 3)
        if distance <= 2:
            line = line + "@"
        else:
            line = line + "."
    print("  " + line)
print("End of travel budget report.")
