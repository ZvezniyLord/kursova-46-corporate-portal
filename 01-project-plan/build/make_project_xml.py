# -*- coding: utf-8 -*-
"""make_project_xml.py — produces an MS Project XML–compatible schedule export
from the agreed CSV source tables (educational simulation, 01-project-plan/).

Output: <workdir>/../01-project-plan/import_package/project_schedule.xml

Usage:
    python build/make_project_xml.py

The XML is shape-consistent with the Microsoft Project (2010+) XML export
(namespace http://schemas.microsoft.com/project). It is GENERATED for import
into MS Project (File > Open > Import > XML); it is NOT the .mpp itself.
MS Project (licensed) is NOT installed, so the native .mpp stays BLOCKED.
"""

import csv
import os
import xml.sax.saxutils
from datetime import date

WORK_DIR = os.path.dirname(os.path.abspath(__file__))
PLAN = os.path.dirname(WORK_DIR)                       # 01-project-plan
OUT_DIR = os.path.join(WORK_DIR, "..", "import_package")
OUT = os.path.join(OUT_DIR, "project_schedule.xml")

PLAN_CSV = {
    "tasks": os.path.join(PLAN, "tasks.csv"),
    "resources": os.path.join(PLAN, "resources.csv"),
    "evm": os.path.join(PLAN, "evm-snapshot.csv"),
}

TASK_ORDER = [
    "T-01", "T-02", "T-03", "T-04", "T-05", "T-06", "T-07", "T-08",
    "T-09", "T-10", "T-11", "T-12", "T-13", "T-14", "T-15", "T-16",
    "T-17", "T-18", "T-19", "T-20", "T-21", "T-22", "T-23", "T-24",
]

BUILTIN_CALENDAR = "Standard"


def wkd_to_iso(wkd):
    """working day index (1..80) -> ISO date; project starts 2026-09-07 (Mon)."""
    d, cnt = date(2026, 9, 7), 0
    while True:
        if d.weekday() < 5:
            cnt += 1
            if cnt == wkd:
                return d.isoformat() + "T00:00:00Z"
        d += __import__("datetime").timedelta(days=1)


def main():
    tasks = list(csv.DictReader(open(PLAN_CSV["tasks"], encoding="utf-8")))
    resources = list(csv.DictReader(open(PLAN_CSV["resources"], encoding="utf-8")))
    evm = list(csv.DictReader(open(PLAN_CSV["evm"], encoding="utf-8")))
    es = evm[0] if evm else {}

    bac = float(es.get("bac_usd") or 0) or 0.0
    pv = float(es.get("pv_usd") or 0) or 0.0
    ev = float(es.get("ev_usd") or 0) or 0.0
    ac = float(es.get("ac_usd") or 0) or 0.0
    eac = bac / (ev / ac) if ac else bac
    vac = bac - eac
    tcpi = (bac - ev) / (bac - ac) if abs(bac - ac) > 1e-9 else 0.0

    L = []
    a = L.append
    a('<?xml version="1.0" encoding="UTF-8"?>')
    a('<Project xmlns="http://schemas.microsoft.com/project" '
      'Version="15.0.0" '
      'XMLFilename="corporate-portal_project.xml" '
      'PlanVersion="15.0.0" '
      'PlanName="Корпоративний портал підприємства" '
      'PlanDateCreated="2026-09-07T00:00:00Z" '
      'PlanTimeCreated="00:00:00" '
      'PlanDateFinished="2026-12-25T00:00:00Z" '
      'PlanStatus="Current">')
    a('  <ProjectVersion>15.0.0</ProjectVersion>')
    a('  <ProjectGuid>00000000-0000-0000-0000-000000000000</ProjectGuid>')
    a('  <Calendar Name="Standard">')
    a('    <WeeklyCalendar Monday="1" Tuesday="1" Wednesday="1" Thursday="1" Friday="1" '
      'Saturday="0" Sunday="0"/>')
    a('  </Calendar>')
    a('  <SummaryTasks>')
    a('    <SummaryTask ID="0" WBS="0" TASK_NAME="Корпоративний портал підприємства"/>')
    a('  </SummaryTasks>')

    # --- tasks ---
    a('  <Tasks>')
    for tid in TASK_ORDER:
        t = next((r for r in tasks if r["task_id"] == tid), None)
        if not t:
            continue
        duration = int(t.get("duration_workdays") or 1)
        work = int(t.get("work_hours") or duration * 8)
        cost = float(t.get("budget_usd") or 0)
        status = t.get("actual_frac_status", "")
        status_txt = ("Completed" if status in ("1.0", "1", "0.75", "0.6", "0.4", "0.1") else "Not Started")
        a('    <Task ID="{tid}" REV="1" WBS="{wbs}" WKS="{wks}" '
          'TASK_NAME="{name}" DURATION="{dur}" START="{start}" FINISH="{finish}" '
          'PRI="1" PREDECESSORS="{preds}" UNITS="100%" WORK="{work}" COST="{cost}" '
          'STATUS="{status}" MILESTONE="0"/>'.format(
              tid=t["task_id"], wbs=t.get("wbs_leaf", ""), wks="",
              name=xml.sax.saxutils.escape(t["task_name"]),
              dur=duration,
              start=wkd_to_iso(int(t["start_workday"])),
              finish=wkd_to_iso(int(t["finish_workday"])),
              preds=t.get("preds", ""),
              work=work, cost=cost,
              status=status_txt))
    a('  </Tasks>')

    # --- resources ---
    a('  <Resources>')
    for r in resources:
        a('    <Resource ID="{rid}" NAME="{name}" TYPE="Work" '
          'BASE_RATES="{rate}" OVERRIDE_RATES="{rate}"/>'.format(
              rid=r["resource_id"], name=xml.sax.saxutils.escape(r["role"]),
              rate=r["rate_usd"]))
    a('  </Resources>')

    # --- baseline (per-task baseline columns from tasks.csv) ---
    a('  <Baseline>')
    a('    <BaselineSource>source schedule (CSV)</BaselineSource>')
    a('    <Baseline>')
    for tid in TASK_ORDER:
        t = next((r for r in tasks if r["task_id"] == tid), None)
        if not t:
            continue
        a('      <Task ID="{tid}" WBS="{wbs}" BASELINE_START_DATE="{bsd}" '
          'BASELINE_FINISH_DATE="{bfd}" BASELINE_COST="{bc}" '
          'BASELINE_WORK="{bh}"/>'.format(
              tid=t["task_id"], wbs=t.get("wbs_leaf", ""),
              bsd=t.get("baseline_start_date", ""),
              bfd=t.get("baseline_finish_date", ""),
              bc=t.get("baseline_cost_usd", 0) or 0,
              bh=t.get("work_hours", 0) or 0))
    a('    </Baseline>')
    a('  </Baseline>')

    # --- earned value (educational snapshot, 2026-11-06) ---
    a('  <EarnedValueData>')
    a('    <EarnedValueData>')
    a('      <BAC>{bac}</BAC>'.format(bac=bac))
    a('      <EV>{ev}</EV>'.format(ev=ev))
    a('      <PV>{pv}</PV>'.format(pv=pv))
    a('      <AC>{ac}</AC>'.format(ac=ac))
    a('      <VAC>{vac}</VAC>'.format(vac=vac))
    a('      <TCPI>{tcpi}</TCPI>'.format(tcpi=round(tcpi, 4)))
    a('      <EAC>{eac}</EAC>'.format(eac=eac))
    a('      <ETC>{etc}</ETC>'.format(etc=eac - ac))
    a('    </EarnedValueData>')
    a('  </EarnedValueData>')

    a('</Project>')

    os.makedirs(OUT_DIR, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
