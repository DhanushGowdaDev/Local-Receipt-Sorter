"""Field-level accuracy on a labeled folder.
Usage: python eval.py ./eval_set   (folder holds receipts + labels.json)
labels.json: {"file1.pdf": {"vendor": "...", "date": "2026-03-04", "currency": "INR",
                            "total": 1180.0, "category": "software"}, ...}
"""
import json
import re
import sys
from pathlib import Path

from extract import extract

FIELDS = ["vendor", "date", "currency", "total", "category"]
norm = lambda s: re.sub(r"[^a-z0-9]", "", str(s or "").lower())

folder = Path(sys.argv[1])
truth = json.loads((folder / "labels.json").read_text())
hits = dict.fromkeys(FIELDS, 0)

for name, want in truth.items():
    got = extract(folder / name).model_dump()
    for f in FIELDS:
        ok = (got[f] is not None and abs(got[f] - want[f]) < 0.01) if f == "total" else norm(got[f]) == norm(want[f])
        hits[f] += ok
        if not ok:
            print(f"{name}: {f} got {got[f]!r}, want {want[f]!r}")

print("\nAccuracy over", len(truth), "documents")
for f in FIELDS:
    print(f"  {f:9s} {hits[f] / len(truth):.0%}")
