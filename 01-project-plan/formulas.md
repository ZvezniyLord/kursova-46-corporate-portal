# EVM formulas — educational simulation (01-project-plan)
# All monetary values are USD (hypothetical). Status date 2026-11-06 (working day 45 of 80).
# PV : Planned Value  = Σ budget_i x planned_fraction_i  (work scheduled by status date)
# EV : Earned Value   = Σ budget_i x actual_fraction_i   (work physically performed)
# AC : Actual Cost    = Σ actual cost incurred to date
# SV = EV - PV        (negative = behind schedule)
# CV = EV - AC        (negative = over budget)
# SPI = EV / PV       (1.0 = on plan; <1 behind)
# CPI = EV / AC       (1.0 = on budget; <1 over)
# BAC = Σ task budget (32,264 USD, no contingency reserve)
# EAC = BAC / CPI     (estimate at completion)
# ETC = EAC - AC
# VAC = BAC - EAC
# Denominator check: tasks with PV==0 get SPI blank; AC==0 gives CPI blank.
# Reproduce: python build/build_dataset.py
