# =====================================================================
# Case Study 10 : Campus Event Financial Planning
# ---------------------------------------------------------------------
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, pattern generation,
#                 lists, nested lists, tuples, tuple operations,
#                 unpacking.
# =====================================================================

# ----------------------------- Event data ----------------------------
sponsors = [("TechCorp", 20000), ("City Bank", 10000)]

# (stall type, number of stalls, rent per stall)
stalls = [("Food stall", 5, 1200), ("Tech stall", 4, 2250)]

fixed_expenses = [
    ("Venue hire", 20000),
    ("Sound and lighting", 15000),
    ("Marketing", 8000),
    ("Prizes and certificates", 15000),
]

CATERING_RATE = 80      # rupees per attendee
KIT_RATE = 30           # programme kit per attendee
BUS_COST = 8800         # 4 hired buses for the day
CONTINGENCY = 5         # percent of the direct expenses

# (scenario, paid tickets, free passes, ticket price)
scenarios = [
    ("Early bird rush", 800, 100, 200),
    ("Regular sales", 1200, 150, 250),
    ("Dull finale", 350, 300, 200),
]

# ---------------------------- Program banner -------------------------
title = "CAMPUS EVENT FINANCIAL PLANNING"
print("=" * 74)
left_pad = (74 - 2 - len(title)) // 2
right_pad = 74 - 2 - len(title) - left_pad
print("=" + " " * left_pad + title + " " * right_pad + "=")
print("=" * 74)
print("Income  = paid tickets + sponsorships + stall rents")
print("Expenses= fixed + buses + catering + kits + 5% contingency")
print("Profit >= 0 means the scenario is profitable")

# -------------------------- Shared income ----------------------------
sponsor_total = 0
for sponsor_name, sponsor_amount in sponsors:
    sponsor_total = sponsor_total + sponsor_amount
stall_total = 0
for stall_type, stall_count, stall_rent in stalls:
    stall_total = stall_total + stall_count * stall_rent
other_income = sponsor_total + stall_total

fixed_total = 0
for expense_name, expense_amount in fixed_expenses:
    fixed_total = fixed_total + expense_amount

print()
print("SPONSORS AND STALLS (shared by every scenario):")
for sponsor_name, sponsor_amount in sponsors:
    print(f"  {sponsor_name:<24}{sponsor_amount:>14,.2f}")
for stall_type, stall_count, stall_rent in stalls:
    amount = stall_count * stall_rent
    print(f"  {stall_type + ' (' + str(stall_count) + ' x ' + str(stall_rent) + ')':<24}{amount:>14,.2f}")
print(f"  {'Other income total':<24}{other_income:>14,.2f}")
print("FIXED EXPENSES:")
for expense_name, expense_amount in fixed_expenses:
    print(f"  {expense_name:<24}{expense_amount:>14,.2f}")
print(f"  {'Fixed total':<24}{fixed_total:>14,.2f}")

# --------------------------- Main processing -------------------------
case_number = 0
best_profit = -999999999
best_scenario = ""
profitable_count = 0

for scenario_name, paid, free_passes, ticket_price in scenarios:
    case_number = case_number + 1
    print()
    print("=== TEST CASE " + str(case_number) + ": " + scenario_name + " ===")
    print("-" * 74)

    # ------------------------- income -------------------------
    ticket_income = paid * ticket_price
    attendees = paid + free_passes
    total_income = ticket_income + other_income
    print(f"  {'Ticket sales (' + str(paid) + ' x ' + str(ticket_price) + ')':<44}{ticket_income:>14,.2f}")
    print(f"  {'Sponsorships + stalls':<44}{other_income:>14,.2f}")
    print(f"  {'TOTAL INCOME':<44}{total_income:>14,.2f}")

    # ------------------------ expenses ------------------------
    catering = attendees * CATERING_RATE
    kits = attendees * KIT_RATE
    direct = fixed_total + BUS_COST + catering + kits
    contingency = direct * CONTINGENCY / 100
    total_expenses = direct + contingency
    print(f"  {'Fixed expenses':<44}{fixed_total:>14,.2f}")
    print(f"  {'Hired buses':<44}{BUS_COST:>14,.2f}")
    print(f"  {'Catering (' + str(attendees) + ' x ' + str(CATERING_RATE) + ')':<44}{catering:>14,.2f}")
    print(f"  {'Programme kits (' + str(attendees) + ' x ' + str(KIT_RATE) + ')':<44}{kits:>14,.2f}")
    print(f"  {'Contingency (' + str(CONTINGENCY) + '%)':<44}{contingency:>14,.2f}")
    print(f"  {'TOTAL EXPENSES':<44}{total_expenses:>14,.2f}")

    # ------------------------ verdict -------------------------
    profit = total_income - total_expenses
    margin = profit * 100 / total_income
    print(f"  {'PROFIT':<44}{profit:>14,.2f}")
    print(f"  {'Profit margin':<44}{margin:>13,.2f}%")

    if profit >= 0:
        profitable_count = profitable_count + 1
        print("  VERDICT: PROFITABLE - the event can run this way")
    else:
        print("  VERDICT: LOSS - this scenario cannot be funded")

    if profit > best_profit:
        best_profit = profit
        best_scenario = scenario_name

    # ------------- break-even scan (loop search) --------------
    break_even = -1
    for need in range(0, 2001):
        scan_income = need * ticket_price + other_income
        scan_attendees = need + free_passes
        scan_direct = (fixed_total + BUS_COST
                       + scan_attendees * CATERING_RATE
                       + scan_attendees * KIT_RATE)
        scan_expenses = scan_direct + scan_direct * CONTINGENCY / 100
        if scan_income - scan_expenses >= 0:
            break_even = need
            break
    if break_even >= 0:
        print(f"  Break-even paid tickets: {break_even} "
              f"(at Rs {ticket_price} with {free_passes} free passes)")
    else:
        print("  Break-even paid tickets: not reachable within 2000")

# -------------------------- Event summary ----------------------------
print()
print("EVENT SUMMARY")
print("-" * 74)
print(f"  {'Profitable scenarios':<40}{profitable_count:>4} of {len(scenarios)}")
print(f"  {'Best scenario':<40}{best_scenario:>20}")
print(f"  {'Best profit':<40}{best_profit:>20,.2f}")
print("-" * 74)

# ------------------------- Pattern generation ------------------------
print()
print("PATTERN - stage lights:")
for row in range(1, 6):
    line = ""
    for col in range(1, 7):
        if (row + col) % 2 == 0:
            line = line + "O "
        else:
            line = line + ". "
    print("  " + line)
print("End of event plan.")
