import time
import heapq
import psutil
import pygame
import numpy as np

TOTAL_RUNTIME = 30  # مدة التشغيل بالثواني

# -------- تهيئة الصوت (Stereo) --------
pygame.mixer.init(frequency=44100, size=-16, channels=2)

def play_tone(duration=0.5, freq=440):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)

    t = np.linspace(0, duration, n_samples, False)
    wave = 0.5 * np.sin(2 * np.pi * freq * t)

    audio = np.array(wave * 32767, dtype=np.int16)

    # تحويل إلى Stereo
    stereo_audio = np.column_stack((audio, audio))

    sound = pygame.sndarray.make_sound(stereo_audio)
    sound.play()
    time.sleep(duration)


# -------- تعريف Task --------
class Task:
    def __init__(self, name, period, execution_time):
        self.name = name
        self.period = period
        self.execution_time = execution_time
        self.next_release = 0
        self.deadline = period
        self.instances = 0
        self.missed_deadlines = 0

    def release(self, current_time):
        if current_time >= self.next_release:
            self.deadline = self.next_release + self.period
            self.next_release += self.period
            self.instances += 1
            return True
        return False


# -------- تعريف التاسكات --------
tasks = [
    Task("Sound Task", period=6, execution_time=1),
    Task("Monitor Task", period=8, execution_time=2),
    Task("CPU Task", period=10, execution_time=3),
]

ready_queue = []
start_time = time.time()

print("\nStarting EDF Real-Time Simulation with Real Sound...\n")

# -------- حلقة EDF --------
while time.time() - start_time < TOTAL_RUNTIME:
    current_time = time.time() - start_time

    # Release tasks
    for task in tasks:
        if task.release(current_time):
            heapq.heappush(ready_queue, (task.deadline, task))

    if ready_queue:
        deadline, task = heapq.heappop(ready_queue)

        print(f"[EDF] Running {task.name} | Deadline: {deadline:.2f}s")

        exec_start = time.time()

        while time.time() - exec_start < task.execution_time:

            if task.name == "CPU Task":
                _ = sum(i*i for i in range(20000))

            elif task.name == "Monitor Task":
                psutil.cpu_percent(interval=None)

            elif task.name == "Sound Task":
                play_tone(0.5)

        finish_time = time.time() - start_time
        if finish_time > deadline:
            task.missed_deadlines += 1
            print(f"⚠ Deadline Missed for {task.name}")

    else:
        time.sleep(0.1)


# -------- حساب Utilization --------
utilization = sum(task.execution_time / task.period for task in tasks)

print("\n========= EDF RESULTS =========")
for task in tasks:
    print(f"{task.name}")
    print(f"  Instances Executed: {task.instances}")
    print(f"  Missed Deadlines : {task.missed_deadlines}")
    print("")

print(f"Total Utilization (U) = {utilization:.2f}")

if utilization <= 1:
    print("System is Schedulable under EDF ✅")
else:
    print("System is NOT Schedulable under EDF ❌")

print("Simulation Finished Successfully ✅")

pygame.mixer.quit()