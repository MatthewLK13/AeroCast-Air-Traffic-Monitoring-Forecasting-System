"""Survey document folder. Uses absolute paths so CWD doesn't matter."""
import os
ROOT = r"C:\Users\khoilm\Downloads\project\AeroCast-VAA-System\document"
OUT  = r"C:\Users\khoilm\Downloads\project\AeroCast-VAA-System\document\_survey.txt"
out = []
for dp, dns, fns in os.walk(ROOT):
    rel = os.path.relpath(dp, ROOT)
    if rel == ".":
        out.append("[document/]")
    else:
        out.append("  " * (rel.count(os.sep) + 1) + f"[{rel}]")
    for d in sorted(dns):
        out.append("  " * (rel.count(os.sep) + 2) + f"/{d}/")
    for f in sorted(fns):
        try:
            sz = os.path.getsize(os.path.join(dp, f))
        except OSError:
            sz = -1
        out.append("  " * (rel.count(os.sep) + 2) + f"- {f}  ({sz:,} B)")
with open(OUT, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out))
