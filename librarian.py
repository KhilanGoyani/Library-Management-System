from datetime import datetime
from book import Book

class Librarian:
    # Constructor to initialize the librarian
    def __init__(self, librarian_id, librarian_name, librarian_password):
        self.librarian_id = librarian_id
        self.librarian_name = librarian_name
        self.librarian_password = librarian_password

    # Helper method to read books from the text file
    def _read_books_from_file(self):
        books = []
        try:
            with open('library_data.txt', 'r') as file:
                lines = file.readlines()
                for line in lines:
                    data = line.strip().split(',')
                    if len(data) == 7:  # Ensure correct data format
                        book = Book(book_id=int(data[0]),
                                    book_name=data[1],
                                    book_author=data[2],
                                    book_publisher=data[3],
                                    book_publish_date=data[4],
                                    book_availability_status=data[5],
                                    book_copies=data[6])
                        books.append(book)
        except FileNotFoundError:
            return []  # Return empty list if file does not exist
        return books

    # Helper method to save books to the text file
    def _save_books_to_file(self, books):
        with open('library_data.txt', 'w') as file:
            for book in books:
                file.write(f"{book.book_id},{book.book_name},{book.book_author},{book.book_publisher},{book.book_publish_date},{book.book_availability_status},{book.book_copies}\n")

    # This method is used to view all the books by the librarian
    def view_books(self):
        books = self._read_books_from_file()
        if books:
            for book in books:
                print(book)
        else:
            print('\t\t\t\tNo books available.')

    # This method is used to add a book by the librarian
    def add_books(self):
        try:
            print('\t\t\t\t\tEnter Book Name')
            book_name = input('\t\t\t\t\t-> ').strip()

            print('\t\t\t\t\tEnter Book Author')
            book_author = input('\t\t\t\t\t-> ').strip()

            print('\t\t\t\t\tEnter Book Publisher [Optional]')
            book_publisher = input('\t\t\t\t\t-> ').strip()

            print('\t\t\t\t\tEnter Book Publish Date (DD-MM-YYYY) [Optional]')
            book_publish_date = input('\t\t\t\t\t-> ').strip()
            
            print('\t\t\t\t\tEnter Book Publish status')
            book_availability_status = input('\t\t\t\t\t-> ').strip()

            print('\t\t\t\t\tEnter No. of copies (Default: 1) [Optional]')
            book_copies = input('\t\t\t\t\t-> ').strip()

            if len(book_copies) == 0:
                book_copies = '1'

            flag = False
            if len(book_publish_date) == 0 or len(book_publish_date) == 10:
                if len(book_publish_date) == 10:
                    day, month, year = book_publish_date.split('-')
                    datetime(day=int(day), month=int(month), year=int(year))
            else:
                flag = True

            if len(book_name) == 0 or len(book_author) == 0 or flag == True or int(book_copies) < 0:
                raise ValueError

        except ValueError as exp:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|                 Error!                 |')
            print('\t\t\t\t------------------------------------------')
            print(f'\t\t\t\t\t\t{exp}')
            print('\t\t\t\t------------------------------------------')

        except Exception as exp:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|        Some Error occurred              |')
            print('\t\t\t\t------------------------------------------')
            print(f'\t\t\t\t\t\t{exp}')
            print('\t\t\t\t------------------------------------------')

        else:
            books = self._read_books_from_file()
            try:
                book_id = max([book.book_id for book in books]) + 1 if books else 1
            except ValueError:
                book_id = 1

            book_obj = Book(book_id=book_id,
                            book_name=book_name,
                            book_author=book_author,
                            book_publisher=book_publisher,
                            book_publish_date=book_publish_date,
                            book_availability_status=book_availability_status,
                            book_copies=book_copies)

            books.append(book_obj)
            self._save_books_to_file(books)
            print('\t\t\t\t------------------------------------------')
            print(f'\t\t\t\t|               Book Saved               |')
            print('\t\t\t\t------------------------------------------')
            print(book_obj)
            print('\t\t\t\t------------------------------------------')

    # This method is used to update a book by the librarian
    def update_book(self):
        books = self._read_books_from_file()
        if not books:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|             No Books Available         |')
            print('\t\t\t\t------------------------------------------')
            return

        print('\t\t\t\tEnter the Book ID to Update')
        book_id_to_update = int(input('\t\t\t\t-> '))

        book_to_update = None
        for book in books:
            if book.book_id == book_id_to_update:
                book_to_update = book
                break

        if not book_to_update:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|             Book not Found!           |')
            print('\t\t\t\t------------------------------------------')
            return

        try:
            print('\t\t\t\t\tEnter New Book Name')
            book_name = input('\t\t\t\t\t-> ').strip()

            print('\t\t\t\t\tEnter New Book Author')
            book_author = input('\t\t\t\t\t-> ').strip()

            print('\t\t\t\t\tEnter New Book Publisher [Optional]')
            book_publisher = input('\t\t\t\t\t-> ').strip()

            print('\t\t\t\t\tEnter New Book Publish Date (DD-MM-YYYY) [Optional]')
            book_publish_date = input('\t\t\t\t\t-> ').strip()

            print('\t\t\t\t\tEnter New No. of copies (Default: 1) [Optional]')
            book_copies = input('\t\t\t\t\t-> ').strip()

            if len(book_copies) == 0:
                book_copies = '1'

            flag = False
            if len(book_publish_date) == 0 or len(book_publish_date) == 10:
                if len(book_publish_date) == 10:
                    day, month, year = book_publish_date.split('-')
                    datetime(day=int(day), month=int(month), year=int(year))
            else:
                flag = True

            if len(book_name) == 0 or len(book_author) == 0 or flag == True or int(book_copies) < 0:
                raise ValueError('Book Details not valid')

        except ValueError as exp:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|                 Error!                 |')
            print('\t\t\t\t------------------------------------------')
            print(f'\t\t\t\t\t\t{exp}')
            print('\t\t\t\t------------------------------------------')

        except Exception as exp:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|        Some Error occurred!           |')
            print('\t\t\t\t------------------------------------------')
            print(f'\t\t\t\t\t\t{exp}')
            print('\t\t\t\t------------------------------------------')

        else:
            book_to_update.book_name = book_name
            book_to_update.book_author = book_author
            book_to_update.book_publisher = book_publisher
            book_to_update.book_publish_date = book_publish_date
            book_to_update.book_copies = book_copies

            self._save_books_to_file(books)
            print('\t\t\t\t------------------------------------------')
            print(f'\t\t\t\t|               Book Updated             |')
            print('\t\t\t\t------------------------------------------')
            print(book_to_update)
            print('\t\t\t\t------------------------------------------')

    # This method is used to remove a book by the librarian
    def remove_book(self):
        books = self._read_books_from_file()
        if not books:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|             No Books Available         |')
            print('\t\t\t\t------------------------------------------')
            return

        print('\t\t\t\tEnter the Book ID to Remove')
        book_id_to_remove = int(input('\t\t\t\t-> '))

        book_to_remove = None
        for book in books:
            if book.book_id == book_id_to_remove:
                book_to_remove = book
                break

        if not book_to_remove:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|             Book not Found!           |')
            print('\t\t\t\t------------------------------------------')
            return

        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\t|                 Alert!                 |')
        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\tAre you sure you want to remove the book? Y/n')
        option = input('\t\t\t\t\t-> ')

        if option == 'Y':
            books.remove(book_to_remove)
            self._save_books_to_file(books)
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|              Book Deleted              |')
            print('\t\t\t\t------------------------------------------')
            print(book_to_remove)
            print('\t\t\t\t------------------------------------------')

    # This method is used to print the details of the librarian
    def __str__(self):
        return f"""
                \t\t\tLibrarian ID     : {self.librarian_id}
                \t\t\tLibrarian Name   : {self.librarian_name}
                """
