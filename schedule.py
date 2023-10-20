import re
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


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
    def __init__(self, schedule, todo_filename):
        self.schedule = schedule
        self.todo_filename = todo_filename
        self.root = tk.Tk()
        self.root.title("Produkt - Time Blocking")

        # Window size
        self.root.geometry("850x600")

        self.root.configure(bg='#2E2E2E')

        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        file = tk.Menu(menu)
        menu.add_cascade(label="File", menu=file)
        file.add_command(label="Exit", command=self.root.destroy)

        # Schedule Section
        schedule_frame = tk.LabelFrame(self.root, text="Schedule", bg='#2E2E2E', fg='#FFFFFF', font=('Helvetica', 12))
        schedule_frame.pack(fill="both", expand="yes", padx=20, pady=10)

        self.current_task_label = tk.Label(schedule_frame, font=('Helvetica', 12), fg='#FFFFFF', bg='#2E2E2E')
        self.current_task_label.pack(pady=5)

        self.next_task_label = tk.Label(schedule_frame, font=('Helvetica', 12), fg='#FFFFFF', bg='#2E2E2E')
        self.next_task_label.pack(pady=5)

        # ToDo Section
        todo_frame = tk.LabelFrame(self.root, text="To-Do List", bg='#2E2E2E', fg='#FFFFFF', font=('Helvetica', 12))
        todo_frame.pack(fill="both", expand="yes", padx=20, pady=10)

        self.todo_list = tk.Listbox(todo_frame, bg='#333333', fg='#FFFFFF', font=('Helvetica', 12))
        self.todo_list.pack(fill="both", expand=True, padx=10, pady=5)

        self.load_todo_list()

        edit_button = tk.Button(todo_frame, text="Edit", command=self.edit_todo, bg='#555555', fg='#FFFFFF', font=('Helvetica', 12))
        edit_button.pack(padx=10, pady=5)

        self.update_schedule()
        self.check_for_updates()

    def load_todo_list(self):
        if not os.path.exists(self.todo_filename):
            with open(self.todo_filename, 'w') as file:
                file.write("")

        with open(self.todo_filename, 'r') as file:
            lines = file.readlines()

        self.todo_list.delete(0, tk.END)
        for line in lines:
            self.todo_list.insert(tk.END, line.strip())

    def edit_todo(self):
        selected = self.todo_list.curselection()
        if selected:
            index = selected[0]
            item = self.todo_list.get(index)

            def save_edit():
                new_item = edit_var.get()
                self.todo_list.delete(index)
                self.todo_list.insert(index, new_item)
                edit_win.destroy()
                with open(self.todo_filename, 'w') as file:
                    file.writelines([item + '\n' for item in self.todo_list.get(0, tk.END)])

            edit_win = tk.Toplevel()
            edit_win.title("Edit Item")
            edit_label = tk.Label(edit_win, text="Edit Item:")
            edit_label.pack(padx=10, pady=5)
            edit_var = tk.StringVar()
            edit_var.set(item)
            edit_entry = tk.Entry(edit_win, textvariable=edit_var)
            edit_entry.pack(padx=10, pady=5)
            save_button = tk.Button(edit_win, text="Save", command=save_edit)
            save_button.pack(padx=10, pady=5)

            
    def update_schedule(self):
        task, next_task = self.schedule.get_current_and_next_task()
        current_time = datetime.now().strftime("%H:%M")
        
        self.current_task_label['text'] = f"[NOW]: [{task[0]}] {task[1]}"
        self.next_task_label['text'] = f"[NEXT]: [{next_task[0]}] {next_task[1]}"
        
        self.root.after(60000, self.update_schedule)  # Update every 60 seconds

    def check_for_updates(self):
        self.schedule.check_for_updates()
        self.root.after(10000, self.check_for_updates)  # Check for updates every 10 seconds

    def run(self):
        self.root.mainloop()

def main():
    schedule = Schedule("schedule.txt")
    app = ScheduleApp(schedule, "todo.txt")
    app.run()

if __name__ == "__main__":
    main()