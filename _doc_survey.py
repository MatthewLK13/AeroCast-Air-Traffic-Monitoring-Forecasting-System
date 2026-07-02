"""List every file under document/ and write report."""
import os
from pathlib import Path

ROOT = Path(r"C:/Users/khoilm/Downloads/project/AeroCast-VAA-System/document")
OUT  = Path(r"C:/Users/khoilm/Downloads/project/AeroCast-VAA-System/_doc_survey.txt")

lines = []
for dirpath, dirnames, filenames in os.walk(ROOT):
    rel = os.path.relpath(dirpath, ROOT)
    indent = "  " * (rel.count(os.sep) + (0 if rel == "." else 1))
    if rel == ".":
        lines.append(f"[{ROOT}]")
    else:
        lines.append(f"{indent}[{rel}]")
    for d in sorted(dirnames):
        lines.append(f"{indent}  /{d}/")
    for f in sorted(filenames):
        try:
            sz = os.path.getsize(os.path.join(dirpath, f))
            lines.append(f"{indent}  - {f}  ({sz:,} B)")
        except OSError:
            lines.append(f"{indent}  - {f}  (?)")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"wrote {OUT} ({len(lines)} lines)")
