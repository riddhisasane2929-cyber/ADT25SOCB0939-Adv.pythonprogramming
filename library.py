class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_available = True

    def __str__(self):
        status = "Available" if self.is_available else "Borrowed"
        return f"{self.book_id}: {self.title} by {self.author} - {status}"


class Patron:
    def __init__(self, patron_id, name):
        self.patron_id = patron_id
        self.name = name
        self.borrowed_books = []

    def borrow_book(self, book):
        self.borrowed_books.append(book)

    def return_book(self, book):
        if book in self.borrowed_books:
            self.borrowed_books.remove(book)

    def __str__(self):
        books = ", ".join(book.title for book in self.borrowed_books)
        return f"{self.patron_id}: {self.name} | Borrowed: {books or 'None'}"


class Library:
    def __init__(self, name):
        self.name = name
        self.books = {}
        self.patrons = {}

    def add_book(self, book):
        if book.book_id in self.books:
            print("Book ID already exists.")
            return

        self.books[book.book_id] = book
        print(f"Book '{book.title}' added successfully.")

    def register_patron(self, patron):
        if patron.patron_id in self.patrons:
            print("Patron ID already exists.")
            return

        self.patrons[patron.patron_id] = patron
        print(f"Patron '{patron.name}' registered successfully.")

    def borrow_book(self, book_id, patron_id):
        if book_id not in self.books:
            print("Book not found.")
            return

        if patron_id not in self.patrons:
            print("Patron not found.")
            return

        book = self.books[book_id]
        patron = self.patrons[patron_id]

        if not book.is_available:
            print(f"'{book.title}' is already borrowed.")
            return

        book.is_available = False
        patron.borrow_book(book)

        print(f"'{book.title}' borrowed by {patron.name}.")

    def return_book(self, book_id, patron_id):
        if book_id not in self.books:
            print("Book not found.")
            return

        if patron_id not in self.patrons:
            print("Patron not found.")
            return

        book = self.books[book_id]
        patron = self.patrons[patron_id]

        if book not in patron.borrowed_books:
            print(f"{patron.name} did not borrow '{book.title}'.")
            return

        book.is_available = True
        patron.return_book(book)

        print(f"'{book.title}' returned successfully.")

    def display_books(self):
        print("\n--- Library Books ---")

        if not self.books:
            print("No books in the library.")
            return

        for book in self.books.values():
            print(book)

    def display_patrons(self):
        print("\n--- Registered Patrons ---")

        if not self.patrons:
            print("No registered patrons.")
            return

        for patron in self.patrons.values():
            print(patron)


# -------------------------
# Example Usage
# -------------------------

library = Library("City Library")

# Add books
library.add_book(Book(1, "Python Programming", "John Smith"))
library.add_book(Book(2, "Clean Code", "Robert C. Martin"))
library.add_book(Book(3, "The Alchemist", "Paulo Coelho"))

# Register patrons
library.register_patron(Patron(101, "Alice"))
library.register_patron(Patron(102, "Bob"))

# Display books and patrons
library.display_books()
library.display_patrons()

# Borrow books
print("\n--- Borrowing Books ---")
library.borrow_book(1, 101)
library.borrow_book(2, 102)

# Try to borrow an already borrowed book
library.borrow_book(1, 102)

# Display current status
library.display_books()
library.display_patrons()

# Return a book
print("\n--- Returning Book ---")
library.return_book(1, 101)

# Display final status
library.display_books()
library.display_patrons()