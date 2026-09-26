#!/usr/bin/env python3
"""Research-strength gates (added 2026-09-26 after the Hilbert-series v0.1.0 release shipped without citing
Derksen's universal denominators or Makam's strategy, and with a cheaply closable conditional theorem).

Validates RESEARCH_GATES.json at the root of a research archive (zip) or directory:
  contributionMap   every novelty/contribution claim in the paper, one entry per contribution UNIT
                    (statement | proof | method | object | identification), each with the paper location,
                    the searches run (dated), the sources read IN FULL, the closest prior work and a verdict.
                    At least one 'method' entry is required: the technique itself must be searched for.
  sourcesReadInFull every cited source that a load-bearing step or novelty claim depends on must be listed
                    as read in full (not only the theorem cited).
  limitationTriage  every limitation / conditional hypothesis / open direction in the paper, each with the
                    question "which known theorem or cheap computation closes this?", what was searched or
                    tried, an estimated cost, and a decision CLOSED or OPEN. OPEN items with estimated cost
                    <= 2 hours and no paid compute need an explicit reason they were not closed.
  extensionScout    who ran the 'what would make this materially stronger for little cost?' pass, when,
                    what was proposed, and what was done.
Prints a JSON summary; exit 0 only if every check passes. This is a completeness gate, not scientific review."""
import json, sys, zipfile, os, re

UNITS = {"statement", "proof", "method", "object", "identification"}
VERDICTS = {"new-in-bounded-search", "known-cited", "partially-known-cited", "collision"}
DECISIONS = {"CLOSED", "OPEN"}

def load(target):
    if os.path.isdir(target):
        p = os.path.join(target, "RESEARCH_GATES.json")
        return json.load(open(p)) if os.path.exists(p) else None
    with zipfile.ZipFile(target) as z:
        names = [n for n in z.namelist() if n.rstrip("/").split("/")[-1] == "RESEARCH_GATES.json" and n.count("/") <= 1]
        return json.loads(z.read(sorted(names, key=len)[0])) if names else None

def nonempty(x): return isinstance(x, str) and x.strip() != "" or isinstance(x, list) and len(x) > 0

def main(target):
    errs = []
    g = load(target)
    if g is None:
        print(json.dumps({"status": "failed", "errors": ["RESEARCH_GATES.json missing at archive root"]})); return 1
    cm = g.get("contributionMap") or []
    if not cm: errs.append("contributionMap is empty")
    if not any(e.get("unit") == "method" for e in cm): errs.append("contributionMap has no 'method' unit: the technique itself must be searched for")
    for i, e in enumerate(cm):
        for k in ("claim", "unit", "paperLocation", "searches", "closestPriorWork", "verdict"):
            if not nonempty(e.get(k)): errs.append(f"contributionMap[{i}].{k} missing")
        if e.get("unit") not in UNITS: errs.append(f"contributionMap[{i}].unit must be one of {sorted(UNITS)}")
        if e.get("verdict") not in VERDICTS: errs.append(f"contributionMap[{i}].verdict must be one of {sorted(VERDICTS)}")
        for s in e.get("searches") or []:
            if not re.search(r"\d{4}-\d{2}-\d{2}", str(s.get("date", ""))) or not nonempty(s.get("query")):
                errs.append(f"contributionMap[{i}].searches entries need a dated query"); break
    src = g.get("sourcesReadInFull") or []
    if not src: errs.append("sourcesReadInFull is empty")
    for i, s in enumerate(src):
        if not nonempty(s.get("citation")) or not nonempty(s.get("usedFor")): errs.append(f"sourcesReadInFull[{i}] needs citation and usedFor")
    lt = g.get("limitationTriage") or []
    if not lt: errs.append("limitationTriage is empty (list every limitation, conditional hypothesis and open direction)")
    for i, e in enumerate(lt):
        for k in ("limitation", "closingQuestion", "triedOrSearched", "estimatedCost", "decision"):
            if not nonempty(e.get(k)): errs.append(f"limitationTriage[{i}].{k} missing")
        if e.get("decision") not in DECISIONS: errs.append(f"limitationTriage[{i}].decision must be CLOSED or OPEN")
        if e.get("decision") == "OPEN":
            if not nonempty(e.get("reasonOpen")): errs.append(f"limitationTriage[{i}] is OPEN without reasonOpen")
            if e.get("cheap") is True and not nonempty(e.get("whyNotClosedNow")):
                errs.append(f"limitationTriage[{i}] is cheap (<= 2 h, no paid compute) but OPEN without whyNotClosedNow")
    sc = g.get("extensionScout") or {}
    for k in ("by", "date", "proposals", "actions"):
        if not nonempty(sc.get(k)): errs.append(f"extensionScout.{k} missing")
    out = {"boundary": "Completeness of prior-art, limitation-triage and extension-scout records only; not scientific validation.",
           "status": "passed" if not errs else "failed", "contributions": len(cm), "limitations": len(lt),
           "openCheap": sum(1 for e in lt if e.get("decision") == "OPEN" and e.get("cheap") is True), "errors": errs}
    print(json.dumps(out)); return 0 if not errs else 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
