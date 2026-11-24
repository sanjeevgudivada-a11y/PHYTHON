# =====================================================================
# Case Study 8 : Manufacturing Cost and Profitability Analysis
# ---------------------------------------------------------------------
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, pattern generation,
#                 lists, nested lists, tuples, tuple operations,
#                 unpacking.
# =====================================================================

# ----------------------------- Product data --------------------------
# product = (code, name,
#            [(material, qty per unit, rate per unit), ...]  <- BOM,
#            labour hours, labour rate per hour,
#            machine hours, machine rate per hour,
#            wastage %, units planned, units sold,
#            selling price per unit, target profit for the batch)

products = [
    ("M1", "Steel Bracket",
     [("Steel sheet", 1, 80), ("Bolt pack", 6, 5), ("Paint", 0.1, 200)],
     0.5, 300, 0.25, 400, 4.0, 1000, 950, 520, 80000),
    ("M2", "Plastic Bottle",
     [("Preform", 1, 15), ("Cap", 1, 2.5), ("Label", 1, 3.5)],
     0.2, 250, 0.1, 600, 6.0, 5000, 5000, 165, 150000),
    ("M3", "Wooden Chair",
     [("Plywood", 2, 450), ("Nails", 20, 1), ("Varnish", 0.3, 400)],
     2.0, 350, 0.5, 500, 5.0, 200, 180, 2600, 45000),
    ("M4", "Ceramic Mug",
     [("Body", 1, 40), ("Handle", 1, 8), ("Glaze", 0.2, 150)],
     0.4, 300, 0.2, 700, 8.0, 300, 0, 480, 10000),
]

# nested list: (description, list of product tuples)
batches = [
    ("Batch 1 - Clear winner (Steel Bracket)", [products[0]]),
    ("Batch 2 - Near miss and a bare pass", [products[1], products[2]]),
    ("Batch 3 - No sales at all (Ceramic Mug)", [products[3]]),
]

# ---------------------------- Program banner -------------------------
title = "MANUFACTURING COST AND PROFITABILITY ANALYSIS"
print("=" * 74)
left_pad = (74 - 2 - len(title)) // 2
right_pad = 74 - 2 - len(title) - left_pad
print("=" + " " * left_pad + title + " " * right_pad + "=")
print("=" * 74)
print("Unit cost = (material + labour + machine) x (1 + wastage %)")
print("Batch cost = unit cost x units planned")
print("Profit     = selling price x units sold - batch cost")
print("Target is met only when profit >= target profit for the batch")

# --------------------------- Main processing -------------------------
case_number = 0
for batch_title, batch in batches:
    case_number = case_number + 1
    print()
    print("=== TEST CASE " + str(case_number) + ": " + batch_title + " ===")
    print("-" * 74)

    met_count = 0
    not_met_count = 0
    sum_cost = 0.0
    sum_revenue = 0.0
    sum_profit = 0.0

    for (code, name, bom, lab_h, lab_rate, mac_h, mac_rate,
         wastage_pct, planned, sold, sell_price, target) in batch:
        print()
        print("--- " + code + " " + name + " ---")

        # -------- material cost from the nested BOM list --------
        material = 0.0
        for material_name, qty_per_unit, rate in bom:
            line_cost = qty_per_unit * rate
            material = material + line_cost
            print(f"  {'  ' + material_name + ' (' + str(qty_per_unit)
                   + ' x ' + str(rate) + ')':<44}{line_cost:>10.2f}")
        print(f"  {'Material cost per unit':<44}{material:>10.2f}")

        # -------- labour, machine, wastage --------
        labour = lab_h * lab_rate
        machine = mac_h * mac_rate
        print(f"  {'Labour (' + str(lab_h) + ' h x ' + str(lab_rate) + ')':<44}{labour:>10.2f}")
        print(f"  {'Machine (' + str(mac_h) + ' h x ' + str(mac_rate) + ')':<44}{machine:>10.2f}")

        base_cost = material + labour + machine
        wastage = base_cost * wastage_pct / 100
        unit_cost = base_cost + wastage
        print(f"  {'Sub-cost':<44}{base_cost:>10.2f}")
        print(f"  {'Wastage (' + str(wastage_pct) + '%)':<44}{wastage:>10.2f}")
        print("  " + "-" * 56)
        print(f"  {'UNIT COST':<44}{unit_cost:>10.2f}")

        # -------- batch economics --------
        batch_cost = unit_cost * planned
        revenue = sell_price * sold
        profit = revenue - batch_cost
        unsold = planned - sold
        print(f"  {'Batch cost (' + str(planned) + ' units)':<44}{batch_cost:>10.2f}")
        print(f"  {'Revenue (' + str(sold) + ' sold x ' + str(sell_price) + ')':<44}{revenue:>10.2f}")
        print(f"  {'Unsold inventory':<44}{unsold:>10}")

        if revenue > 0:
            margin = round(profit * 100 / revenue, 2)
            print(f"  {'Profit margin':<44}{margin:>9}%")
        else:
            print(f"  {'Profit margin':<44}{'n/a (no sales)':>10}")

        print("  " + "=" * 56)
        if profit >= target:
            met_count = met_count + 1
            print(f"  VERDICT: TARGET MET - profit {profit:,.2f} >= "
                  f"target {target:,.2f}")
        else:
            not_met_count = not_met_count + 1
            short_by = target - profit
            print(f"  VERDICT: TARGET NOT MET - profit {profit:,.2f} < "
                  f"target {target:,.2f} (short by {short_by:,.2f})")

        sum_cost = sum_cost + batch_cost
        sum_revenue = sum_revenue + revenue
        sum_profit = sum_profit + profit

    # -------- batch summary --------
    print()
    print("-" * 74)
    print(f"  {'Total batch cost':<40}{sum_cost:>16,.2f}")
    print(f"  {'Total revenue':<40}{sum_revenue:>16,.2f}")
    print(f"  {'Total profit':<40}{sum_profit:>16,.2f}")
    print("  Targets met: " + str(met_count)
          + "   not met: " + str(not_met_count))
    print("-" * 74)

# ------------------------- Pattern generation ------------------------
print()
print("PATTERN - production line:")
for row in range(1, 7):
    unit = "[] " if row % 2 == 1 else "## "
    line = ""
    for col in range(1, row + 1):
        line = line + unit
    print("  " + line)
print("End of manufacturing report.")
