from utils.file_handler import FileHandler

ISSUE_FILE = "data/issued_books.json"
BOOK_FILE = "data/books.json"

class IssueService:
    def issue(self, book_id, member_name):
        issues = FileHandler.read(ISSUE_FILE)
        books = FileHandler.read(BOOK_FILE)

        for book in books:
            if book["id"] == book_id and book["available"]:
                book["available"] = False
                issues.append({
                    "book_id": book_id,
                    "member": member_name
                })
                FileHandler.write(ISSUE_FILE, issues)
                FileHandler.write(BOOK_FILE, books)
                return True
        return False

    def return_book(self, book_id):
        issues = FileHandler.read(ISSUE_FILE)
        books = FileHandler.read(BOOK_FILE)

        issues = [i for i in issues if i["book_id"] != book_id]

        for book in books:
            if book["id"] == book_id:
                book["available"] = True

        FileHandler.write(ISSUE_FILE, issues)
        FileHandler.write(BOOK_FILE, books)
