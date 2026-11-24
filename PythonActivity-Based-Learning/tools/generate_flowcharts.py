#!/usr/bin/env python3
"""Flowchart generator for PythonActivity-Based-Learning.

Converts compact nested-list flowchart specifications into clean SVG files.

Spec node forms:
    ["term", text]                                  -> stadium (Start/End)
    ["proc", text]                                  -> process rectangle
    ["io", text]                                    -> input/output parallelogram
    ["dec", text, then_seq, else_seq]               -> decision diamond
    ["dec", text, then_seq, else_seq, t_lab, e_lab] -> decision with custom labels
    ["while", text, body_seq]                       -> loop condition
                                                      (Yes -> body on the side,
                                                       No  -> exit downward,
                                                       back-edge returns to top)

Branches of a decision either both terminate (must be the last step) or both
rejoin before the flow continues. Layout columns are allocated automatically so
nested decisions never overlap.
"""

LINE_H = 17          # text line height inside nodes
GAP = 46             # vertical gap between successive nodes
SIDE_DX = 380        # horizontal distance between layout columns
BACK_OFF = 190       # left channel offset used by loop back-edges
MAIN_X = 340         # x coordinate of the main (primary) column
EDGE_GAP = 30        # space left between a decision and its first branch node
REJOIN_STUB = 14     # extra height after the taller branch before rejoining

FONT = "DejaVu Sans, Verdana, sans-serif"
STROKE = "#334155"
TEXT_C = "#0f172a"


def wrap(text, max_chars):
    """Greedy word wrap of a label into lines of at most max_chars."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        if not cur:
            cur = w
        elif len(cur) + 1 + len(w) <= max_chars:
            cur = cur + " " + w
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines if lines else [""]


class Flowchart:
    def __init__(self, title):
        self.title = title
        self.nodes = []
        self.edges = []      # tuples describing lines/polylines
        self.labels = []     # (x, y, text)
        self.col = 0         # side-column counter
        self.main_x = MAIN_X
        self.min_x = 1e9
        self.max_x = -1e9
        self.min_y = 1e9
        self.max_y = -1e9

    # ---------- tracking ----------
    def track(self, x, y):
        self.min_x = min(self.min_x, x)
        self.max_x = max(self.max_x, x)
        self.min_y = min(self.min_y, y)
        self.max_y = max(self.max_y, y)

    def track_box(self, nd):
        self.track(nd["cx"] - nd["w"] / 2, nd["cy"] - nd["h"] / 2)
        self.track(nd["cx"] + nd["w"] / 2, nd["cy"] + nd["h"] / 2)

    # ---------- geometry helpers ----------
    def make_node(self, kind, text):
        if kind == "term":
            maxc, minw, minh, padx, pady = 20, 170, 46, 40, 14
        elif kind in ("proc", "io"):
            maxc, minw, minh, padx, pady = 27, 210, 48, 36, 15
        else:  # dec
            maxc, minw, minh, padx, pady = 23, 240, 88, 56, 42
        lines = wrap(text, maxc)
        tw = max(len(l) for l in lines) * 7.9
        w = max(minw, tw + 2 * padx)
        h = max(minh, len(lines) * LINE_H + 2 * pady)
        return {"kind": kind, "lines": lines, "w": w, "h": h}

    def edge_v(self, x, y1, y2, arrow=True):
        self.edges.append(("v", x, y1, y2, arrow))
        self.track(x, y1)
        self.track(x, y2)

    def edge_h(self, y, x1, x2, arrow=True):
        self.edges.append(("h", y, x1, x2, arrow))
        self.track(x1, y)
        self.track(x2, y)

    def edge_path(self, points, end_dir):
        self.edges.append(("path", points, end_dir))
        for px, py in points:
            self.track(px, py)

    def place_label(self, x, y, text):
        self.labels.append((x, y, text))
        self.track(x, y)

    # ---------- layout ----------
    def layout(self, seq, x, y, depth, prev=None):
        """Lay out a sequence of nodes. Returns (bottom_y, x_used)."""
        cx = x
        for i, node in enumerate(seq):
            kind = node[0]
            if kind in ("term", "proc", "io"):
                nd = self.make_node(kind, node[1])
                nd["cx"] = cx
                nd["cy"] = y + nd["h"] / 2
                self.nodes.append(nd)
                self.track_box(nd)
                if prev is not None:
                    self.edge_v(cx, prev, y)
                prev = y + nd["h"]
                y = prev + GAP

            elif kind == "dec":
                nd = self.make_node("dec", node[1])
                nd["cx"] = cx
                nd["cy"] = y + nd["h"] / 2
                self.nodes.append(nd)
                self.track_box(nd)
                d_top, d_bot, cy = y, y + nd["h"], nd["cy"]
                d_right = cx + nd["w"] / 2
                if prev is not None:
                    self.edge_v(cx, prev, d_top)

                then_seq = node[2] if len(node) > 2 else []
                else_seq = node[3] if len(node) > 3 else []
                t_lab = node[4] if len(node) > 4 and node[4] else "Yes"
                e_lab = node[5] if len(node) > 5 and node[5] else "No"

                # then-branch continues straight down
                self.place_label(cx + 13, d_bot + EDGE_GAP - 12, t_lab)
                then_end = d_bot + EDGE_GAP
                if then_seq:
                    then_end, _ = self.layout(
                        then_seq, cx, d_bot + EDGE_GAP, depth + 1, prev=d_bot)

                # else-branch leaves from the right point of the diamond.
                # Its column is claimed AFTER the then-branch so that nested
                # decisions receive the nearer columns (fewer line crossings).
                self.col += 1
                side_x = self.main_x + SIDE_DX * self.col
                else_top = cy + 42
                if else_seq:
                    self.place_label(d_right + 14, cy - 9, e_lab)
                    self.edge_h(cy, d_right, side_x, arrow=False)
                    self.edge_v(side_x, cy, else_top, arrow=True)
                    else_end, _ = self.layout(
                        else_seq, side_x, else_top, depth + 1, prev=None)
                else:
                    self.place_label(d_right + 14, cy - 9, e_lab)
                    else_end = cy

                then_term = bool(then_seq) and then_seq[-1][0] == "term"
                else_term = bool(else_seq) and else_seq[-1][0] == "term"

                if then_term and else_term:
                    if i != len(seq) - 1:
                        raise ValueError(
                            "decision with two terminating branches must be last")
                    prev = None
                    y = max(then_end, else_end)
                elif then_term or else_term:
                    raise ValueError(
                        "one branch terminates while the other continues")
                else:
                    rejoin_y = max(then_end, else_end) + REJOIN_STUB
                    if else_seq:
                        self.edge_v(side_x, else_end, rejoin_y, arrow=False)
                    else:
                        self.edge_h(cy, d_right, side_x, arrow=False)
                        self.edge_v(side_x, cy, rejoin_y, arrow=False)
                    self.edge_h(rejoin_y, side_x, cx, arrow=True)
                    if then_end < rejoin_y:
                        self.edge_v(cx, then_end, rejoin_y, arrow=False)
                    prev = rejoin_y
                    y = rejoin_y + GAP

            elif kind == "while":
                nd = self.make_node("dec", node[1])
                nd["cx"] = cx
                nd["cy"] = y + nd["h"] / 2
                self.nodes.append(nd)
                self.track_box(nd)
                d_top, d_bot, cy = y, y + nd["h"], nd["cy"]
                d_right = cx + nd["w"] / 2
                if prev is not None:
                    self.edge_v(cx, prev, d_top)

                body = node[2] if len(node) > 2 else []
                self.col += 1
                side_x = self.main_x + SIDE_DX * self.col

                self.place_label(d_right + 14, cy - 9, "Yes")
                self.place_label(cx + 13, d_bot + EDGE_GAP - 12, "No")
                body_end = d_bot
                if body:
                    body_top = cy + 42
                    self.edge_h(cy, d_right, side_x, arrow=False)
                    self.edge_v(side_x, cy, body_top, arrow=True)
                    body_end, _ = self.layout(
                        body, side_x, body_top, depth + 1, prev=None)
                    # Back-edge: body bottom -> up through the channel that
                    # sits BETWEEN the condition column and the body column,
                    # then over the top into the condition box. Routing the
                    # channel to the right of the condition (instead of the
                    # far left) keeps the bottom segment inside the column
                    # gap so it never cuts through process boxes.
                    chx = cx + BACK_OFF
                    self.edge_path(
                        [(side_x, body_end),
                         (side_x, body_end + 28),
                         (chx, body_end + 28),
                         (chx, d_top - 32),
                         (cx, d_top - 32),
                         (cx, d_top)],
                        end_dir="down")
                # The "No" exit spine continues BELOW the loop body, so any
                # later side-branch line in this column starts under the
                # body's boxes instead of cutting through them.
                if body_end > d_bot:
                    self.edge_v(cx, d_bot, body_end, arrow=False)
                prev = max(d_bot, body_end)
                y = prev + GAP

            else:
                raise ValueError("unknown node type: %r" % (kind,))

        return (prev if prev is not None else y), cx

    # ---------- rendering ----------
    @staticmethod
    def arrow(x, y, d, s=9.5):
        if d == "down":
            pts = (x, y), (x - s * 0.55, y - s), (x + s * 0.55, y - s)
        elif d == "up":
            pts = (x, y), (x - s * 0.55, y + s), (x + s * 0.55, y + s)
        elif d == "right":
            pts = (x, y), (x - s, y - s * 0.55), (x - s, y + s * 0.55)
        else:  # left
            pts = (x, y), (x + s, y - s * 0.55), (x + s, y + s * 0.55)
        return '<polygon points="%s" fill="%s"/>' % (
            " ".join("%.1f,%.1f" % p for p in pts), STROKE)

    def node_svg(self, nd):
        cx, cy, w, h = nd["cx"], nd["cy"], nd["w"], nd["h"]
        x, y = cx - w / 2, cy - h / 2
        k = nd["kind"]
        if k == "term":
            shape = ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
                     'rx="%.1f" fill="#dbeafe" stroke="#2563eb" stroke-width="2"/>'
                     % (x, y, w, h, h / 2))
        elif k == "proc":
            shape = ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="5" '
                     'fill="#ffffff" stroke="%s" stroke-width="2"/>'
                     % (x, y, w, h, STROKE))
        elif k == "io":
            s = 16
            pts = [(x + s, y), (x + w, y), (x + w - s, y + h), (x, y + h)]
            shape = '<polygon points="%s" fill="#dcfce7" stroke="#16a34a" stroke-width="2"/>' % (
                " ".join("%.1f,%.1f" % p for p in pts))
        else:  # dec
            pts = [(cx, y), (x + w, cy), (cx, y + h), (x, cy)]
            shape = '<polygon points="%s" fill="#fef9c3" stroke="#b45309" stroke-width="2"/>' % (
                " ".join("%.1f,%.1f" % p for p in pts))

        lines = nd["lines"]
        n = len(lines)
        first_y = cy - (n - 1) * LINE_H / 2 + 4.5
        tspans = []
        for j, ln in enumerate(lines):
            tspans.append('<tspan x="%.1f" dy="%s">%s</tspan>' % (
                cx, "0" if j == 0 else str(LINE_H),
                ln.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")))
        text = ('<text font-family="%s" font-size="13" fill="%s" '
                'text-anchor="middle">%s</text>' % (FONT, TEXT_C, "".join(tspans)))
        # first tspan needs explicit y
        text = text.replace('<tspan x="%.1f" dy="0">' % cx,
                            '<tspan x="%.1f" dy="0" y="%.1f">' % (cx, first_y), 1)
        return shape + text

    def edge_svg(self, e):
        out = []
        if e[0] == "v":
            _, x, y1, y2, arrow = e
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                       'stroke="%s" stroke-width="1.8"/>' % (x, y1, x, y2, STROKE))
            if arrow:
                d = "down" if y2 >= y1 else "up"
                out.append(self.arrow(x, y2, d))
        elif e[0] == "h":
            _, y, x1, x2, arrow = e
            out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                       'stroke="%s" stroke-width="1.8"/>' % (x1, y, x2, y, STROKE))
            if arrow:
                d = "right" if x2 >= x1 else "left"
                out.append(self.arrow(x2, y, d))
        else:  # path - drawn as consecutive line segments (universal support)
            _, pts, end_dir = e
            for j in range(len(pts) - 1):
                x1, y1 = pts[j]
                x2, y2 = pts[j + 1]
                out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" '
                           'stroke="%s" stroke-width="1.8"/>'
                           % (x1, y1, x2, y2, STROKE))
            ex, ey = pts[-1]
            out.append(self.arrow(ex, ey, end_dir))
        return "".join(out)

    def to_svg(self):
        pad = 38
        x0 = self.min_x - pad
        y0 = self.min_y - 58
        w = (self.max_x + pad) - x0
        h = (self.max_y + pad) - y0
        parts = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="%.0f %.0f %.0f %.0f" '
                 'width="%.0f" height="%.0f">' % (x0, y0, w, h, w, h)]
        parts.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="#f8fafc"/>'
                     % (x0, y0, w, h))
        parts.append('<text x="%.0f" y="%.0f" font-family="%s" font-size="17" '
                     'font-weight="bold" fill="#0f172a">%s</text>'
                     % (x0 + 16, y0 + 36, FONT,
                        self.title.replace("&", "&amp;").replace("<", "&lt;")))
        for e in self.edges:
            parts.append(self.edge_svg(e))
        for lx, ly, lt in self.labels:
            parts.append('<text x="%.1f" y="%.1f" font-family="%s" font-size="12.5" '
                         'fill="#475569">%s</text>'
                         % (lx, ly, FONT, lt.replace("&", "&amp;")))
        for nd in self.nodes:
            parts.append(self.node_svg(nd))
        parts.append("</svg>")
        return "\n".join(parts)


def generate(title, spec, out_path):
    fc = Flowchart(title)
    fc.layout(spec, MAIN_X, 72, 0, prev=None)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(fc.to_svg())
    return out_path


# ---------------------------------------------------------------------------
# Flowchart specifications, one per case study
# ---------------------------------------------------------------------------
SPECS = {
    "01-scholarship-allocation": (
        "Flowchart 1: University Scholarship Allocation",
        [
            ["term", "Start"],
            ["io", "Read all applicant records into a list"],
            ["proc", "Set index i = 0 and create empty eligible and rejected lists"],
            ["while", "i < number of applicants?", [
                ["proc", "Unpack record i: name, aggregate, subject marks, attendance, income"],
                ["dec", "aggregate >= 75 AND every subject mark >= 40?",
                    [
                        ["dec", "attendance >= 70 AND income <= 500000?",
                            [["proc", "Add record to eligible list"]],
                            [["proc", "Reject: low attendance or high income"]],
                        ],
                    ],
                    [
                        ["proc", "Reject: low aggregate or low subject marks"],
                    ],
                ],
                ["proc", "Set i = i + 1"],
            ]],
            ["proc", "Rank eligible students using the tie-break rules"],
            ["io", "Print ranked eligible list and rejected list with reasons"],
            ["term", "End"],
        ]),

    "02-progressive-electricity-billing": (
        "Flowchart 2: Progressive Electricity Billing",
        [
            ["term", "Start"],
            ["io", "Read households: name, load, six monthly readings"],
            ["proc", "Set household index h = 0 and comparison list"],
            ["while", "h < number of households?", [
                ["proc", "Unpack household h: name, load, readings; find fixed charge"],
                ["proc", "Set month index m = 0, totals = 0"],
                ["while", "m < number of readings?", [
                    ["proc", "Unpack reading: month, units, paid flag; compute slab energy"],
                    ["proc", "Add fixed charge, duty 5% and fuel 3% surcharges"],
                    ["dec", "units <= 200?",
                        [["proc", "Add 5% green rebate"]],
                        [["proc", "No green rebate"]],
                    ],
                    ["dec", "paid on time?",
                        [["proc", "Add 2% prompt rebate"]],
                        [["proc", "No prompt rebate"]],
                    ],
                    ["proc", "Bill = subtotal - rebates; store bill; m = m + 1"],
                ]],
                ["proc", "Print monthly table, average, highest and lowest bills"],
                ["proc", "Flag months where units rose more than 20%"],
                ["proc", "Print bill bar-chart pattern and household totals"],
                ["proc", "Append household totals; h = h + 1"],
            ]],
            ["io", "Print cross-household comparison table"],
            ["proc", "Print closing strip pattern"],
            ["term", "End"],
        ]),

    "03-hospital-billing-patient-classification": (
        "Flowchart 3: Hospital Billing and Patient Classification",
        [
            ["term", "Start"],
            ["io", "Read patient records into a list"],
            ["proc", "Set index i = 0, valid = 0, invalid = 0"],
            ["while", "i < number of patients?", [
                ["proc", "Unpack record: id, name, age, consult, days, room, procedure, tests"],
                ["dec", "Age, days and every key are valid?",
                    [
                        ["proc", "Consultation + room x days + procedure + tests = subtotal"],
                        ["dec", "age >= 60?",
                            [
                                ["dec", "age >= 70?",
                                    [["proc", "Set rate = 0.20"]],
                                    [["proc", "Set rate = 0.10"]],
                                ],
                            ],
                            [
                                ["dec", "age <= 12?",
                                    [["proc", "Set rate = 0.15"]],
                                    [["proc", "Set rate = 0.00"]],
                                ],
                            ],
                        ],
                        ["proc", "Payable = subtotal - concession; update counters"],
                        ["proc", "Classify payable into policy band A/B/C/D"],
                    ],
                    [
                        ["proc", "Print every validation error; count invalid"],
                    ],
                ],
                ["proc", "Print bill or errors; i = i + 1"],
            ]],
            ["io", "Print batch summary of valid and invalid counts"],
            ["proc", "Print closing cross-row pattern"],
            ["term", "End"],
        ]),

    "04-employee-payroll-deductions": (
        "Flowchart 4: Employee Payroll and Deduction Analysis",
        [
            ["term", "Start"],
            ["io", "Read employee records: id, name, basic, OT hours, incentive"],
            ["proc", "Set totals of gross, deductions and net to 0"],
            ["while", "i < number of employees?", [
                ["proc", "Gross = basic + HRA 40% + DA 10% + TA + OT + incentive"],
                ["dec", "12% of basic exceeds 1800?",
                    [["proc", "PF = 1800 (cap)"]],
                    [["proc", "PF = 12% of basic"]],
                ],
                ["proc", "Professional tax from gross slab table"],
                ["dec", "taxable = gross - PF - PT greater than 0?",
                    [["proc", "Walk income-tax slabs slice by slice"]],
                    [["proc", "Income tax = 0"]],
                ],
                ["proc", "Net = gross - PF - PT - tax; print salary statement"],
                ["proc", "Add to batch totals; i = i + 1"],
            ]],
            ["io", "Print batch totals and average net"],
            ["proc", "Print closing diamond pattern"],
            ["term", "End"],
        ]),

    "05-telecom-plan-optimization": (
        "Flowchart 5: Multi-Plan Telecommunications Cost Optimization",
        [
            ["term", "Start"],
            ["io", "Read plan table and usage profiles"],
            ["proc", "Set usage index u = 0"],
            ["while", "u < number of usages?", [
                ["proc", "Unpack usage: data, minutes, SMS, days, budget"],
                ["proc", "Set plan index p = 0 and best plan = none"],
                ["while", "p < number of plans?", [
                    ["proc", "Packs = ceil(days / validity); base = packs x price"],
                    ["proc", "Excess data + minutes + SMS = shortfall x rates"],
                    ["proc", "Total = base + excess charges"],
                    ["dec", "total <= budget?",
                        [["proc", "Mark eligible; keep it if cheaper than best"]],
                        [["proc", "Mark not eligible"]],
                    ],
                    ["proc", "p = p + 1"],
                ]],
                ["dec", "A best plan was found?",
                    [["proc", "Print most economical plan and breakdown"]],
                    [["proc", "Print no-plan message and shortfall"]],
                ],
                ["proc", "Print comparison table and cost bars; u = u + 1"],
            ]],
            ["proc", "Print closing signal-bar pattern"],
            ["term", "End"],
        ]),

    "06-railway-fare-reservation": (
        "Flowchart 6: Railway Fare and Reservation Calculator",
        [
            ["term", "Start"],
            ["io", "Read passengers: name, age, distance, class, status, hours"],
            ["proc", "Set collections = 0, refunds = 0, counters = 0"],
            ["while", "i < number of passengers?", [
                ["proc", "Unpack record; find class label, multiplier and fee"],
                ["proc", "Base fare = distance x rate of first matching slab"],
                ["proc", "Class fare = base x multiplier"],
                ["dec", "age < 5?",
                    [
                        ["proc", "Concession = 100% and reservation fee = 0"],
                    ],
                    [
                        ["dec", "age <= 11 or age >= 60?",
                            [["proc", "Concession = 50% child or 40% senior"]],
                            [["proc", "No age concession"]],
                        ],
                    ],
                ],
                ["proc", "Ticket value = fare - concession + reservation fee"],
                ["dec", "status = CANCELLED?",
                    [
                        ["dec", "hours before departure >= 24?",
                            [["proc", "Penalty = 10% of ticket value"]],
                            [
                                ["dec", "hours >= 12?",
                                    [["proc", "Penalty = 30%"]],
                                    [["proc", "Penalty = 100%"]],
                                ],
                            ],
                        ],
                        ["proc", "Refund = ticket - penalty; add to refunds"],
                    ],
                    [
                        ["proc", "Add ticket value to collections"],
                    ],
                ],
                ["proc", "Print passenger details; i = i + 1"],
            ]],
            ["io", "Print revenue summary: collections, refunds, net"],
            ["proc", "Print rail-track pattern"],
            ["term", "End"],
        ]),

    "07-retail-billing-discounts": (
        "Flowchart 7: Retail Billing with Multiple Discount Rules",
        [
            ["term", "Start"],
            ["io", "Read product catalogue, tax rates, discount rules, cart"],
            ["proc", "Set invoice counter = 0"],
            ["while", "invoice < number of carts?", [
                ["proc", "Set lines = empty, subtotal = 0, invalid = 0"],
                ["while", "item index < number of cart lines?", [
                    ["proc", "Unpack line: product name, quantity"],
                    ["dec", "Product found AND quantity > 0?",
                        [["proc", "amount = price x qty; subtotal = subtotal + amount"]],
                        [["proc", "Print line error; invalid = invalid + 1"]],
                    ],
                    ["proc", "item index = item index + 1"],
                ]],
                ["dec", "subtotal > 0?",
                    [
                        ["proc", "Threshold discount on subtotal, capped at maximum"],
                        ["proc", "Share discount per line; tax per category"],
                        ["proc", "Print invoice: lines, discount, taxes, grand total"],
                    ],
                    [
                        ["proc", "Print no-billable-items message"],
                    ],
                ],
                ["proc", "invoice = invoice + 1"],
            ]],
            ["proc", "Print barcode pattern"],
            ["term", "End"],
        ]),
    "08-manufacturing-profitability": (
        "Flowchart 8: Manufacturing Cost and Profitability Analysis",
        [
            ["term", "Start"],
            ["io", "Read product records with BOM lists"],
            ["proc", "Set counters"],
            ["while", "p < number of products?", [
                ["proc", "Unpack product; walk BOM nested list = material cost"],
                ["proc", "unit = material + labour + machine; wastage on top"],
                ["proc", "batch cost = unit x planned; revenue = price x sold"],
                ["proc", "profit = revenue - batch cost"],
                ["dec", "profit >= target?",
                 [["proc", "Count met; print TARGET MET"]],
                 [["proc", "Count not met; print shortfall"]]],
                ["proc", "Print cost sheet; p = p + 1"],
            ]],
            ["io", "Print batch profitability summary"],
            ["proc", "Print production-line pattern"],
            ["term", "End"],
        ]),
    "09-multicurrency-travel-budget": (
        "Flowchart 9: Multi-Currency Travel Budget Analysis",
        [
            ["term", "Start"],
            ["io", "Read exchange rates, itineraries, budgets"],
            ["proc", "Print rate table"],
            ["while", "t < number of test cases?", [
                ["proc", "Unpack budget, legs; remaining = budget"],
                ["while", "i < number of legs?", [
                    ["proc", "Find rate; sum local prices for leg"],
                    ["proc", "local -> INR; fee 2%; country cost"],
                    ["dec", "cost <= remaining?",
                     [["proc", "remaining -= cost; covered += 1; print COVERED"]],
                     [["proc", "Print shortfalls; print SKIPPED"]]],
                    ["proc", "i = i + 1"],
                ]],
                ["proc", "Print trip summary; t = t + 1"],
            ]],
            ["proc", "Print diamond pattern"],
            ["term", "End"],
        ]),
    "10-campus-event-financial-planning": (
        "Flowchart 10: Campus Event Financial Planning",
        [
            ["term", "Start"],
            ["io", "Read sponsors, stalls, fixed costs, scenarios"],
            ["proc", "Print event cost sheet"],
            ["while", "s < number of scenarios?", [
                ["proc", "Unpack scenario; income = tickets + sponsors + stalls"],
                ["proc", "expenses = fixed + buses + catering + kits"],
                ["proc", "contingency 5%; total expenses; profit"],
                ["dec", "profit >= 0?",
                 [["proc", "Count profitable; print PROFIT"]],
                 [["proc", "Count losses; print LOSS"]]],
                ["proc", "Scan paid = 0..2000 for break-even"],
                ["proc", "Print scenario result; s = s + 1"],
            ]],
            ["io", "Print event summary"],
            ["proc", "Print stage-light pattern"],
            ["term", "End"],
        ]),
}


if __name__ == "__main__":
    import os
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for folder, (title, spec) in sorted(SPECS.items()):
        out_dir = os.path.join(root, folder)
        os.makedirs(out_dir, exist_ok=True)
        path = os.path.join(out_dir, "flowchart.svg")
        generate(title, spec, path)
        print("wrote", path)
