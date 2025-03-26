import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Schedule App")
        self.events = []
        self.finished_events = []

        # Configure grid to split window into 2x2, each taking 1/4
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        # Top-Left: Add Event Frame
        self.add_frame = tk.Frame(root)
        self.add_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.add_frame.grid_columnconfigure(1, weight=1)

        self.label_event = tk.Label(self.add_frame, text="Event Name:")
        self.label_event.grid(row=0, column=0, padx=5, pady=5)
        self.entry_event = tk.Entry(self.add_frame)
        self.entry_event.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        self.label_importance = tk.Label(self.add_frame, text="Importance (-5 to 5):")
        self.label_importance.grid(row=1, column=0, padx=5, pady=5)
        self.importance = ttk.Combobox(self.add_frame, values=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
        self.importance.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.importance.set(0)

        self.label_urgency = tk.Label(self.add_frame, text="Urgency (-5 to 5):")
        self.label_urgency.grid(row=2, column=0, padx=5, pady=5)
        self.urgency = ttk.Combobox(self.add_frame, values=[-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5])
        self.urgency.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
        self.urgency.set(0)

        self.add_button = tk.Button(self.add_frame, text="Add Event", command=self.add_event)
        self.add_button.grid(row=3, column=0, padx=5, pady=5)
        self.plot_button = tk.Button(self.add_frame, text="Generate Plot", command=self.generate_plot)
        self.plot_button.grid(row=3, column=1, padx=5, pady=5)

        # Bottom-Left: Plot Frame
        self.plot_frame = tk.Frame(root)
        self.plot_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.canvas = None  # Placeholder for plot canvas

        # Top-Right: To-Do List Frame
        self.todo_frame = tk.Frame(root)
        self.todo_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        self.todo_label = tk.Label(self.todo_frame, text="To-Do List (Double-click to finish):")
        self.todo_label.pack(pady=5)
        self.todo_listbox = tk.Listbox(self.todo_frame)
        self.todo_listbox.pack(expand=True, fill="both")
        self.todo_listbox.bind("<Double-1>", self.mark_finished)  # Double-click to finish

        # Bottom-Right: Finished Events Frame
        self.finished_frame = tk.Frame(root)
        self.finished_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
        self.finished_label = tk.Label(self.finished_frame, text="Finished Events:")
        self.finished_label.pack(pady=5)
        self.finished_listbox = tk.Listbox(self.finished_frame)
        self.finished_listbox.pack(expand=True, fill="both")

    def add_event(self):
        event_name = self.entry_event.get()
        importance = int(self.importance.get())
        urgency = int(self.urgency.get())

        if event_name:
            self.events.append({"name": event_name, "importance": importance, "urgency": urgency})
            self.update_todo_list()
            self.entry_event.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please enter an event name.")

    def update_todo_list(self):
        self.todo_listbox.delete(0, tk.END)
        sorted_events = sorted(self.events, key=lambda x: (-x["urgency"], -x["importance"]))
        for event in sorted_events:
            self.todo_listbox.insert(tk.END, f"{event['name']} - Urgency: {event['urgency']}, Importance: {event['importance']}")

    def mark_finished(self, event=None):
        selected = self.todo_listbox.curselection()
        if selected:
            index = selected[0]
            finished_event = self.events.pop(index)
            self.finished_events.append(finished_event)
            self.update_todo_list()
            self.finished_listbox.insert(tk.END, f"{finished_event['name']} - Urgency: {finished_event['urgency']}, Importance: {finished_event['importance']}")
            self.generate_plot()
        else:
            messagebox.showwarning("Selection Error", "Please select an event to mark as finished.")

    def generate_plot(self):
        if not self.events:
            messagebox.showwarning("No Events", "No active events to plot.")
            return

        # Clear previous plot if exists
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        fig, ax = plt.subplots()
        for event in self.events:
            x = event["importance"]
            y = event["urgency"]
            ax.scatter(x, y, label=event["name"])
            ax.annotate(event["name"], (x, y), xytext=(5, 5), textcoords="offset points")

        ax.set_xlim(-5.5, 5.5)
        ax.set_ylim(-5.5, 5.5)
        ax.set_xticks(range(-5, 6))
        ax.set_yticks(range(-5, 6))
        ax.set_xlabel("Importance (-5 to 5)")
        ax.set_ylabel("Urgency (-5 to 5)")
        ax.set_title("Event Priority Matrix")
        
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.spines['top'].set_linewidth(0)
        ax.spines['right'].set_linewidth(0)
        ax.grid(True, linestyle='--', alpha=0.3)
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)

        self.canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(expand=True, fill="both")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")  # Initial size for testing
    app = ScheduleApp(root)
    root.mainloop()