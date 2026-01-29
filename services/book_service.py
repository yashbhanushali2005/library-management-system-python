from utils.file_handler import FileHandler

BOOKS_FILE = "data/books.json"

class BookService:
    def get_all(self):
        return FileHandler.read(BOOKS_FILE)

    def add(self, title, author):
        books = self.get_all()
        books.append({
            "id": len(books) + 1,
            "title": title,
            "author": author,
            "available": True
        })
        FileHandler.write(BOOKS_FILE, books)

    def update(self, books):
        FileHandler.write(BOOKS_FILE, books)
