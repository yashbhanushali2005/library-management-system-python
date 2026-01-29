import tkinter as tk
from tkinter import messagebox
from services.auth_service import AuthService
from ui.dashboard import Dashboard
from ui.styles import *

class LoginUI:
    def __init__(self):
        self.auth = AuthService()
        self.root = tk.Tk()
        self.root.title("Login")
        self.root.geometry("300x250")
        self.root.configure(bg=BG)

        tk.Label(self.root, text="Admin Login", font=TITLE, bg=BG).pack(pady=10)

        self.u = tk.Entry(self.root)
        self.p = tk.Entry(self.root, show="*")
        self.u.pack(pady=5)
        self.p.pack(pady=5)

        tk.Button(self.root, text="Login", bg=BTN, fg="white",
                  command=self.login).pack(pady=10)

    def login(self):
        if self.auth.login(self.u.get(), self.p.get()):
            self.root.destroy()
            Dashboard().run()
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def run(self):
        self.root.mainloop()
