import tkinter as tk
from tkinter import messagebox
from services.book_service import BookService
from services.member_service import MemberService
from services.issue_service import IssueService
from ui.styles import *

class Dashboard:
    def __init__(self):
        self.books = BookService()
        self.members = MemberService()
        self.issue = IssueService()

        self.root = tk.Tk()
        self.root.title("Library Dashboard")
        self.root.geometry("500x500")
        self.root.configure(bg=BG)

        tk.Label(
            self.root,
            text="Library Management System",
            font=TITLE,
            bg=BG
        ).pack(pady=10)

        self.btn("Add Book", self.add_book)
        self.btn("View Books", self.view_books)
        self.btn("Add Member", self.add_member)
        self.btn("Issue Book", self.issue_book)
        self.btn("Return Book", self.return_book)

    def btn(self, text, cmd):
        tk.Button(
            self.root,
            text=text,
            bg=BTN,
            fg="white",
            font=FONT,
            width=20,
            command=cmd
        ).pack(pady=5)

    # ---------------- BOOKS ----------------

    def add_book(self):
        w = tk.Toplevel(self.root)
        w.title("Add Book")

        tk.Label(w, text="Title").pack(pady=5)
        t = tk.Entry(w)
        t.pack(pady=5)

        tk.Label(w, text="Author").pack(pady=5)
        a = tk.Entry(w)
        a.pack(pady=5)

        def save():
            if not t.get() or not a.get():
                messagebox.showerror("Error", "All fields are required")
                return

            self.books.add(t.get(), a.get())
            messagebox.showinfo("Success", "Book added successfully")
            w.destroy()

        tk.Button(w, text="Save", command=save).pack(pady=10)

    def view_books(self):
        w = tk.Toplevel(self.root)
        w.title("Books List")

        books = self.books.get_all()
        if not books:
            tk.Label(w, text="No books found").pack()
            return

        for b in books:
            status = "Available" if b["available"] else "Issued"
            tk.Label(
                w,
                text=f'{b["id"]}. {b["title"]} by {b["author"]} ({status})'
            ).pack(anchor="w")

    # ---------------- MEMBERS ----------------

    def add_member(self):
        w = tk.Toplevel(self.root)
        w.title("Add Member")

        tk.Label(w, text="Member Name").pack(pady=5)
        n = tk.Entry(w)
        n.pack(pady=5)

        def save():
            if not n.get():
                messagebox.showerror("Error", "Name cannot be empty")
                return

            self.members.add(n.get())
            messagebox.showinfo("Success", "Member added successfully")
            w.destroy()

        tk.Button(w, text="Save", command=save).pack(pady=10)

    # ---------------- ISSUE / RETURN ----------------

    def issue_book(self):
        w = tk.Toplevel(self.root)
        w.title("Issue Book")

        tk.Label(w, text="Book ID").pack(pady=5)
        b = tk.Entry(w)
        b.pack(pady=5)

        tk.Label(w, text="Member Name").pack(pady=5)
        m = tk.Entry(w)
        m.pack(pady=5)

        def issue():
            if not b.get().isdigit() or not m.get():
                messagebox.showerror("Error", "Invalid input")
                return

            success = self.issue.issue(int(b.get()), m.get())
            if success:
                messagebox.showinfo("Success", "Book issued successfully")
                w.destroy()
            else:
                messagebox.showerror("Error", "Book not available")

        tk.Button(w, text="Issue", command=issue).pack(pady=10)

    def return_book(self):
        w = tk.Toplevel(self.root)
        w.title("Return Book")

        tk.Label(w, text="Book ID").pack(pady=5)
        b = tk.Entry(w)
        b.pack(pady=5)

        def ret():
            if not b.get().isdigit():
                messagebox.showerror("Error", "Enter a valid Book ID")
                return

            self.issue.return_book(int(b.get()))
            messagebox.showinfo("Success", "Book returned successfully")
            w.destroy()

        tk.Button(w, text="Return", command=ret).pack(pady=10)

    # ---------------- RUN ----------------

    def run(self):
        self.root.mainloop()
