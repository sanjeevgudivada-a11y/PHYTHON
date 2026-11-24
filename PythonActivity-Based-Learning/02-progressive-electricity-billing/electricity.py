# =====================================================================
# Case Study 2 : Progressive Electricity Billing
# ---------------------------------------------------------------------
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, pattern generation,
#                 lists, nested lists, tuples, tuple operations,
#                 unpacking.
# =====================================================================

# --------------------------- Billing rules ---------------------------
# progressive energy slabs: (upper limit of slab, rate per unit)
SLABS = [(100, 2.50), (300, 4.00), (500, 6.50), (999999, 8.75)]

# fixed monthly charge by connected load: (maximum kW, fixed charge)
LOAD_CHARGES = [(5, 90), (10, 150), (9999, 260)]

DUTY_RATE = 0.05            # electricity duty on energy charge
FUEL_RATE = 0.03            # fuel adjustment charge on energy charge
GREEN_REBATE_RATE = 0.05    # conservation rebate on energy charge
GREEN_REBATE_LIMIT = 200    # units below or equal to this get the rebate
PROMPT_REBATE_RATE = 0.02   # prompt-payment rebate on the subtotal
UNUSUAL_INCREASE_PCT = 20   # month-on-month rise treated as unusual

# ----------------------------- Test data -----------------------------
# household = (name, connected load in kW,
#              [(month, units consumed, paid on time?), ...])

households = [
    ("Shanti Nilayam", 5, [
        ("Jan", 140, True), ("Feb", 165, True), ("Mar", 190, False),
        ("Apr", 240, True), ("May", 310, True), ("Jun", 280, True),
    ]),
    ("Green Villa", 10, [
        ("Jan", 90, True), ("Feb", 95, True), ("Mar", 260, True),
        ("Apr", 310, True), ("May", 690, False), ("Jun", 720, True),
    ]),
    ("Boundary House", 3, [
        ("Jan", 100, True), ("Feb", 300, True), ("Mar", 500, True),
        ("Apr", 100, True), ("May", 99, True), ("Jun", 120, True),
    ]),
]

# ---------------------------- Program banner -------------------------
title = "PROGRESSIVE ELECTRICITY BILLING"
print("=" * 68)
left_pad = (68 - 2 - len(title)) // 2
right_pad = 68 - 2 - len(title) - left_pad
print("=" + " " * left_pad + title + " " * right_pad + "=")
print("=" * 68)
print("Slabs: 0-100 @ Rs 2.50 | 101-300 @ Rs 4.00 | 301-500 @ Rs 6.50")
print("       above 500 @ Rs 8.75 per unit")
print("Surcharges: duty 5% + fuel 3% of energy | Rebates: green 5% if")
print("units <= 200, prompt 2% if paid on time")
print("Unusual increase: month-on-month units rise > "
      + str(UNUSUAL_INCREASE_PCT) + "%")

# --------------------------- Main processing -------------------------
case_number = 0
all_totals = []   # list of (household name, total units, total bill)

for hh_name, load_kw, readings in households:
    case_number = case_number + 1

    # find the fixed charge for this connected load
    fixed = 0
    for max_kw, charge in LOAD_CHARGES:
        if load_kw <= max_kw:
            fixed = charge
            break

    print()
    print("=== TEST CASE " + str(case_number) + ": " + hh_name
          + " (" + str(load_kw) + " kW load, fixed Rs " + str(fixed) + ") ===")
    print("-" * 68)

    bills = []   # list of (month, units, energy, surcharge, rebate, bill)

    for month, units, paid_on_time in readings:
        # ---- progressive slab energy charge ----
        remaining = units
        energy = 0.0
        previous_limit = 0
        for limit, rate in SLABS:
            span = limit - previous_limit
            take = remaining
            if take > span:
                take = span
            if take > 0:
                energy = energy + take * rate
                remaining = remaining - take
            previous_limit = limit
            if remaining <= 0:
                break

        # ---- fixed charge, surcharges, rebates ----
        duty = energy * DUTY_RATE
        fuel = energy * FUEL_RATE
        surcharge = duty + fuel
        subtotal = energy + fixed + surcharge

        green_rebate = 0.0
        if units <= GREEN_REBATE_LIMIT:
            green_rebate = energy * GREEN_REBATE_RATE

        prompt_rebate = 0.0
        if paid_on_time:
            prompt_rebate = subtotal * PROMPT_REBATE_RATE

        rebate = green_rebate + prompt_rebate
        bill = round(subtotal - rebate, 2)
        bills = bills + [(month, units, energy, surcharge, rebate, bill)]

    # ---- monthly comparison table ----
    print(f"{'Month':<7}{'Units':>7}{'Energy':>10}{'Fixed':>9}"
          f"{'Surcharges':>12}{'Rebates':>10}{'Bill':>11}")
    print("-" * 68)
    total_units = 0
    total_bill = 0.0
    for month, units, energy, surcharge, rebate, bill in bills:
        total_units = total_units + units
        total_bill = total_bill + bill
        print(f"{month:<7}{units:>7}{energy:>10.2f}{fixed:>9.2f}"
              f"{surcharge:>12.2f}{0 - rebate:>10.2f}{bill:>11.2f}")
    print("-" * 68)
    print(f"{'TOTAL':<7}{total_units:>7}{'':>10}{'':>9}{'':>12}"
          f"{'':>10}{round(total_bill, 2):>11.2f}")
    average_bill = round(total_bill / len(bills), 2)
    print("Average monthly bill: Rs " + str(average_bill))

    # ---- highest and lowest bill months ----
    high = bills[0]
    low = bills[0]
    for b in bills:
        if b[5] > high[5]:
            high = b
        if b[5] < low[5]:
            low = b
    print("Highest bill: " + high[0] + " (Rs " + str(high[5]) + ")"
          + "   Lowest bill: " + low[0] + " (Rs " + str(low[5]) + ")")

    # ---- slab breakdown of the highest-usage month ----
    max_units = 0
    for b in bills:
        if b[1] > max_units:
            max_units = b[1]
    detail = ""
    remaining = max_units
    previous_limit = 0
    for limit, rate in SLABS:
        span = limit - previous_limit
        take = remaining
        if take > span:
            take = span
        if take > 0:
            if detail != "":
                detail = detail + " + "
            detail = detail + str(take) + "u@" + str(rate)
            remaining = remaining - take
        previous_limit = limit
        if remaining <= 0:
            break
    print("Slab breakdown of " + str(max_units) + " units: " + detail)

    # ---- detect unusual month-on-month increases ----
    print("Unusual increases (units rise > "
          + str(UNUSUAL_INCREASE_PCT) + "%):")
    found_unusual = False
    for i in range(1, len(bills)):
        prev = bills[i - 1]
        cur = bills[i]
        rise = (cur[1] - prev[1]) * 100 / prev[1]
        if rise > UNUSUAL_INCREASE_PCT:
            found_unusual = True
            print("  ! " + cur[0] + ": " + str(prev[1]) + " -> "
                  + str(cur[1]) + " units (+" + str(round(rise, 1))
                  + "%), bill Rs " + str(prev[5]) + " -> Rs " + str(cur[5]))
    if not found_unusual:
        print("  none")

    # ---- pattern generation: bill bar chart ----
    print("Bill bar chart (1 star = Rs 100):")
    for month, units, energy, surcharge, rebate, bill in bills:
        stars = ""
        for s in range(1, int(bill // 100) + 1):
            stars = stars + "*"
        print("  " + month + " " + stars + " " + str(round(bill)))

    all_totals = all_totals + [(hh_name, total_units, round(total_bill, 2))]

# ------------------- Cross-household comparison ----------------------
print()
print("=== HOUSEHOLD COMPARISON (6 months) ===")
print("-" * 68)
print(f"{'Household':<18}{'Total Units':>13}{'Total Bill':>13}{'Avg Bill':>11}")
print("-" * 68)
for hh_name, t_units, t_bill in all_totals:
    print(f"{hh_name:<18}{t_units:>13}{t_bill:>13.2f}"
          f"{round(t_bill / 6, 2):>11.2f}")
print("-" * 68)

# ------------------------- Pattern generation ------------------------
print()
print("PATTERN - closing strip:")
strip = ""
for i in range(1, 15):
    strip = strip + "=" if i % 2 == 1 else strip + "-"
print(strip)
print("End of electricity billing report.")
