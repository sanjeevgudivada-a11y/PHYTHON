# =====================================================================
# Case Study 3 : Hospital Billing and Patient Classification
# ---------------------------------------------------------------------
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, pattern generation,
#                 lists, nested lists, tuples, tuple operations,
#                 unpacking.
# =====================================================================

# ---------------------------- Charge tables --------------------------
# nested lists of (key, charge) tuples
CONSULTATIONS = [("General", 500), ("Specialist", 800), ("Consultant", 1200)]
ROOM_RENTS = [("General", 1500), ("Semi-Private", 3000), ("Private", 6000)]
TEST_PRICES = [
    ("Blood Test", 350), ("X-Ray", 700), ("MRI", 2500),
    ("ECG", 400), ("Sugar Test", 200), ("Ultrasound", 900),
]
PROCEDURES = [
    ("None", 0), ("Minor Surgery", 8000),
    ("Major Surgery", 25000), ("Physiotherapy", 3000),
]

# supplied payment policy: (minimum payable, maximum payable, class)
CLASS_POLICY = [
    (0, 5000, "A - Economy"),
    (5000, 15000, "B - Standard"),
    (15000, 50000, "C - Premium"),
    (50000, 99999999, "D - Critical Care"),
]

MIN_AGE = 1
MAX_AGE = 120
MIN_DAYS = 1
MAX_DAYS = 60
SENIOR_AGE = 60
SUPER_SENIOR_AGE = 70
CHILD_AGE = 12
SENIOR_RATE = 0.10
SUPER_SENIOR_RATE = 0.20
CHILD_RATE = 0.15

# ------------------------------- Test data ---------------------------
# patient = (pid, name, age, consult type, days, room type,
#            procedure, [tests])
batch_one = [
    ("P101", "Ramesh Kumar", 68, "Consultant", 3, "Private",
     "Minor Surgery", ["Blood Test", "ECG"]),
    ("P102", "Aarav Sharma", 8, "Specialist", 2, "Semi-Private",
     "Physiotherapy", ["X-Ray", "Sugar Test"]),
]

batch_two = [
    ("P103", "Sushma Devi", 60, "General", 60, "General",
     "None", ["Blood Test"]),
    ("P104", "Kiara Patel", 12, "General", 1, "General",
     "None", []),
    ("P105", "Mohan Lal", 70, "Specialist", 1, "Semi-Private",
     "None", ["ECG"]),
]

batch_three = [
    ("P106", "Bad Days", 40, "General", 0, "General", "None", []),
    ("P107", "Bad Room", 40, "General", 2, "Deluxe", "None", []),
    ("P108", "Bad Age", 200, "General", 2, "General", "None", []),
    ("P109", "Bad Test", 35, "General", 2, "General", "None", ["CT Scan"]),
    ("P110", "Valid Senior", 62, "General", 2, "General",
     "None", ["Blood Test"]),
]

# nested list: (description, list of patient tuples)
batches = [
    ("Batch 1 - Valid patients with concessions", batch_one),
    ("Batch 2 - Age boundary patients", batch_two),
    ("Batch 3 - Validation failures and one control", batch_three),
]

# ---------------------------- Program banner -------------------------
title = "HOSPITAL BILLING AND PATIENT CLASSIFICATION"
print("*" * 70)
left_pad = (70 - 2 - len(title)) // 2
right_pad = 70 - 2 - len(title) - left_pad
print("*" + " " * left_pad + title + " " * right_pad + "*")
print("*" * 70)
print("Concessions: age >= 70 -> 20% | age >= 60 -> 10% | age <= 12 -> 15%")
print("Validation: age 1-120, days 1-60, known consult/room/procedure/tests")
print("Classes: A < 5000 | B 5000-15000 | C 15000-50000 | D >= 50000")

# --------------------------- Main processing -------------------------
case_number = 0
for batch_title, patients in batches:
    case_number = case_number + 1
    print()
    print("=== TEST CASE " + str(case_number) + ": " + batch_title + " ===")
    print("-" * 70)

    valid_count = 0
    invalid_count = 0

    for pid, name, age, consult, days, room, procedure, tests in patients:
        print()
        print("--- " + pid + " " + name + " (" + str(age) + " yrs) ---")

        # ---------------- validation ----------------
        errors = []
        if age < MIN_AGE or age > MAX_AGE:
            errors = errors + ["age must be between 1 and 120"]
        if days < MIN_DAYS or days > MAX_DAYS:
            errors = errors + ["days must be between 1 and 60"]

        consult_fee = 0
        found = False
        for key, charge in CONSULTATIONS:
            if key == consult:
                found = True
                consult_fee = charge
        if not found:
            errors = errors + ["unknown consultation type: " + consult]

        room_rate = 0
        found = False
        for key, charge in ROOM_RENTS:
            if key == room:
                found = True
                room_rate = charge
        if not found:
            errors = errors + ["unknown room type: " + room]

        procedure_fee = 0
        found = False
        for key, charge in PROCEDURES:
            if key == procedure:
                found = True
                procedure_fee = charge
        if not found:
            errors = errors + ["unknown procedure: " + procedure]

        test_total = 0
        for t in tests:
            price = 0
            found = False
            for key, charge in TEST_PRICES:
                if key == t:
                    found = True
                    price = charge
            if not found:
                errors = errors + ["unknown test: " + t]
            else:
                test_total = test_total + price

        # ---------------- billing (only if valid) ----------------
        if len(errors) > 0:
            invalid_count = invalid_count + 1
            print("  INVALID RECORD - billing skipped")
            for e in errors:
                print("    ! " + e)
            continue

        valid_count = valid_count + 1
        room_total = room_rate * days
        subtotal = consult_fee + room_total + procedure_fee + test_total

        # ---------------- conditional concession ----------------
        rate = 0.0
        reason = "no concession"
        if age >= SUPER_SENIOR_AGE:
            rate = SUPER_SENIOR_RATE
            reason = "senior citizen (age >= 70)"
        elif age >= SENIOR_AGE:
            rate = SENIOR_RATE
            reason = "senior citizen (age >= 60)"
        elif age <= CHILD_AGE:
            rate = CHILD_RATE
            reason = "child (age <= 12)"

        concession = round(subtotal * rate, 2)
        payable = round(subtotal - concession, 2)

        # ---------------- itemised bill ----------------
        print(f"  {'Consultation (' + consult + ')':<42}{consult_fee:>10.2f}")
        print(f"  {'Room rent (' + room + ' x ' + str(days) + ' day(s))':<42}{room_total:>10.2f}")
        print(f"  {'Procedure (' + procedure + ')':<42}{procedure_fee:>10.2f}")
        if len(tests) == 0:
            print(f"  {'Tests':<42}{test_total:>10.2f}")
        else:
            test_line = "Tests: "
            for t in tests:
                test_line = test_line + t + "  "
            print(f"  {test_line:<42}{test_total:>10.2f}")
        print("  " + "-" * 52)
        print(f"  {'Subtotal':<42}{subtotal:>10.2f}")
        print(f"  {'Concession (' + reason + ')':<42}{0 - concession:>10.2f}")
        print("  " + "=" * 52)
        print(f"  {'PAYABLE':<42}{payable:>10.2f}")

        # ---------------- classification ----------------
        pay_class = "unclassified"
        for cmin, cmax, cname in CLASS_POLICY:
            if payable >= cmin and payable < cmax:
                pay_class = cname
        print("  Classification: " + pay_class)

    # ---------------- batch summary ----------------
    print()
    print("Summary: valid = " + str(valid_count)
          + "  invalid = " + str(invalid_count))

# ------------------------- Pattern generation ------------------------
print()
print("PATTERN - cross rows:")
for row in range(1, 5):
    line = ""
    for col in range(1, 5):
        if (row + col) % 2 == 0:
            line = line + "+ "
        else:
            line = line + ". "
    print("  " + line)
print("End of hospital billing report.")
