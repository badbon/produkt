import re
import os
from datetime import datetime
import tkinter as tk


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

class ScheduleApp:
    def __init__(self, schedule):
        self.schedule = schedule
        self.root = tk.Tk()
        self.root.title("Produkt - Time Blocking")

        # Window size
        self.root.geometry("650x180")

        self.root.configure(bg='#2E2E2E')
        
        self.current_task_label = tk.Label(self.root, font=('Helvetica', 12), fg='#FFFFFF', bg='#2E2E2E')
        self.current_task_label.pack(pady=5)

        self.next_task_label = tk.Label(self.root, font=('Helvetica', 12), fg='#FFFFFF', bg='#2E2E2E')
        self.next_task_label.pack(pady=5)

        self.update_schedule()
        self.check_for_updates()

    def update_schedule(self):
        task, next_task = self.schedule.get_current_and_next_task()
        current_time = datetime.now().strftime("%H:%M")
        
        self.current_task_label['text'] = f"[{current_time}] [NOW]: [{task[0]}] {task[1]}"
        self.next_task_label['text'] = f"[{current_time}] [NEXT]: [{next_task[0]}] {next_task[1]}"
        
        self.root.after(60000, self.update_schedule)  # Update every 60 seconds

    def check_for_updates(self):
        self.schedule.check_for_updates()
        self.root.after(10000, self.check_for_updates)  # Check for updates every 10 seconds

    def run(self):
        self.root.mainloop()

def main():
    schedule = Schedule("schedule.txt")
    app = ScheduleApp(schedule)
    app.run()

if __name__ == "__main__":
    main()