# =====================================================================
# Case Study 6 : Railway Fare and Reservation Calculator
# ---------------------------------------------------------------------
# Syllabus used : variables, data types, operators, conditional
#                 statements, loops, strings, pattern generation,
#                 lists, nested lists, tuples, tuple operations,
#                 unpacking.
# =====================================================================

# ---------------------------- Fare rules -----------------------------
# distance slabs: (upper limit of slab, rate per km) - first match wins
FARE_SLABS = [(100, 1.50), (500, 1.25), (1000, 1.00), (99999, 0.85)]

# travel classes: (code, label, fare multiplier, reservation fee)
CLASSES = [
    ("SL", "Sleeper", 1.00, 20),
    ("3A", "AC 3-Tier", 1.80, 40),
    ("2A", "AC 2-Tier", 2.50, 60),
    ("1A", "AC First", 3.20, 80),
]

CHILD_FREE_AGE = 5      # below this age: fare and fee are zero
CHILD_CONCESSION_AGE = 11   # 5 to 11 years: 50% concession
SENIOR_AGE = 60         # 60 years and above: 40% concession
CHILD_RATE = 0.50
SENIOR_RATE = 0.40

# cancellation penalties: (minimum hours before departure, penalty rate)
CANCEL_RULES = [(24, 0.10), (12, 0.30), (0, 1.00)]

# ------------------------------- Test data ---------------------------
# passenger = (name, age, distance km, class code, status, hours before
#              departure at the time of cancellation)

batch_one = [
    ("Anand", 35, 250, "SL", "BOOKED", 0),
    ("Bhavana", 62, 250, "3A", "BOOKED", 0),
    ("Chetan", 8, 200, "2A", "BOOKED", 0),
    ("Divya", 28, 1500, "1A", "BOOKED", 0),
    ("Eshwar", 45, 100, "SL", "BOOKED", 0),
]

batch_two = [
    ("Fatima", 30, 400, "3A", "CANCELLED", 30),
    ("Girish", 55, 600, "2A", "CANCELLED", 18),
    ("Harini", 40, 300, "SL", "CANCELLED", 6),
    ("Ishaan", 62, 500, "3A", "BOOKED", 0),
    ("Baby Kavi", 2, 200, "2A", "BOOKED", 0),
]

batch_three = [
    ("Jaya", 5, 100, "SL", "BOOKED", 0),
    ("Kiran", 11, 500, "SL", "BOOKED", 0),
    ("Lata", 60, 1000, "3A", "BOOKED", 0),
    ("Mohan", 12, 150, "SL", "BOOKED", 0),
    ("Naina", 60, 1500, "1A", "CANCELLED", 24),
]

# nested list: (description, list of passenger tuples)
batches = [
    ("Batch 1 - Mixed classes and ages, all booked", batch_one),
    ("Batch 2 - Cancellations at different notice times", batch_two),
    ("Batch 3 - Slab and age boundaries", batch_three),
]

# ---------------------------- Program banner -------------------------
title = "RAILWAY FARE AND RESERVATION CALCULATOR"
print("=" * 74)
left_pad = (74 - 2 - len(title)) // 2
right_pad = 74 - 2 - len(title) - left_pad
print("=" + " " * left_pad + title + " " * right_pad + "=")
print("=" * 74)
print("Fare slabs: <=100 km Rs 1.50/km | <=500 Rs 1.25 | <=1000 Rs 1.00")
print("           above 1000 Rs 0.85 per km (first matching slab)")
print("Classes: SL x1.00 fee 20 | 3A x1.80 fee 40 | 2A x2.50 fee 60")
print("         1A x3.20 fee 80 | Age: <5 free, 5-11 50% off, >=60 40% off")
print("Cancellation: >=24h 10% penalty | >=12h 30% | <12h 100%")

# --------------------------- Main processing -------------------------
case_number = 0
for batch_title, passengers in batches:
    case_number = case_number + 1
    print()
    print("=== TEST CASE " + str(case_number) + ": " + batch_title + " ===")
    print("-" * 74)

    total_collections = 0.0
    total_refunds = 0.0
    booked_count = 0
    cancelled_count = 0

    for name, age, distance, class_code, status, hours in passengers:
        # -------- travel class lookup --------
        class_label = ""
        multiplier = 1.0
        res_fee = 0
        found = False
        for c_code, c_label, c_mult, c_fee in CLASSES:
            if c_code == class_code:
                found = True
                class_label = c_label
                multiplier = c_mult
                res_fee = c_fee
        if not found:
            class_label = "Unknown"
            multiplier = 1.0
            res_fee = 0

        # -------- base fare: first matching distance slab --------
        rate = FARE_SLABS[0][1]
        slab_limit = FARE_SLABS[0][0]
        for limit, slab_rate in FARE_SLABS:
            if distance <= limit:
                rate = slab_rate
                slab_limit = limit
                break
        base_fare = round(distance * rate, 2)

        # -------- class fare and age concession --------
        class_fare = round(base_fare * multiplier, 2)
        concession_rate = 0.0
        concession_reason = "none"
        if age < CHILD_FREE_AGE:
            res_fee = 0
            concession_rate = 1.0
            concession_reason = "child under 5 (free)"
        elif age <= CHILD_CONCESSION_AGE:
            concession_rate = CHILD_RATE
            concession_reason = "child 5-11 (50%)"
        elif age >= SENIOR_AGE:
            concession_rate = SENIOR_RATE
            concession_reason = "senior 60+ (40%)"

        concession = round(class_fare * concession_rate, 2)
        fare_after = round(class_fare - concession, 2)
        ticket_value = round(fare_after + res_fee, 2)

        # -------- booking or cancellation --------
        print()
        print("--- " + name + " (" + str(age) + " y) : " + str(distance)
              + " km " + class_label + " | " + status
              + (("" if status == "BOOKED" else ", " + str(hours) + " h notice"))
              + " ---")
        print(f"  {'Base fare (' + str(distance) + ' km @ Rs ' + str(rate) + '/km)':<46}{base_fare:>9.2f}")
        print(f"  {'Class multiplier (' + class_label + ' x ' + str(multiplier) + ')':<46}{class_fare:>9.2f}")
        print(f"  {'Age concession (' + concession_reason + ')':<46}{0 - concession:>9.2f}")

        if status == "CANCELLED":
            penalty_rate = 1.0
            for min_hours, p_rate in CANCEL_RULES:
                if hours >= min_hours:
                    penalty_rate = p_rate
                    break
            penalty = round(ticket_value * penalty_rate, 2)
            refund = round(ticket_value - penalty, 2)
            print(f"  {'Reservation fee':<46}{res_fee:>9.2f}")
            print(f"  {'Ticket value':<46}{ticket_value:>9.2f}")
            print(f"  {'Cancellation penalty (' + str(round(penalty_rate * 100)) + '%)':<46}{0 - penalty:>9.2f}")
            print(f"  {'REFUND':<46}{refund:>9.2f}")
            total_refunds = total_refunds + refund
            cancelled_count = cancelled_count + 1
        else:
            print(f"  {'Reservation fee (' + class_label + ')':<46}{res_fee:>9.2f}")
            print(f"  {'TOTAL PAYABLE':<46}{ticket_value:>9.2f}")
            total_collections = total_collections + ticket_value
            booked_count = booked_count + 1

    # -------- batch summary --------
    net = round(total_collections - total_refunds, 2)
    print()
    print("-" * 74)
    print("  Booked: " + str(booked_count) + "  collections Rs "
          + f"{total_collections:.2f}")
    print("  Cancelled: " + str(cancelled_count) + "  refunds Rs "
          + f"{total_refunds:.2f}")
    print("  NET REVENUE Rs " + f"{net:.2f}")
    print("-" * 74)

# ------------------------- Pattern generation ------------------------
print()
print("PATTERN - rail track:")
for row in range(1, 4):
    print("  " + "-o" * (row * 8) + "-")
print("End of railway report.")
