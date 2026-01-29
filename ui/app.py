import tkinter as tk
from tkinter import messagebox
from services.book_service import BookService
from services.member_service import MemberService
from ui.styles import BG_COLOR, BTN_COLOR, FONT

class LibraryApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Library Management System")
        self.root.geometry("500x400")
        self.root.configure(bg=BG_COLOR)

        self.book_service = BookService()
        self.member_service = MemberService()

        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Library Management", font=("Arial", 18, "bold"), bg=BG_COLOR).pack(pady=10)

        tk.Button(self.root, text="Add Book", command=self.add_book_ui, bg=BTN_COLOR, fg="white", font=FONT).pack(pady=5)
        tk.Button(self.root, text="View Books", command=self.view_books, bg=BTN_COLOR, fg="white", font=FONT).pack(pady=5)

        tk.Button(self.root, text="Add Member", command=self.add_member_ui, bg=BTN_COLOR, fg="white", font=FONT).pack(pady=5)
        tk.Button(self.root, text="View Members", command=self.view_members, bg=BTN_COLOR, fg="white", font=FONT).pack(pady=5)

    def add_book_ui(self):
        window = tk.Toplevel(self.root)
        window.title("Add Book")

        tk.Label(window, text="Title").pack()
        title_entry = tk.Entry(window)
        title_entry.pack()

        tk.Label(window, text="Author").pack()
        author_entry = tk.Entry(window)
        author_entry.pack()

        def save():
            self.book_service.add_book(title_entry.get(), author_entry.get())
            messagebox.showinfo("Success", "Book added successfully")
            window.destroy()

        tk.Button(window, text="Save", command=save).pack(pady=10)

    def view_books(self):
        books = self.book_service.get_books()
        window = tk.Toplevel(self.root)
        window.title("Books")

        for book in books:
            status = "Available" if book["available"] else "Issued"
            tk.Label(window, text=f'{book["id"]}. {book["title"]} by {book["author"]} ({status})').pack(anchor="w")

    def add_member_ui(self):
        window = tk.Toplevel(self.root)
        window.title("Add Member")

        tk.Label(window, text="Member Name").pack()
        name_entry = tk.Entry(window)
        name_entry.pack()

        def save():
            self.member_service.add_member(name_entry.get())
            messagebox.showinfo("Success", "Member added successfully")
            window.destroy()

        tk.Button(window, text="Save", command=save).pack(pady=10)

    def view_members(self):
        members = self.member_service.get_members()
        window = tk.Toplevel(self.root)
        window.title("Members")

        for member in members:
            tk.Label(window, text=f'{member["id"]}. {member["name"]}').pack(anchor="w")

    def run(self):
        self.root.mainloop()
