# =====================================================================
# Case Study 5 : Multi-Plan Telecommunications Cost Optimization
# ---------------------------------------------------------------------
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, pattern generation,
#                 lists, nested lists, tuples, tuple operations,
#                 unpacking.
# =====================================================================

# ----------------------------- Plan table ----------------------------
# plan = (code, name, data GB, minutes, SMS, validity days, price,
#         Rs per extra GB, Rs per extra minute)
# SMS excess is charged at a flat rate below.
SMS_EXCESS_RATE = 0.25

plans = [
    ("P1", "TalkLite", 1, 100, 100, 28, 199, 80, 0.25),
    ("P2", "DataMax", 2, 300, 300, 28, 399, 70, 0.20),
    ("P3", "PowerPlus", 5, 1000, 1000, 28, 649, 60, 0.10),
    ("P4", "Smart90", 3, 500, 500, 90, 999, 65, 0.15),
    ("P5", "Economy", 0.5, 50, 50, 28, 99, 90, 0.30),
]

# ------------------------------- Usage data --------------------------
# usage = (label, data GB, minutes, SMS, days needed, budget Rs)
usages = [
    ("Light user, one month", 1.5, 120, 50, 30, 500),
    ("Heavy user, three months", 4.5, 950, 200, 90, 1500),
    ("Tight budget, one month", 2, 200, 100, 28, 150),
]

# ---------------------------- Program banner -------------------------
title = "MULTI-PLAN TELECOMMUNICATIONS COST OPTIMIZATION"
print("=" * 74)
left_pad = (74 - 2 - len(title)) // 2
right_pad = 74 - 2 - len(title) - left_pad
print("=" + " " * left_pad + title + " " * right_pad + "=")
print("=" * 74)
print("Pack cost = ceil(days / validity) x price; excess usage is charged")
print("per extra GB / minute / SMS beyond the packs that were bought")
print("A plan is eligible when its total cost stays within the budget")

# --------------------------- Main processing -------------------------
case_number = 0
for label, need_data, need_min, need_sms, need_days, budget in usages:
    case_number = case_number + 1
    print()
    print("=== TEST CASE " + str(case_number) + ": " + label + " ===")
    print("-" * 74)
    print("Requirement: " + str(need_data) + " GB, " + str(need_min)
          + " min, " + str(need_sms) + " SMS over " + str(need_days)
          + " days | Budget Rs " + str(budget))
    print("-" * 74)

    plan_rows = []   # one tuple per plan, see below

    for code, name, data_gb, minutes, sms, validity, price, gb_rate, min_rate in plans:
        # packs needed so that validity covers the required days
        packs = (need_days + validity - 1) // validity
        base = packs * price

        # allowances after buying the packs
        total_data = data_gb * packs
        total_min = minutes * packs
        total_sms = sms * packs

        # excess usage charges
        extra_data = need_data - total_data
        if extra_data < 0:
            extra_data = 0
        extra_min = need_min - total_min
        if extra_min < 0:
            extra_min = 0
        extra_sms = need_sms - total_sms
        if extra_sms < 0:
            extra_sms = 0

        data_cost = extra_data * gb_rate
        min_cost = extra_min * min_rate
        sms_cost = extra_sms * SMS_EXCESS_RATE
        excess_total = data_cost + min_cost + sms_cost
        total = round(base + excess_total, 2)

        eligible = total <= budget
        plan_rows = plan_rows + [(code, name, packs, base,
                                  data_cost, min_cost, sms_cost,
                                  total, eligible)]

    # ---------------- comparison table ----------------
    print(f"{'Code':<6}{'Plan':<12}{'Packs':>6}{'Base':>10}"
          f"{'Excess':>10}{'Total':>10}  Eligible")
    print("-" * 74)
    for code, name, packs, base, d_cost, m_cost, s_cost, total, eligible in plan_rows:
        excess = d_cost + m_cost + s_cost
        flag = "YES" if eligible else "no"
        print(f"{code:<6}{name:<12}{packs:>6}{base:>10.2f}"
              f"{round(excess, 2):>10.2f}{total:>10.2f}  {flag}")

    # ---------------- pick the cheapest eligible plan ----------------
    print()
    best_code = ""
    best_total = -1
    best_excess = -1
    best_name = ""
    best_row = ()
    for row in plan_rows:
        r_code, r_name, r_packs, r_base, r_d, r_m, r_s, r_total, r_ok = row
        if r_ok:
            r_excess = r_d + r_m + r_s
            if best_total < 0:
                choose = True
            elif r_total < best_total:
                choose = True
            elif r_total == best_total and r_excess < best_excess:
                choose = True
            else:
                choose = False
            if choose:
                best_total = r_total
                best_excess = r_excess
                best_code = r_code
                best_name = r_name
                best_row = row

    if best_total >= 0:
        print("MOST ECONOMICAL ELIGIBLE PLAN: " + best_code + " "
              + best_name + f" - Rs {best_total:.2f}"
              + " (budget Rs " + str(budget) + ")")
        r_code, r_name, r_packs, r_base, r_d, r_m, r_s, r_total, r_ok = best_row
        print("  Breakdown: " + str(r_packs) + f" pack(s) = Rs {r_base:.2f}"
              + f" + excess data Rs {r_d:.2f}"
              + f" + excess minutes Rs {r_m:.2f}"
              + f" + excess SMS Rs {r_s:.2f}")
    else:
        # no plan fits: find the cheapest plan and the shortfall
        cheapest_total = -1
        cheapest_code = ""
        cheapest_name = ""
        for row in plan_rows:
            r_code, r_name, r_packs, r_base, r_d, r_m, r_s, r_total, r_ok = row
            if cheapest_total < 0 or r_total < cheapest_total:
                cheapest_total = r_total
                cheapest_code = r_code
                cheapest_name = r_name
        shortfall = round(cheapest_total - budget, 2)
        print("NO PLAN IS ELIGIBLE WITHIN THE BUDGET")
        print("  Cheapest option: " + cheapest_code + " " + cheapest_name
              + f" costs Rs {cheapest_total:.2f}"
              + f" - shortfall Rs {shortfall:.2f}")

    # ---------------- pattern generation: cost bars ----------------
    print("Cost bar chart (1 # = Rs 100):")
    for code, name, packs, base, d_cost, m_cost, s_cost, total, eligible in plan_rows:
        bars = ""
        for b in range(1, int(total // 100) + 1):
            bars = bars + "#"
        mark = " *" if (best_total >= 0 and code == best_code) else ""
        print("  " + code + " " + bars + " " + str(round(total)) + mark)

# ------------------------- Pattern generation ------------------------
print()
print("PATTERN - signal bars:")
for level in range(1, 6):
    line = ""
    for b in range(1, level + 1):
        line = line + "|" + " " * 3
    print("  " + line + "  " + str(level) + " bar(s)")
print("End of telecom plan report.")
