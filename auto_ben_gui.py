import auto_ben
import tkinter as tk
from tkinter import filedialog

class AutoBenGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hi Ben")

        self.wait_time_label = tk.Label(self, text="Wait Time:")
        self.wait_time_label.grid(row=0, column=0)
        self.wait_time_entry = tk.Entry(self)
        self.wait_time_entry.grid(row=0, column=1)
        self.wait_time_entry.insert(0, auto_ben.WAIT_TIME)

        self.start_delay_label = tk.Label(self, text="Start Delay:")
        self.start_delay_label.grid(row=1, column=0)
        self.start_delay_entry = tk.Entry(self)
        self.start_delay_entry.grid(row=1, column=1)
        self.start_delay_entry.insert(0, auto_ben.START_DELAY)

        self.log_location_path = tk.Entry(self)
        self.log_location_path.grid(row=2, column=0, columnspan=2, sticky='WE')
        self.log_location_path.insert(0, auto_ben.LOGS_FOLDER)
        self.log_location_path.config(state="readonly")
        self.log_location_button = tk.Button(self, text="Select Log Location", command=self.select_log_location)
        self.log_location_button.grid(row=3, column=0, columnspan=2, sticky='WE')

        self.start_button = tk.Button(self, text="Start", command=self.start_main)
        self.start_button.grid(row=4, column=0, columnspan=2, sticky='WE')
        
        self.grid_columnconfigure(0, weight=1)

        self.update_idletasks()
        self.geometry(f"300x{self.winfo_height()}")

    def select_log_location(self):
        directory = filedialog.askdirectory()
        if directory:
            self.log_location_path.config(state=tk.NORMAL)
            self.log_location_path.delete(0, tk.END)
            self.log_location_path.insert(0, directory)
            self.log_location_path.config(state="readonly")

    def start_main(self):
        auto_ben.WAIT_TIME = int(self.wait_time_entry.get())
        auto_ben.START_DELAY = int(self.start_delay_entry.get())    
        auto_ben.LOGS_FOLDER = self.log_location_path.get()
        self.withdraw()
        auto_ben.main()
        self.deiconify()

if __name__ == "__main__":
    app = AutoBenGUI()
    app.mainloop()
