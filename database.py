# Importing the required libraries
import datetime
import os
from book import *

class Database:
    # Initializing the Database Object (Null in this case)
    def __init__(self):
        pass

    # This method is used to get all the book details from the books file.
    def view_books(self):
        with open('library_data.txt', mode='r') as file:
            lines = file.readlines()
            count = 1
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|                All Book(s)             |')
            print('\t\t\t\t------------------------------------------')
            for line in lines:
                self.print_it(line)

                if count % 4 == 0:
                    print('\t\t\t\t------------------------------------------')
                    print('\t\t\t\t|       Press enter to view more...      |')
                    print('\t\t\t\t|       Press other key to exit          |')
                    print('\t\t\t\t------------------------------------------')
                    inp = input('\t\t\t\t\t-> ')
                    if len(inp) != 0:
                        break
                count += 1

    # This method is used to view all the books and get the valid book id that the user has selected.
    def view_and_select_books(self):
        with open('b.txt', mode='r') as file:
            lines = file.readlines()
            count = 1
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|                All Book(s)             |')
            print('\t\t\t\t------------------------------------------')
            for line in lines:
                self.print_it(line)

                if count % 4 == 0:
                    print('\t\t\t\t------------------------------------------')
                    print('\t\t\t\t|        Provide accurate Book ID.       |')
                    print('\t\t\t\t|        Press enter to view more...     |')
                    print('\t\t\t\t------------------------------------------')
                    inp = input('\t\t\t\t\t-> ')
                    if len(inp) != 0:
                        return inp
                count += 1

        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\t|        Provide accurate Book ID.       |')
        print('\t\t\t\t|        Press enter to exit.            |')
        print('\t\t\t\t------------------------------------------')
        inp = input('\t\t\t\t\t-> ')

        if len(inp) == 0:
            return False

        return inp

    # This method is used to print the book details from the books file.
    def print_it(self, data):
        try:
            book_data = data.strip().split(',')
            print('\t\t\t\tID            : ', book_data[0])
            print('\t\t\t\tName          : ', book_data[1])
            print('\t\t\t\tAuthor        : ', book_data[2])
            print('\t\t\t\tPublisher     : ', book_data[3])
            print('\t\t\t\tPublish Date  : ', book_data[4])
            print('\t\t\t\tAvailability  : ', book_data[5])
            print('\t\t\t\tNo. of Copies : ', book_data[6])
            print('\t', '-'*110)
        except IndexError:
            pass
        except Exception:
            pass
    
    # This method is used to validate the student details entered
    def authenticate(self, stud_id, stud_password):
        status = False
        from student import Student
        with open('s.txt', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                try:
                    student_data = line.strip().split(',')
                    if student_data[0] == stud_id and student_data[2] == stud_password:
                        status = Student(student_data[0], student_data[1], student_data[2], student_data[3])
                        break
                except IndexError:
                    pass
                except Exception:
                    pass

        return status

    # This method is used to fetch the last student id which is used to generate new id.
    def fetch_last_student_id(self):
        last = []
        with open('s.txt', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                last = line.strip().split(',')
            try:
                return last[0]
            except IndexError:
                return last[0]
            except Exception:
                pass
    
    # This is used to store the student details in students file
    def save_student(self, stud_obj):
        data = f"{stud_obj.student_id},{stud_obj.student_name},{stud_obj.student_password},{stud_obj.student_batch}\n"
        with open('s.txt', mode='a') as file:
            file.write(data)

    # This method allows the student to borrow a book.
    def borrow_book(self, stud_obj, book_id):
        with open('library_data.txt', mode='r') as file:
            books = file.readlines()
            success = False

            with open('temp.txt', mode='a') as temp_file:
                for book in books:
                    try:
                        book_data = book.strip().split(',')
                        if book_data[0] == book_id:
                            if int(book_data[6]) >= 1:
                                book_data[6] = str(int(book_data[6]) - 1)
                                if book_data[6] == "0":
                                    book_data[5] = "False"
                                success = book_data
                    except IndexError:
                        continue
                    except Exception:
                        continue

                    temp_file.write(','.join(book_data) + '\n')

        os.remove('library_data.txt')
        os.rename('temp.txt', 'library_data.txt')

        if success:
            book_obj = Book(success[0], success[1], success[2], success[3], success[4], success[5], success[6])
            trans_id, today_date = self.write_to_transaction_and_borrow_file(stud_obj, book_obj, 'b')
            return trans_id, today_date, book_obj

        return success

    # This method writes to a file that tracks the borrow history.
    def update_all_borrows_file(self, stud_obj, book_obj):
        status = False

        with open('temp.txt', mode='w') as temp_file:
            with open('all_borrows.txt', mode='r') as borrow_file:
                borrow_file_reader = borrow_file.readlines()

                for line in borrow_file_reader:
                    try:
                        borrow_data = line.strip().split(',')
                        if borrow_data[1] == stud_obj.student_id and borrow_data[2] == book_obj.book_id and not status:
                            status = True
                            continue
                    except IndexError:
                        continue
                    except Exception:
                        continue
                    temp_file.write(line)

        os.remove('all_borrows.txt')
        os.rename('temp.txt', 'all_borrows.txt')

    # This method allows the student to return a book.
    def return_book(self, stud_obj, book_id):
        with open('library_data.txt', mode='r') as file:
            books = file.readlines()
            success = False

            with open('temp.txt', mode='a') as temp_file:
                for book in books:
                    try:
                        book_data = book.strip().split(',')
                        if book_data[0] == book_id and not success:
                            book_data[6] = str(int(book_data[6]) + 1)
                            book_data[5] = "True"
                            success = book_data
                    except IndexError:
                        continue
                    except Exception:
                        continue

                    temp_file.write(','.join(book_data) + '\n')

        os.remove('library_data.txt')
        os.rename('temp.txt', 'library_data.txt')

        if success:
            book_obj = Book(success[0], success[1], success[2], success[3], success[4], success[5],success[6])
            trans_id = self.write_to_transaction_and_borrow_file(stud_obj, book_obj, 'r')
            self.update_all_borrows_file(stud_obj, book_obj)

            return trans_id, book_obj
        return success

    # This methods gets the last transaction id of a borrow or return.
    def fetch_last_transaction_id(self):
        last = []
        with open('all_transactions.txt', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                last = line.strip().split(',')
            try:
                return last[0]
            except IndexError:
                return last[0]

    # This method generates current date.
    def get_current_date(self):
        x = datetime.datetime.now()
        return x.strftime("%d-%m-%Y")

    # This method writes borrows and returns to the all_transaction file.
    def write_to_transaction_and_borrow_file(self, stud_obj, book_obj, trans_type):
        transaction_id = self.create_transaction_id()
        today_date = self.get_current_date()

        with open('all_transactions.txt', mode='a') as file:
            data_to_write = f"{transaction_id},{stud_obj.student_id},{book_obj.book_id},{today_date},{trans_type}\n"
            file.write(data_to_write)

        if trans_type == 'b':
            with open('all_borrows.txt', mode='a') as borrow_file:
                data_to_write = f"{transaction_id},{stud_obj.student_id},{book_obj.book_id},{today_date}\n"
                borrow_file.write(data_to_write)

        return transaction_id, today_date

    # This method creates a new transaction id.
    def create_transaction_id(self):
        num_of_zeros = 4
        try:
            returned_id = self.fetch_last_transaction_id()
            new_id = int(returned_id[2:]) + 1
            temp = new_id
            num_of_digits = 0

            while temp > 0:
                num_of_digits += 1
                temp //= 10

            new_id = 'tr' + '0' * (num_of_zeros - num_of_digits) + str(new_id)

        except IndexError:
            new_id = 'tr0001'

        return new_id

    # This method fetches all the borrowed books by a student.
    def get_all_borrowed_books(self, stud_obj):
        with open('all_borrows.txt', mode='r') as borrow_file:
            borrow_file_reader = borrow_file.readlines()
            book_list = []

            for line in borrow_file_reader:
                try:
                    borrow_data = line.strip().split(',')
                    if borrow_data[1] == stud_obj.student_id:

                        with open('b.txt', mode='r') as book_file:
                            book_file_reader = book_file.readlines()

                            for book_line in book_file_reader:
                                try:
                                    book_data = book_line.strip().split(',')
                                    if borrow_data[2] == book_data[0]:
                                        book_obj = Book(book_data[0], book_data[1], book_data[2], book_data[3], book_data[4], book_data[5], book_data[6])
                                        book_obj.borrow_date = borrow_data[3]

                                        book_list.append(book_obj)
                                except IndexError:
                                    pass
                                except Exception:
                                    pass
                except IndexError:
                    pass
                except Exception:
                    pass

        return book_list

    # This method is used to de-register/remove a student.
    def deregister(self, student_obj):
        with open('students.txt', mode='r') as file_read_obj:
            lines = file_read_obj.readlines()

            with open('temp.txt', mode='w') as file_write_object:
                for line in lines:
                    student_data = line.strip().split(',')
                    if student_obj.student_id == student_data[0]:
                        continue
                    file_write_object.write(','.join(student_data) + '\n')

        os.remove('students.txt')
        os.rename('temp.txt', 'students.txt')

    # This method is used to get the last librarian id.
    def fetch_last_librarian_id(self):
        last = []
        with open('l.txt', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                last = line.strip().split(',')
            try:
                return last[0]
            except IndexError:
                return last[0]
            except Exception:
                pass

    # This method is used to save a librarian
    def save_librarian(self, lib_obj):
        data = f"{lib_obj.librarian_id},{lib_obj.librarian_name},{lib_obj.librarian_password}\n"
        with open('l.txt', mode='a') as file:
            file.write(data)

    # This method is used to authenticate the librarian.
    def lib_authenticate(self, lib_id, lib_pass):
        from librarian import Librarian
        status = False
        
        with open('l.txt', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                try:
                    lib_data = line.strip().split(',')
                    if lib_data[0] == lib_id and lib_data[2] == lib_pass:
                        status = Librarian(lib_data[0], lib_data[1], lib_data[2])
                        break
                except IndexError:
                    pass
                except Exception:
                    pass

        return status

    # This method is used to fetch the last librarian id.
    def fetch_last_librarian_id(self):
        last = []
        with open('l.txt', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                last = line.strip().split(',')
            try:
                return last[0]
            except IndexError:
                return last[0]
            except Exception:
                pass
    # Save librarian details into text file
    def save_librarian(self, lib_obj):
        data = f"{lib_obj.librarian_id},{lib_obj.librarian_name},{lib_obj.librarian_password}\n"
        with open('librarian.txt', mode='a') as file:
            file.write(data)

    # Authenticate librarian using provided id and password
    def lib_authenticate(self, lib_id, lib_pass):
        from librarian import Librarian
        status = False
        
        with open('librarian.txt', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                try:
                    lib_data = line.strip().split(',')
                    if lib_data[0] == lib_id and lib_data[2] == lib_pass:
                        status = Librarian(lib_data[0], lib_data[1], lib_data[2])
                        break
                except IndexError:
                    pass
                except Exception:
                    pass

        return status

    # Get the last book ID from the books file
    def get_last_book_id(self):
        last = []
        with open('books.txt', mode='r') as file:
            lines = file.readlines()
            for line in lines:
                last = line.strip().split(',')
            try:
                return last[0]
            except IndexError:
                return last[0]
            except Exception:
                pass

    # Save book details into the books file
    def save_book(self, book_obj):
        book_data = f"{book_obj.book_id},{book_obj.book_name},{book_obj.book_author},{book_obj.book_publisher},{book_obj.book_publish_date},{book_obj.book_availability_status},{book_obj.book_copies}\n"
        with open('books.txt', mode='a') as file_obj:
            file_obj.write(book_data)

    # Update book details in the books file
    def update_book(self, book_obj):
        success = False
        with open('books.txt', mode='r') as file:
            books = file.readlines()

        with open('temp.txt', mode='w') as temp_file:
            for book in books:
                try:
                    book_data = book.strip().split(',')
                    if book_data[0] == book_obj.book_id and not success:
                        success = True
                        data = f"{book_obj.book_id},{book_obj.book_name},{book_obj.book_author},{book_obj.book_publisher},{book_obj.book_publish_date},{book_obj.book_availability_status},{book_obj.book_copies}\n"
                        temp_file.write(data)
                    else:
                        temp_file.write(book)
                except IndexError:
                    continue
                except Exception:
                    continue
        
        os.remove('books.txt')
        os.rename('temp.txt', 'books.txt')
        return success

    # Remove a book's details from the books file
    def remove_book(self, book_id):
        success = False
        with open('books.txt', mode='r') as file:
            books = file.readlines()

        with open('temp.txt', mode='w') as temp_file:
            for book in books:
                try:
                    book_data = book.strip().split(',')
                    if book_data[0] == book_id and not success:
                        success = True
                        continue
                    temp_file.write(book)
                except IndexError:
                    continue
                except Exception:
                    continue
        
        os.remove('books.txt')
        os.rename('temp.txt', 'books.txt')

        if success:
            return f"Book with ID {book_id} has been removed."
        else:
            return "Book not found."
           