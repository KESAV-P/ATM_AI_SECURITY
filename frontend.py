import tkinter as tk

class ATMUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ATM Security System")
        self.root.geometry("600x400")
        self.root.configure(bg="black")

        self.label = tk.Label(
            self.root,
            text="WELCOME\nPLEASE INSERT YOUR CARD",
            font=("Arial", 22),
            fg="green",
            bg="black"
        )
        self.label.pack(expand=True)

    def show_safe(self):
        self.root.configure(bg="black")
        self.label.config(
            text="ATM STATUS: SAFE\nPLEASE INSERT YOUR CARD",
            fg="green",
            bg="black"
        )
        self.root.update()

    def show_alert(self, level, reason):
        self.root.configure(bg="red")
        self.label.config(
            text=f"🚨 {level} 🚨\n{reason}\n\nATM USAGE LOCKED",
            fg="white",
            bg="red"
        )
        self.root.update()

    def start(self):
        self.root.mainloop()
