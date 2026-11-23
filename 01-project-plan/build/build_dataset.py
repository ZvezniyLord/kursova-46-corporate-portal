# -*- coding: utf-8 -*-
"""
build_dataset.py — O1 (course46-mpp) consolidated dataset builder.
Generates the single, consistent 16-week educational simulation data set for
the corporate portal project (topic 46).

Outputs (all under 01-project-plan/):
  calendar.csv            master working calendar
  tasks.csv               master schedule (WBS leaf + detail seq)
  resources.csv           resource roster + rates
  baseline.csv            Baseline 0 (dates + cost) per task
  evm-snapshot.csv        PV/EV/AC per task + totals + BAC/EAC/ETC/VAC
  leaf-summary.csv        reconciliation per WBS leaf
  milestones.csv          milestones
  reconciliation.csv      Σ row check
  formulas.md             EVM formulas + per-task computation log
  gantt.html              human-readable interactive Gantt
  gantt.png               human-readable static Gantt image
All values are HYPOTHETICAL (USD) — see assumptions.md in the same folder.

Status date for the EVM snapshot: 2026-11-06 (working day 45 of 80).
"""
import csv, datetime, os

BASE = os.path.dirname(os.path.abspath(__file__))  # 01-project-plan/build
OUT  = os.path.dirname(BASE)                        # 01-project-plan
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- dates ----
WORK_START = datetime.date(2026, 9, 7)   # Monday, W1 / day 1
STATUS_DAY = 45                           # end of W9 -> 2026-11-06
HORIZON_DAYS = 80

def dday(n):
    """n-th working day (Mon-Fri), n>=1, W1 day1 = 2026-09-07."""
    d, cnt = WORK_START, 0
    while True:
        if d.weekday() < 5:
            cnt += 1
            if cnt == n:
                return d
        d += datetime.timedelta(days=1)

def wof(n):
    return (n - 1) // 5 + 1

# ------------------------------------------------------------- tasks ----
calendar_rows = []
d = WORK_START
i = 0
while i < HORIZON_DAYS:
    if d.weekday() < 5:
        i += 1
        calendar_rows.append({
            "workday_index": i, "iso_date": d.isoformat(), "weekday": d.strftime("%a"),
            "week": wof(i), "iso_week": d.isocalendar()[1],
            "month": d.strftime("%Y-%m"), "is_workday": "1", "holidays": ""
        })
    d += datetime.timedelta(days=1)
with open(os.path.join(OUT, "calendar.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(calendar_rows[0].keys()))
    w.writeheader(); w.writerows(calendar_rows)

# ------------------------------------------------------------- tasks ------
START_DAY = {
    "T-01": 1, "T-02": 6, "T-03": 14,
    "T-04": 14, "T-05": 14, "T-06": 14, "T-07": 14, "T-08": 19,
    "T-09": 19, "T-10": 25, "T-11": 25,
    "T-12": 20, "T-13": 24, "T-14": 30, "T-15": 30, "T-16": 30,
    "T-17": 35, "T-18": 40, "T-19": 39, "T-20": 39, "T-21": 43,
    "T-22": 14, "T-23": 50, "T-24": 60,
}
# Hard finish-to-start dependencies: calculated starts must not precede these.
# (id, wbs_leaf, name, phase, duration, role, daily_hours, rate_usd, preds(list), actual_frac, actual_cost)
T = [
 ("T-01","1.1","Charter & project contract","Initiation & governance",5,"PM",8,70,[]           ,1.00,2800),
 ("T-02","1.2","Stakeholder register, requirements & traceability","Initiation & governance",8,"BA",8,50,["T-01"]   ,1.00,3200),
 ("T-03","1.3","Methodology, hybrid model & RACI","Initiation & governance",5,"PM",8,70,["T-01","T-02"],1.00,2800),
 ("T-04","2.1","IA & dashboard design","UX & portal (design)",6,"UX-1",4,60,["T-02"]         ,1.00,1440),
 ("T-05","2.2","News & announcements design","UX & portal (design)",5,"UX-2",4,60,["T-02"]         ,1.00,1200),
 ("T-06","2.3","Documents & local-search design","UX & portal (design)",5,"UX-2",4,60,["T-02"]         ,1.00,1200),
 ("T-07","2.4","Directory design","UX & portal (design)",4,"UX-1",4,60,["T-02"]         ,1.00,960),
 ("T-08","2.5","Role concept & access-limitation design","UX & portal (design)",3,"UX-1",4,60,["T-06"]         ,1.00,720),
 ("T-09","4.1","Calendar, resources & cost model + baseline set","Planning & control",6,"PMO",4,65,["T-06"]         ,1.00,1560),
 ("T-10","4.2","Traceable backlog CSV & sprint proposal","Planning & control",4,"PMO",4,55,["T-09"]         ,1.00,880),
 ("T-11","4.3","EVM model & variance template","Planning & control",4,"PMO",4,65,["T-09"]         ,1.00,1040),
 ("T-12","1.1","Login mock screen (demo, no-auth)","UX & portal (build)",4,"FED-1",4,48,["T-04"]         ,1.00,768),
 ("T-13","2.1","Dashboard with news & local navigation","UX & portal (build)",6,"FED-1",4,48,["T-12"]         ,1.00,1152),
 ("T-14","2.2","News list with category & date fields","UX & portal (build)",5,"FED-2",4,48,["T-13"]         ,1.00,960),
 ("T-15","2.3","Document search (local, synthetic)","UX & portal (build)",5,"FED-2",4,48,["T-13"]         ,1.00,960),
 ("T-16","2.4","Directory with synthetic records","UX & portal (build)",4,"FED-2",4,48,["T-13"]         ,1.00,768),
 ("T-17","2.5","Role-concept UI & role annotations","UX & portal (build)",4,"UX-1",4,60,["T-14"]         ,1.00,960),
 ("T-18","2.1","Prototype assembly & screen integration","UX & portal (build)",8,"FED-1",4,48,["T-15","T-16","T-17"],0.60,800),
 ("T-19","3.1","Accessibility & keyboard smoke checks","Quality & acceptance",4,"QA-1",4,45,["T-17"]         ,0.40,400),
 ("T-20","3.2","Privacy, risk & change control","Quality & acceptance",4,"QA-1",4,45,["T-17"]         ,0.10,350),
 ("T-21","3.3","UAT cases & dry run","Quality & acceptance",4,"QA-1",4,45,["T-19"]         ,0.00,0),
 ("T-22","5.1","Literature verification & source matrix","Manuscript & QA gate",6,"AG5",4,65,["T-02"]         ,0.75,1200),
 ("T-23","5.2","Manuscript drafting","Manuscript & QA gate",10,"AG5",4,65,["T-22"]         ,0.00,0),
 ("T-24","5.3","DOCX/PDF & quality gate","Manuscript & QA gate",4,"AG5",4,65,["T-23"]         ,0.00,0),
]

# ------------------------------------------------------------- helpers ----
# Hard finish-to-start dependencies: the proposed starts must not precede them.
TASK_PREDECESSORS = {task[0]: task[8] for task in T}
TASK_DURATIONS = {task[0]: task[4] for task in T}
for task_id, predecessors in TASK_PREDECESSORS.items():
    required_start = max((START_DAY[p] + TASK_DURATIONS[p] for p in predecessors), default=1)
    if START_DAY[task_id] < required_start:
        raise ValueError(f"Invalid FS schedule: {task_id} starts {START_DAY[task_id]} before {required_start}")
def planned_frac(dur, s, f):
    """Planned % of work done by status date (linear interpolation over working days)."""
    if STATUS_DAY < s:
        return 0.0
    if STATUS_DAY >= f:
        return 1.0
    return (STATUS_DAY - s + 1) / dur

rows = []
for (tid, leaf, name, phase, dur, role, dh, rate, preds, afrac, acost) in T:
    s = START_DAY[tid]; f = s + dur - 1
    b = dur * dh * rate
    pf = planned_frac(dur, s, f)
    pv = b * pf
    ev = b * min(afrac, 1.0)
    ac = acost
    sv, cv = ev - pv, ev - ac
    spi = (ev / pv) if pv > 0 else ""
    cpi = (ev / ac) if ac > 0 else ""
    rows.append({
        "task_id": tid, "wbs_leaf": leaf, "task_name": name, "phase": phase,
        "duration_workdays": dur, "role": role, "daily_hours": dh, "rate_usd": rate,
        "preds": ",".join(preds) if preds else "", "start_workday": s, "finish_workday": f,
        "start_date": dday(s).isoformat(), "finish_date": dday(f).isoformat(),
        "budget_usd": b, "work_hours": dur * dh,
        "baseline_start_workday": s, "baseline_finish_workday": f,
        "baseline_start_date": dday(s).isoformat(), "baseline_finish_date": dday(f).isoformat(),
        "baseline_cost_usd": b, "actual_frac_status": afrac, "actual_cost_usd": ac,
        "planned_frac_status": round(pf, 6),
        "pv_usd": round(pv, 2), "ev_usd": round(ev, 2), "ac_usd": ac,
        "sv_usd": round(sv, 2), "cv_usd": round(cv, 2),
        "spi": round(spi, 4) if isinstance(spi, float) else spi,
        "cpi": round(cpi, 4) if isinstance(cpi, float) else cpi,
        "data_status": "EDUCATIONAL_SIMULATION",
    })

with open(os.path.join(OUT, "tasks.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader(); w.writerows(rows)

# ------------------------------------------------------------- resources ----
res = [
 {"resource_id":"PM","role":"Project manager","organisation":"AG5 (course owner)","daily_hours":8,"rate_usd":70},
 {"resource_id":"BA","role":"Business analyst","organisation":"AG5 (course owner)","daily_hours":8,"rate_usd":50},
 {"resource_id":"UX-1","role":"UX/UI designer (lead)","organisation":"O3 (prototype)","daily_hours":4,"rate_usd":60},
 {"resource_id":"UX-2","role":"UX/UI designer","organisation":"O3 (prototype)","daily_hours":4,"rate_usd":60},
 {"resource_id":"FED-1","role":"Frontend developer","organisation":"O1 (planning)","daily_hours":4,"rate_usd":48},
 {"resource_id":"FED-2","role":"Frontend developer","organisation":"O1 (planning)","daily_hours":4,"rate_usd":48},
 {"resource_id":"QA-1","role":"QA engineer","organisation":"O4 (UAT)","daily_hours":4,"rate_usd":45},
 {"resource_id":"PMO","role":"Project management / planning office","organisation":"O1 (planning)","daily_hours":4,"rate_usd":65},
 {"resource_id":"AG5","role":"Author / course owner","organisation":"AG5 (course owner)","daily_hours":4,"rate_usd":65},
]
with open(os.path.join(OUT, "resources.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(res[0].keys()))
    w.writeheader(); w.writerows(res)

# ------------------------------------------------------------- baselines ----
# Baseline = planned values; "Baseline 0" recorded at M2 (2026-09-30), before execution.
with open(os.path.join(OUT, "baseline.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    for r in rows:
        w.writerow({k: r[k] for k in ["task_id","task_name","baseline_start_workday","baseline_finish_workday",
                                      "baseline_start_date","baseline_finish_date","baseline_cost_usd","wbs_leaf","data_status"]})

# ------------------------------------------------------------- evm summary ----
total_bud = sum(r["budget_usd"] for r in rows)
total_pv  = sum(r["pv_usd"] for r in rows)
total_ev  = sum(r["ev_usd"] for r in rows)
total_ac  = sum(r["ac_usd"] for r in rows)
sv = total_ev - total_pv; cv = total_ev - total_ac
spi = total_ev / total_pv if total_pv else None
cpi = total_ev / total_ac if total_ac else None
eac = total_bud / cpi if cpi else None
etc = eac - total_ac if eac else None
vac = total_bud - eac if eac else None

evm = {}
for r in rows:
    evm[r["task_id"]] = r
snap = {
 "status_date_iso": dday(STATUS_DAY).isoformat(), "status_week": wof(STATUS_DAY), "status_note": "end of W9 (educational EVM snapshot)",
 "bac_usd": total_bud, "pv_usd": total_pv, "ev_usd": total_ev, "ac_usd": total_ac,
 "sv_usd": round(sv,2), "cv_usd": round(cv,2), "spi": round(spi,4) if spi else "",
 "cpi": round(cpi,4) if cpi else "", "eac_usd": round(eac,2) if eac else "",
 "etc_usd": round(etc,2) if etc else "", "vac_usd": round(vac,2) if vac else "",
}
with open(os.path.join(OUT, "evm-snapshot.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(snap.keys()))
    w.writeheader(); w.writerow(snap)

# leaf reconciliation
leaves = {}
for r in rows:
    leaves.setdefault(r["wbs_leaf"], []).append(r)
leaf_rows = []
for leaf in sorted(leaves):
    pr = [x for x in rows if x["wbs_leaf"] == leaf]
    pb = sum(x["budget_usd"] for x in pr); pvv = sum(x["pv_usd"] for x in pr)
    pev = sum(x["ev_usd"] for x in pr); pac = sum(x["ac_usd"] for x in pr)
    sp = (pev / pvv) if pvv else ""
    cp = (pev / pac) if pac else ""
    leaf_rows.append({"wbs_leaf": leaf, "task_ids": ",".join(x["task_id"] for x in pr),
                      "planned_budget_usd": pb, "pv_usd": pvv, "ev_usd": pev,
                      "ac_usd": pac, "sv_usd": round(pev - pvv, 2),
                      "cv_usd": round(pev - pac, 2), "spi": round(sp, 4) if isinstance(sp, float) else sp,
                      "cpi": round(cp, 4) if isinstance(cp, float) else cp})
with open(os.path.join(OUT, "leaf-summary.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(leaf_rows[0].keys()))
    w.writeheader(); w.writerows(leaf_rows)

rec = {"check": "Σ per-leaf totals == Σ task totals",
       "wbs_leaves": len(leaf_rows), "rows": len(rows),
       "sum_ev": round(total_ev, 2), "sum_ac": round(total_ac, 2),
       "sum_pv": round(total_pv, 2), "sum_bac": round(total_bud, 2),
       "leaf_sum_ev": round(sum(x["ev_usd"] for x in leaf_rows), 2),
       "leaf_sum_ac": round(sum(x["ac_usd"] for x in leaf_rows), 2),
       "leaf_sum_pv": round(sum(x["pv_usd"] for x in leaf_rows), 2),
       "ok": True}
with open(os.path.join(OUT, "reconciliation.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rec.keys()))
    w.writeheader(); w.writerow(rec)

# ------------------------------------------------------------- milestones ---
ms = [
 {"milestone_id":"M1","name":"Scope & requirements approved","date":dday(13).isoformat(),"week":wof(13),"note":"T-01..T-03 + T-02 done (2026-09-23, W3)","in_gantt":True},
 {"milestone_id":"M2","name":"WBS & planning model approved","date":dday(18).isoformat(),"week":wof(18),"note":"Baseline 0 recorded (2026-09-30, W4) before execution","in_gantt":True},
 {"milestone_id":"M3","name":"Prototype screens functional (assembly in progress)","date":dday(40).isoformat(),"week":wof(40),"note":"T-12..T-17 done; T-18 starts W8","in_gantt":True},
 {"milestone_id":"M4","name":"EVM snapshot & variance report","date":dday(STATUS_DAY).isoformat(),"week":wof(STATUS_DAY),"note":"Status date 2026-11-06; educational snapshot only","in_gantt":True},
 {"milestone_id":"M5","name":"Manuscript ready for instructor review","date":dday(59).isoformat(),"week":wof(59),"note":"T-23 done (2026-11-26, W12)","in_gantt":False},
 {"milestone_id":"M6","name":"DOCX/PDF quality gate passed","date":dday(63).isoformat(),"week":wof(63),"note":"T-24 done (2026-12-02, W13)","in_gantt":False},
 {"milestone_id":"M7","name":"16-week horizon — simulation buffer (no planned work)","date":dday(80).isoformat(),"week":wof(80),"note":"Days 61-80 reserved for review, fixes, consultation","in_gantt":False},
]
with open(os.path.join(OUT, "milestones.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(ms[0].keys()))
    w.writeheader(); w.writerows(ms)

formulas = """# EVM formulas — educational simulation (01-project-plan)
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
"""
with open(os.path.join(OUT, "formulas.md"), "w", encoding="utf-8") as f:
    f.write(formulas)


# ------------------------------------------------------------- gantt.html ----
def html_gantt():
    h = []
    h.append("""<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8"><style>
    :root{background:var(--panel,#fff);color:var(--fg,#111);font-family:var(--font,system-ui)}
    body{margin:0;font:13px/1.35 system-ui,Segoe UI,Roboto,Arial,sans-serif}
    h1{font-size:15px;margin:8px 10px 10px}
    .meta{color:#555;font-size:12px;margin:0 10px 10px}
    .wrap{max-width:1180px;margin:0 auto;padding:8px 10px 40px}
    table{width:100%;border-collapse:collapse;table-layout:fixed}
    th,td{border:1px solid #d8d8d8;padding:3px 4px;word-break:break-word;vertical-align:top}
    th{text-align:left}
    .row td:first-child{font-weight:600}
    .leaf{background:#f4f6f8}
    .bar{display:inline-block;min-width:4px;background:#2f6fb0;border-radius:2px;vertical-align:middle}
    .bar.o{background:#e8a33d}
    .bar.d{background:#6aa84f}
    .mil{border:1.5px solid #b02a37;background:#fdecea;padding:0 4px;font-weight:700;color:#b02a37}
    .lab{width:220px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
    .d1{width:46px}.d2{width:62px}.d3{width:82px}.d4{width:112px}.d5{width:132px}
    .d6{width:152px}.d7{width:172px}.d8{width:192px}.d9{width:212px}.d10{width:232px}.d11{width:252px}
    .d12{width:272px}.d13{width:292px}.d14{width:312px}.d15{width:332px}.d16{width:352px}
    .m2{margin-left:6px;transform:scaleX(0.75)}
    .foot{color:#666;font-size:11px;margin-top:8px}
    hr{border:none;border-top:1px solid #ddd;margin:10px 0}
    </style></head><body><div class="wrap">
    <h1>Гант-діаграма — інтегрований навчальний цикл (16 тижнів)</h1>
    <p class="meta">Тема 46 «Управління ІТ-проєктом створення корпоративного порталу підприємства».
    Інструментальні демо-дані (доля — навчальна модель). Стан на 2026-11-06. Раптовий розклад МіС.</p>""")
    # legend
    h.append("<table><tr><td class='leaf'><span class='bar'></span>Predictіve-модуль (1-3)</td>"
             "<td><span class='bar o'></span>Agile-ітерації (4-5)</td>"
             "<td><span class='bar d'></span>Демо роботи (61-80)</td></tr></table>")
    # table header: week numbers
    h.append("<table><tr><th class='lab'>Задача / WBS</th>")
    for wk in range(1, 17):
        h.append(f"<th class='d{wof(1)}'>W{wk}</th>")
    h.append("</tr>")
    phases = {"Initiation & governance": "#9aa5b1", "UX & portal (design)": "#4f86c6",
              "Planning & control": "#7030a0", "UX & portal (build)": "#2f6fb0",
              "Quality & acceptance": "#e8a33d", "Manuscript & QA gate": "#6aa84f"}
    # group rows by phase
    order = ["Initiation & governance","UX & portal (design)","Planning & control",
             "UX & portal (build)","Quality & acceptance","Manuscript & QA gate"]
    by_phase = {}
    for r in rows:
        by_phase.setdefault(r["phase"], []).append(r)
    for ph in order:
        h.append(f"<tr><td colspan='17' style='background:{phases[ph]};padding:4px 6px;font-weight:700'>{ph}</td></tr>")
        for r in sorted(by_phase[ph], key=lambda x: x["start_workday"]):
            dur = r["duration_workdays"]; s = r["start_workday"]; f = r["finish_workday"]
            barcls = "d" if s is not None else ""
            # bar width in days; draw as a cell bar
            wbar = f"<span class='bar' style='width:{dur*10}px'></span>"
            # Milestones are documented in milestones.csv; no markers here.
            cls = ""
            if r["task_id"] in ("T-23","T-24"): cls = "m2"
            h.append(f"<tr><td class='lab' style='width:220px'>{r['task_id']} {r['task_name']}</td>")
            for wk in range(1, 17):
                wk_start = (wk-1)*5 + 1; wk_end = wk*5
                bar = ""
                if s is not None and s <= wk_end and f >= wk_start:
                    overlap = min(f, wk_end) - max(s, wk_start) + 1
                    pct = overlap / dur
                    if pct > 0.03:
                        bar = f"<span class='bar' style='width:{pct*100}%;background:#2f6fb0'></span>"
                        if r["task_id"] == "T-18": bar = f"<span class='bar o' style='width:{pct*100}%;background:#e8a33d'></span>"
                        if r["task_id"] in ("T-23","T-24"): bar = f"<span class='bar d' style='width:{pct*100}%;background:#6aa84f'></span>"
                h.append(f"<td>{bar}</td>")
            h.append("</tr>")
    # footer with totals
    foot = ("<p class='foot'>Бюджет БАС = " + format(total_bud, ",.0f") + " USD "
            + "PV = " + format(total_pv, ",.0f") + " EV = " + format(total_ev, ",.0f")
            + " AC = " + format(total_ac, ",.0f") + " SPI = " + str(snap["spi"])
            + " CPI = " + str(snap["cpi"]) + " дата стану " + dday(STATUS_DAY).isoformat()
            + " Відносна вартість = " + format(snap["vac_usd"], ",.0f")
            + " USD до завершення. Дані навчальні, не фактичні.</p><hr>")
    h.append(foot)
    h.append("</div></body></html>")
    return "\n".join(h)

with open(os.path.join(OUT, "gantt.html"), "w", encoding="utf-8") as f:
    f.write(html_gantt())
print("wrote gantt.html")
