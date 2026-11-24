# =====================================================================
# Case Study 4 : Employee Payroll and Deduction Analysis
# ---------------------------------------------------------------------
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, pattern generation,
#                 lists, nested lists, tuples, tuple operations,
#                 unpacking.
# =====================================================================

# ---------------------------- Pay rules ------------------------------
HRA_RATE = 0.40           # house rent allowance, 40% of basic
DA_RATE = 0.10            # dearness allowance, 10% of basic
TA_FIXED = 3000           # transport allowance, fixed
OT_RATE = 150             # rupees per overtime hour
PF_RATE = 0.12            # provident fund, 12% of basic
MAX_PF = 1800             # PF is capped at this amount

# professional tax: (gross upper limit, tax charge)
PT_SLABS = [(10000, 0), (15000, 110), (20000, 200), (99999999, 300)]

# progressive income tax: (cumulative upper limit, rate on the slice)
TAX_SLABS = [
    (250000, 0.00),
    (500000, 0.05),
    (1000000, 0.10),
    (99999999, 0.20),
]

# ------------------------------- Test data ---------------------------
# employee = (emp id, name, basic pay, overtime hours, incentive)

batch_one = [
    ("E101", "Ravi Teja", 12000, 0, 0),
    ("E102", "Sunita Rao", 8000, 0, 0),
    ("E103", "Deepa Menon", 45000, 20, 5000),
]

batch_two = [
    ("E104", "Arun Prasad", 200000, 10, 0),
    ("E105", "Meena Krishnan", 350000, 0, 0),
]

batch_three = [
    ("E106", "Kiran Joshi", 166000, 0, 100),
]

# nested list: (description, list of employee tuples)
batches = [
    ("Batch 1 - Employees with no income tax", batch_one),
    ("Batch 2 - Employees entering income-tax slabs", batch_two),
    ("Batch 3 - Boundary: taxable income exactly 2,50,000", batch_three),
]

# ---------------------------- Program banner -------------------------
title = "EMPLOYEE PAYROLL AND DEDUCTION ANALYSIS"
print("=" * 62)
left_pad = (62 - 2 - len(title)) // 2
right_pad = 62 - 2 - len(title) - left_pad
print("=" + " " * left_pad + title + " " * right_pad + "=")
print("=" * 62)
print("Gross = basic + HRA 40% + DA 10% + TA 3000 + OT x 150 + incentive")
print("Deductions: PF 12% of basic (max 1800) + professional tax slab")
print("            + progressive tax (0% to 2.5L, 5% to 5L, 10% to 10L, 20%)")

# --------------------------- Main processing -------------------------
case_number = 0
for batch_title, employees in batches:
    case_number = case_number + 1
    print()
    print("=== TEST CASE " + str(case_number) + ": " + batch_title + " ===")
    print("-" * 62)

    sum_gross = 0.0
    sum_deductions = 0.0
    sum_net = 0.0

    for emp_id, name, basic, ot_hours, incentive in employees:
        # ------------------- gross salary -------------------
        hra = basic * HRA_RATE
        da = basic * DA_RATE
        ot_pay = ot_hours * OT_RATE
        gross = basic + hra + da + TA_FIXED + ot_pay + incentive

        # ------------------- deductions -------------------
        pf = basic * PF_RATE
        if pf > MAX_PF:
            pf = MAX_PF

        pt = 0
        for limit, charge in PT_SLABS:
            if gross <= limit:
                pt = charge
                break

        taxable = gross - pf - pt
        tax = 0.0
        remaining = taxable
        previous_limit = 0
        for limit, rate in TAX_SLABS:
            span = limit - previous_limit
            slice_amount = remaining
            if slice_amount > span:
                slice_amount = span
            if slice_amount > 0:
                tax = tax + slice_amount * rate
                remaining = remaining - slice_amount
            previous_limit = limit
            if remaining <= 0:
                break

        tax = round(tax, 2)
        total_deductions = round(pf + pt + tax, 2)
        net = round(gross - total_deductions, 2)

        # ------------------- formatted statement -------------------
        print()
        print("#" * 62)
        print("# " + emp_id + "  " + name)
        print("#" * 62)
        print(f"  {'Basic salary':<38}{basic:>12.2f}")
        print(f"  {'HRA (40% of basic)':<38}{hra:>12.2f}")
        print(f"  {'DA (10% of basic)':<38}{da:>12.2f}")
        print(f"  {'Transport allowance':<38}{TA_FIXED:>12.2f}")
        print(f"  {'Overtime (' + str(ot_hours) + ' hrs x Rs 150)':<38}{ot_pay:>12.2f}")
        print(f"  {'Incentive':<38}{incentive:>12.2f}")
        print("  " + "-" * 50)
        print(f"  {'GROSS SALARY':<38}{gross:>12.2f}")
        print(f"  {'PF (12% of basic, max 1800)':<38}{pf:>12.2f}")
        print(f"  {'Professional tax':<38}{pt:>12.2f}")
        print(f"  {'Income tax (progressive)':<38}{tax:>12.2f}")
        print("  " + "-" * 50)
        print(f"  {'TOTAL DEDUCTIONS':<38}{total_deductions:>12.2f}")
        print(f"  {'NET TAKE-HOME':<38}{net:>12.2f}")
        print("#" * 62)

        rate_pct = round(total_deductions * 100 / gross, 2)
        print("  Deduction rate = " + str(rate_pct) + "% of gross")

        sum_gross = sum_gross + gross
        sum_deductions = sum_deductions + total_deductions
        sum_net = sum_net + net

    # ------------------- batch summary -------------------
    count = len(employees)
    print()
    print("-" * 62)
    print(f"  {'Batch total gross':<38}{sum_gross:>12.2f}")
    print(f"  {'Batch total deductions':<38}{sum_deductions:>12.2f}")
    print(f"  {'Batch total net':<38}{sum_net:>12.2f}")
    print(f"  {'Average net per employee':<38}{round(sum_net / count, 2):>12.2f}")
    print("-" * 62)

# ------------------------- Pattern generation ------------------------
print()
print("PATTERN - salary diamond:")
for row in range(1, 6):
    line = ""
    for col in range(1, row + 1):
        line = line + "* "
    print(" " * (5 - row) + line)
for row in range(4, 0, -1):
    line = ""
    for col in range(1, row + 1):
        line = line + "* "
    print(" " * (5 - row) + line)
print("End of payroll report.")
