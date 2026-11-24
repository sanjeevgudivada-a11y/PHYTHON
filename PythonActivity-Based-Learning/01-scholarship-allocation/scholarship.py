# =====================================================================
# Case Study 1 : University Scholarship Allocation
# ---------------------------------------------------------------------
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, pattern generation,
#                 lists, nested lists, tuples, tuple operations,
#                 unpacking.
# =====================================================================

# --------------------- Decision rules (constants) ---------------------
MIN_AGGREGATE = 75          # minimum aggregate marks out of 100
MIN_SUBJECT_MARK = 40       # minimum mark required in EVERY subject
MIN_ATTENDANCE = 70         # minimum attendance percentage
MAX_FAMILY_INCOME = 500000  # maximum annual family income in rupees
BANNER_WIDTH = 64

# ------------------------------- Test data ---------------------------
# applicant = (name, aggregate, (m1, m2, m3, m4), attendance, income)

batch_one = [
    ("Asha Rao", 84.5, (78, 82, 91, 87), 92, 420000),
    ("Vikram Iyer", 76.0, (55, 62, 71, 80), 71, 380000),
    ("Meera Nair", 91.5, (88, 94, 90, 94), 96, 250000),
    ("Rohan Das", 68.0, (72, 65, 70, 66), 85, 300000),
    ("Sara Khan", 84.5, (80, 85, 88, 85), 90, 450000),
    ("Deepak Joshi", 79.0, (45, 60, 75, 82), 68, 550000),
    ("Anita Paul", 88.0, (84, 90, 86, 92), 88, 600000),
    ("Kabir Sen", 91.5, (85, 92, 95, 94), 96, 250000),
]

batch_two = [
    ("Neha Verma", 90.0, (87, 91, 92, 90), 95, 480000),
    ("Arjun Reddy", 82.5, (75, 80, 85, 88), 80, 350000),
    ("Isha Gupta", 87.0, (82, 88, 90, 86), 91, 499000),
]

batch_three = [
    ("Ravi Kumar", 74.0, (70, 72, 75, 78), 75, 300000),
    ("Tina Roy", 80.0, (60, 65, 70, 72), 65, 250000),
    ("Amit Shah", 85.0, (80, 82, 84, 86), 80, 750000),
    ("Pooja Das", 60.0, (35, 40, 45, 50), 55, 200000),
]

# nested list: every element is (description, list of applicant tuples)
batches = [
    ("Batch 1 - Mixed applicants (eligible and rejected)", batch_one),
    ("Batch 2 - All applicants eligible", batch_two),
    ("Batch 3 - No applicant eligible", batch_three),
]

# ---------------------------- Program banner --------------------------
title = "UNIVERSITY SCHOLARSHIP ALLOCATION"
print("*" * BANNER_WIDTH)
left_pad = (BANNER_WIDTH - 2 - len(title)) // 2
right_pad = BANNER_WIDTH - 2 - len(title) - left_pad
print("*" + " " * left_pad + title + " " * right_pad + "*")
print("*" * BANNER_WIDTH)
print("Rules: aggregate >= " + str(MIN_AGGREGATE)
      + " | every subject >= " + str(MIN_SUBJECT_MARK)
      + " | attendance >= " + str(MIN_ATTENDANCE)
      + " | income <= " + str(MAX_FAMILY_INCOME))
print("Tie-break: Aggregate DESC > Attendance DESC > Income ASC > Name ASC")

# --------------------------- Main processing -------------------------
case_number = 0
for batch_title, applicants in batches:
    case_number = case_number + 1
    print()
    print("=== TEST CASE " + str(case_number) + ": " + batch_title + " ===")
    print("-" * BANNER_WIDTH)

    eligible = []      # list of (aggregate, attendance, income, name, lowest)
    rejected = []      # list of (name, reason string)

    # -------- table header (string formatting) --------
    print(f"{'Name':<15}{'Agg':>7}{'SubjMin':>9}{'Att':>6}{'Income':>11}  Status")
    print("-" * BANNER_WIDTH)

    for name, aggregate, subjects, attendance, income in applicants:
        # find the lowest subject mark by looping over the tuple
        lowest = subjects[0]
        for mark in subjects:
            if mark < lowest:
                lowest = mark

        # collect every violated rule as a list of reason strings
        parts = []
        if aggregate < MIN_AGGREGATE:
            parts = parts + ["aggregate below cutoff"]
        if lowest < MIN_SUBJECT_MARK:
            parts = parts + ["subject below minimum"]
        if attendance < MIN_ATTENDANCE:
            parts = parts + ["attendance below cutoff"]
        if income > MAX_FAMILY_INCOME:
            parts = parts + ["income above limit"]

        # concatenate the reason parts with a separator (loop, no functions)
        reason = ""
        for p in parts:
            if reason != "":
                reason = reason + ", "
            reason = reason + p

        if reason == "":
            eligible = eligible + [(aggregate, attendance, income, name, lowest)]
            status = "ELIGIBLE"
        else:
            rejected = rejected + [(name, reason)]
            status = "REJECTED"

        print(f"{name:<15}{aggregate:>7.1f}{lowest:>9}{attendance:>6}"
              f"{income:>11,}  {status}")

    # -------- rejection reasons --------
    if len(rejected) > 0:
        print()
        print("Rejection reasons:")
        for name, reason in rejected:
            print("  - " + name + " : " + reason)

    # -------- ranking with tie-break rules --------
    print()
    if len(eligible) == 0:
        print("No eligible students in this batch.")
    else:
        ranks = []   # list of (rank, name, aggregate, attendance, income)
        for e in eligible:
            e_agg, e_att, e_inc, e_name, e_low = e   # tuple unpacking
            better_count = 0
            for o in eligible:
                o_agg, o_att, o_inc, o_name, o_low = o
                is_better = False
                if o_agg > e_agg:
                    is_better = True
                elif o_agg == e_agg and o_att > e_att:
                    is_better = True
                elif o_agg == e_agg and o_att == e_att and o_inc < e_inc:
                    is_better = True
                elif (o_agg == e_agg and o_att == e_att
                      and o_inc == e_inc and o_name < e_name):
                    is_better = True
                if is_better:
                    better_count = better_count + 1
            ranks = ranks + [(better_count + 1, e_name, e_agg, e_att, e_inc)]

        print("RANKED LIST OF ELIGIBLE STUDENTS")
        print(f"{'Rank':<6}{'Name':<15}{'Agg':>7}{'Att':>6}{'Income':>11}")
        print("-" * BANNER_WIDTH)
        for position in range(1, len(ranks) + 1):
            for r in ranks:
                rank_no, r_name, r_agg, r_att, r_inc = r
                if rank_no == position:
                    print(f"{rank_no:<6}{r_name:<15}{r_agg:>7.1f}"
                          f"{r_att:>6}{r_inc:>11,}")

    # -------- batch summary --------
    print("-" * BANNER_WIDTH)
    print(f"Summary: total={len(applicants)}  eligible={len(eligible)}"
          f"  rejected={len(rejected)}")

# ------------------------- Pattern generation ------------------------
print()
print("PATTERN - star pyramid closing the report:")
for row in range(1, 6):
    line = ""
    for col in range(1, row + 1):
        line = line + "* "
    print(" " * (6 - row) + line)
print("End of scholarship report.")
