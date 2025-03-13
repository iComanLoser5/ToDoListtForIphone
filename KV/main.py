import csv
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty
from kivy.core.window import Window

# Set the background color to black (RGBA)
Window.clearcolor = (0, 0, 0, 1)

class ToDoWidget(BoxLayout):
    # ListProperty to hold tasks; each task is a list: [Task, Due, Diff, Priority]
    tasks = ListProperty([])

    def load_tasks(self):
        """Load tasks from 'ToDo.csv'. Each row must have 4 columns."""
        self.tasks = []
        try:
            with open("ToDo.csv", "r", newline="") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 4:
                        self.tasks.append(row[:4])
        except FileNotFoundError:
            pass
        self.update_list()

    def save_tasks(self):
        """Save the current tasks to 'ToDo.csv'."""
        with open("ToDo.csv", "w", newline="") as f:
            writer = csv.writer(f)
            for task in self.tasks:
                writer.writerow(task)

    def update_list(self):
        """Update the RecycleView’s data so that tasks are displayed."""
        # Format each task as a string: "Task | Due: X | Diff: Y | Prio: Z"
        self.ids.task_rv.data = [{
            'text': f"{t[0]} | Due: {t[1]} | Diff: {t[2]} | Prio: {t[3]}",
            'font_size': 18,
            'color': (1, 1, 1, 1),
            'size_hint_y': None,
            'height': 30
        } for t in self.tasks]

    def add_task(self):
        """Read input fields, compute priority, add a task, update and save."""
        task = self.ids.task_input.text.strip()
        due = self.ids.due_input.text.strip()
        diff = self.ids.diff_input.text.strip()
        if not task or not due.isdigit() or not diff.isdigit():
            return  # You might add error feedback here
        due_val = int(due)
        diff_val = int(diff)
        if diff_val < 1 or diff_val > 5:
            return
        prio = diff_val / due_val if due_val != 0 else diff_val
        # Save priority rounded to 2 decimals
        self.tasks.append([task, due, diff, f"{prio:.2f}"])
        self.update_list()
        self.save_tasks()
        self.ids.task_input.text = ""
        self.ids.due_input.text = ""
        self.ids.diff_input.text = ""

    def remove_task(self):
        """Remove the last task from the list."""
        if self.tasks:
            self.tasks.pop()
            self.update_list()
            self.save_tasks()

    def sort_tasks(self):
        """Sort tasks by priority (descending)."""
        try:
            self.tasks.sort(key=lambda t: float(t[3]), reverse=True)
        except Exception as e:
            print("Sorting error:", e)
        self.update_list()
        self.save_tasks()

class ToDoApp(App):
    def build(self):
        root = ToDoWidget()
        root.load_tasks()
        return root

if __name__ == "__main__":
    ToDoApp().run()
