"""Survey document/. Write to ROOT where I know it works."""
import os
ROOT = r"C:\Users\khoilm\Downloads\project\AeroCast-VAA-System\document"
OUT  = r"C:\Users\khoilm\Downloads\project\AeroCast-VAA-System\survey_root.txt"
try:
    out = []
    n_dir = 0
    n_file = 0
    for dp, dns, fns in os.walk(ROOT):
        n_dir += 1
        rel = os.path.relpath(dp, ROOT)
        if rel == ".":
            out.append("[document/]")
        else:
            out.append("  " * (rel.count(os.sep) + 1) + "[" + rel + "]")
        for d in sorted(dns):
            out.append("  " * (rel.count(os.sep) + 2) + "/" + d + "/")
        for f in sorted(fns):
            n_file += 1
            try:
                sz = os.path.getsize(os.path.join(dp, f))
            except OSError:
                sz = -1
            out.append("  " * (rel.count(os.sep) + 2) + "- " + f + "  (" + str(sz) + " B)")
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(out))
    with open(OUT + ".ok", "w", encoding="utf-8") as fh:
        fh.write("dirs=" + str(n_dir) + " files=" + str(n_file))
except Exception as e:
    with open(OUT + ".err", "w", encoding="utf-8") as fh:
        fh.write(repr(e))
