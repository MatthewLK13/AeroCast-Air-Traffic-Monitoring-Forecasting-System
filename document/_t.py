import sys
print("hello", flush=True)
with open(r"C:\Users\khoilm\Downloads\project\AeroCast-VAA-System\_ping.txt", "w") as f:
    f.write("ping ok\n" + sys.executable)
