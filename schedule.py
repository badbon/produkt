import re
import time
import os
from datetime import datetime

class Schedule:
    def __init__(self, filename):
        self.filename = filename
        self.schedule = self.load_schedule()
        self.last_modified = os.path.getmtime(self.filename)

    def load_schedule(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as file:
                file.write("")
                
        with open(self.filename, "r") as file:
            lines = file.readlines()
            tasks = [line.strip() for line in lines if re.match(r'^\d{2}:\d{2}', line.strip())]
            schedule = []
            for task in tasks:
                start_time, task_detail = task.split(' - ', 1)
                schedule.append((start_time.strip(), task_detail.strip()))
            return schedule

    def get_current_and_next_task(self):
        current_time = datetime.now().time()
        current_task = ("00:00", "No task scheduled")
        next_task = ("00:00", "No upcoming task")
        for i, (start_time, task_detail) in enumerate(self.schedule):
            task_time = datetime.strptime(start_time, "%H:%M").time()
            if task_time <= current_time:
                current_task = (start_time, task_detail)
                if i < len(self.schedule) - 1:
                    next_task = self.schedule[i + 1]
            else:
                break

        return current_task, next_task

    def check_for_updates(self):
        modified_time = os.path.getmtime(self.filename)
        if modified_time > self.last_modified:
            print(f"[{datetime.now().strftime('%H:%M')}] [UPDATE] Schedule updated, reloading...")
            self.schedule = self.load_schedule()
            self.last_modified = modified_time

def main():
    schedule = Schedule("schedule.txt")
    current_task = ("", "")
    while True:
        schedule.check_for_updates()
        task, next_task = schedule.get_current_and_next_task()
        if current_task != task:
            current_time = datetime.now().strftime("%H:%M")
            if current_task[1]:
                print(f"[{current_time}] [END]   : {current_task[1]}")
            print(f"[{current_time}] [START] : [{task[0]}] {task[1]}")
            print(f"[{current_time}] [NEXT]  : [{next_task[0]}] {next_task[1]}")
            current_task = task
        time.sleep(60)

if __name__ == "__main__":
    main()
