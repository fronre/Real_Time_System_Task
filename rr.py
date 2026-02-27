import threading
import time
import os
import subprocess
import psutil
from datetime import datetime

quantum = 2
total_runtime = 30
running = True
monitor_process = None

# احصائيات
sound_cycles = 0
cpu_cycles = 0
cpu_samples = []

# ---------------- SOUND TASK ----------------
def sound_task():
    global running, sound_cycles
    while running:
        os.system("paplay /usr/share/sounds/freedesktop/stereo/complete.oga 2>/dev/null")
        sound_cycles += 1
        time.sleep(quantum)

# ---------------- MONITOR TASK ----------------
def monitor_task():
    global monitor_process, running, cpu_samples
    monitor_process = subprocess.Popen(["gnome-system-monitor"])

    while running:
        cpu = psutil.cpu_percent(interval=1)
        cpu_samples.append(cpu)

# ---------------- CPU TASK ----------------
def cpu_task():
    global running, cpu_cycles
    number = 1
    while running:
        slice_start = time.time()
        while time.time() - slice_start < quantum and running:
            number += 1
            _ = all(number % i != 0 for i in range(2, int(number**0.5) + 1))
        cpu_cycles += 1

# ---------------- MAIN ----------------
def main():
    global running, monitor_process

    print(f"\nSystem Running for {total_runtime} seconds...\n")

    t1 = threading.Thread(target=sound_task)
    t2 = threading.Thread(target=monitor_task)
    t3 = threading.Thread(target=cpu_task)

    t1.start()
    t2.start()
    t3.start()

    time.sleep(total_runtime)
    running = False

    t1.join()
    t2.join()
    t3.join()

    if monitor_process:
        monitor_process.kill()

    # ----------- حساب النتائج -----------
    avg_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

    results = f"""
========= REAL-TIME SYSTEM RESULTS =========
Execution Date: {datetime.now()}
Total Runtime: {total_runtime} seconds
Quantum: {quantum} seconds

Sound Cycles: {sound_cycles}
CPU Cycles: {cpu_cycles}
CPU Samples Taken: {len(cpu_samples)}
Average CPU Usage: {avg_cpu:.2f}%

System Stopped Successfully
============================================
"""

    # حفظ في ملف
    with open("results.txt", "a") as file:
        file.write(results)

    print("Results saved to results.txt ✅")

if __name__ == "__main__":
    main()