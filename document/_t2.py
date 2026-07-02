import time, os
fp = r"C:\Users\khoilm\Downloads\project\AeroCast-VAA-System\document\_ping.txt"
for i in range(20):
    time.sleep(0.5)
    with open(fp, "w") as f:
        f.write("tick " + str(i) + "\ncwd=" + os.getcwd() + "\n")
