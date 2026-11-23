"""Recalculate the coursework B1 network, role loads and EVM using the standard library."""
import csv
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

root = Path(__file__).resolve().parent
with (root / "tasks.csv").open(encoding="utf-8", newline="") as source:
    tasks = {r["task_id"]: r for r in csv.DictReader(source)}
with (root / "resources.csv").open(encoding="utf-8", newline="") as source:
    roles = {r["role"]: r for r in csv.DictReader(source)}
predecessors = {
    k: set(filter(None, (r["logic_predecessors"] + ";" + r["resource_predecessors"]).split(";")))
    for k, r in tasks.items()
}
early = {}
while len(early) < len(tasks):
    ready = [k for k in tasks if k not in early and predecessors[k] <= early.keys()]
    assert ready, "Cyclic network or missing predecessor"
    for k in ready:
        start = max((early[p][1] for p in predecessors[k]), default=0)
        early[k] = start, start + int(tasks[k]["duration_workdays"])
finish = max(end for _, end in early.values())
late = {}
for k in reversed(early):
    successors = [s for s, pred in predecessors.items() if k in pred]
    end = min((late[s][0] for s in successors), default=finish)
    late[k] = end - int(tasks[k]["duration_workdays"]), end

calendar = []
day = date(2026, 9, 7)
while len(calendar) < finish:
    if day.weekday() < 5:
        calendar.append(day)
    day += timedelta(days=1)
loads = Counter()
totals = Counter()
for k, row in tasks.items():
    es, ef = early[k]
    ls, lf = late[k]
    successors = [s for s, pred in predecessors.items() if k in pred]
    ff = min((early[s][0] for s in successors), default=finish) - ef
    assert [es, ef, ls, lf, ls - es, ff] == [
        int(row[f]) for f in ("es", "ef", "ls", "lf", "total_float", "free_float")
    ]
    assert row["start_date"] == calendar[es].isoformat()
    assert row["finish_date"] == calendar[ef - 1].isoformat()
    role = row["role"]
    hours, rate = int(row["daily_hours"]), int(roles[role]["usd_h"])
    assert rate == int(row["rate_usd"])
    for index in range(es, ef):
        loads[role, index] += hours
    work = hours * (ef - es)
    bac = work * rate
    pv = bac * max(0, min(45 - es, ef - es)) / (ef - es)
    ev = bac * float(row["modeled_fraction"])
    ac = int(row["modeled_work_h"]) * rate
    for key, value in (("planned_hours", work), ("bac_usd", bac), ("pv_usd", pv),
                       ("ev_usd", ev), ("ac_usd", ac)):
        assert abs(float(row[key]) - value) < 1e-7, (k, key)
        totals[key] += value
assert all(hours <= int(roles[role]["daily_capacity_h"]) for (role, _), hours in loads.items())
assert len(tasks) == 28 and finish == 72 and str(calendar[-1]) == "2026-12-15"
assert tuple(totals.values()) == (692, 40308, 31720, 29836, 30437)
pv, ev, ac = (totals[k] for k in ("pv_usd", "ev_usd", "ac_usd"))
print(totals)
print(f"SPI={ev/pv:.4f}, CPI={ev/ac:.4f}, EAC={totals['bac_usd']*ac/ev:.2f}")
