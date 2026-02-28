import threading
import time
import psutil
from datetime import datetime

quantum = 2
max_cycles = 20

sound_cycles = 0
cpu_cycles = 0
monitor_cycles = 0
cpu_samples = []

# ---------------- SOUND TASK ----------------
def sound_task():
    global sound_cycles
    while sound_cycles < max_cycles:
        print("🔊 Sound Task Running")
        sound_cycles += 1
        time.sleep(quantum)

# ---------------- MONITOR TASK ----------------
def monitor_task():
    global monitor_cycles, cpu_samples

    while monitor_cycles < max_cycles:
        cpu = psutil.cpu_percent(interval=1)
        cpu_samples.append(cpu)
        print(f"📊 CPU Usage: {cpu}%")
        monitor_cycles += 1

# ---------------- CPU TASK ----------------
def cpu_task():
    global cpu_cycles
    number = 1

    while cpu_cycles < max_cycles:
        slice_start = time.time()
        while time.time() - slice_start < quantum:
            number += 1
            _ = all(number % i != 0 for i in range(2, int(number**0.5) + 1))
        cpu_cycles += 1
        print("⚙ CPU Task Cycle Done")

# ---------------- MAIN ----------------
def main():

    print(f"\nSystem Running for {max_cycles} cycles per task...\n")

    t1 = threading.Thread(target=sound_task)
    t2 = threading.Thread(target=monitor_task)
    t3 = threading.Thread(target=cpu_task)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    avg_cpu = sum(cpu_samples) / len(cpu_samples) if cpu_samples else 0

    print("\n========= RESULTS =========")
    print(f"Sound Cycles: {sound_cycles}")
    print(f"Monitor Cycles: {monitor_cycles}")
    print(f"CPU Cycles: {cpu_cycles}")
    print(f"Average CPU Usage: {avg_cpu:.2f}%")
    print("System Stopped Successfully ✅")


if __name__ == "__main__":
    main()