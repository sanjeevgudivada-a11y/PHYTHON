# Python Activity
my name is GUDIVADA GNANI SANJEEV .From section 2 my roll number is N26V01A0100 

Every case study contains the full set of deliverables: **problem
statement · objectives · assumptions · algorithm · flowchart · pseudocode ·
Python source code · test cases · output screenshots · conclusion**.

## Case Studies

| # | Case study | Folder | Script |
|---|------------|--------|--------|
| 1 | University Scholarship Allocation | [`01-scholarship-allocation`](01-scholarship-allocation/) | `scholarship.py` |
| 2 | Progressive Electricity Billing | [`02-progressive-electricity-billing`](02-progressive-electricity-billing/) | `electricity.py` |
| 3 | Hospital Billing and Patient Classification | [`03-hospital-billing-patient-classification`](03-hospital-billing-patient-classification/) | `hospital_billing.py` |
| 4 | Employee Payroll and Deduction Analysis | [`04-employee-payroll-deductions`](04-employee-payroll-deductions/) | `payroll.py` |
| 5 | Multi-Plan Telecommunications Cost Optimization | [`05-telecom-plan-optimization`](05-telecom-plan-optimization/) | `telecom_plans.py` |
| 6 | Railway Fare and Reservation Calculator | [`06-railway-fare-reservation`](06-railway-fare-reservation/) | `railway_fare.py` |
| 7 | Retail Billing with Multiple Discount Rules | [`07-retail-billing-discounts`](07-retail-billing-discounts/) | `retail_billing.py` |
| 8 | Manufacturing Cost and Profitability Analysis | [`08-manufacturing-profitability`](08-manufacturing-profitability/) | `manufacturing.py` |
| 9 | Multi-Currency Travel Budget Analysis | [`09-multicurrency-travel-budget`](09-multicurrency-travel-budget/) | `travel_budget.py` |
| 10 | Campus Event Financial Planning | [`10-campus-event-financial-planning`](10-campus-event-financial-planning/) | `event_planning.py` |

Each folder contains:

```
NN-case-name/
├── README.md           # all 10 written deliverables (problem → conclusion)
├── flowchart.svg       # generated flowchart
├── <script>.py         # the Python solution
└── outputs/
    ├── run_output.txt  # full console transcript
    └── screenshot_*.png # output screenshots (test cases 1–3)
```

## Running a Case Study

```bash
python3 01-scholarship-allocation/scholarship.py
```

Scripts are plain top-to-bottom programs — no imports, no functions, no
dictionaries, no comprehensions. Test data lives in lists and tuples and
is processed with loops, conditionals and unpacking only; every script
also prints at least one `*`/symbol pattern (pattern generation).

## Repository Tools

- `tools/generate_flowcharts.py` — regenerates every `flowchart.svg`
  from declarative specs (node kinds: `term`, `io`, `proc`, `dec`,
  `while`).
- `tools/check_flowcharts.py` — geometry QA: fails if any flow line
  pierces a node box or crosses another line inside a box. All ten
  flowcharts pass.
- `tools/build_outputs.py` — runs each case, saves `outputs/run_output.txt`
  and renders the PNG screenshots.
