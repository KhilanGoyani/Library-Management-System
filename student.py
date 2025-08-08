from datetime import datetime
from database import Database
from book import Book

class Student:
    # Constructor to initialize the student
    def __init__(self, student_id, student_name, student_password, student_batch):
        self.student_id = student_id
        self.student_name = student_name
        self.student_password = student_password
        self.student_batch = student_batch

    # This method is used to view all the books by the Student
    def view_books(self):
        try:
            with open('library_data.txt', 'r') as file:
                books = file.readlines()
                if not books:
                    print('\t\t\t\t------------------------------------------')
                    print('\t\t\t\t|   No books available currently!         |')
                    print('\t\t\t\t------------------------------------------')
                    return
                print('\t\t\t\t------------------------------------------')
                print('\t\t\t\t|              Available Books            |')
                print('\t\t\t\t------------------------------------------')
                print('\t\t\t\t--------------------------------------------------------')
                for book in books:
                    print('\t\t\t|        ',book.strip(),'    |')
                print('\t\t\t----------------------------------------------------------')
        except FileNotFoundError:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|     Error: Books database not found!    |')
            print('\t\t\t\t------------------------------------------')

    # This method is used to borrow a book by the Student
    def borrow_book(self):
        try:
            with open('library_data.txt', 'r') as file:
                books = file.readlines()

            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|        Available Books for Borrowing    |')
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t----------------------------------------------------------')
            for book in books:
                print('\t\t\t|        ',book.strip(),'    |')
            print('\t\t\t----------------------------------------------------------')
            
            selected_book_id = input('\t\t\t\tEnter the Book ID you want to borrow: ')

            with open('borrowed_books.txt', 'a') as file:
                file.write(f'{self.student_id},{selected_book_id},{self.student_name},{datetime.now().strftime("%d-%m-%Y")}\n')
            
            print('\t\t\t\t------------------------------------------')
            print(f'\t\t\t\t|      Successfully Borrowed Book ID: {selected_book_id} |')
            print('\t\t\t\t------------------------------------------')

        except FileNotFoundError:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|     Error: Books database not found!    |')
            print('\t\t\t\t------------------------------------------')

    # This method is used to return a book by the Student
    def return_book(self):
        try:
            with open('borrowed_books.txt', 'r') as file:
                borrowed_books = file.readlines()
            
            if not borrowed_books:
                print('\t\t\t\t------------------------------------------')
                print('\t\t\t\t|    Error: No books have been borrowed yet!  |')
                print('\t\t\t\t------------------------------------------')
                return
            
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|    Your Borrowed Books                 |')
            print('\t\t\t\t------------------------------------------')
            for book in borrowed_books:
                if book.startswith(self.student_id):
                    print(book.strip())
            
            book_id_to_return = input('\t\t\t\tEnter the Book ID you want to return: ')
            return_date_input = input('Enter the return date (DD-MM-YYYY): ')
            return_date = datetime.strptime(return_date_input, '%d-%m-%Y')
            updated_books = [book for book in borrowed_books if not (book.startswith(self.student_id) and book.split(',')[1] == book_id_to_return)]
            
            with open('borrowed_books.txt', 'w') as file:
                file.writelines(updated_books)

            print('\t\t\t\t------------------------------------------')
            print(f'\t\t\t\t|      Successfully Returned Book ID: {book_id_to_return} |')
            print('\t\t\t\t------------------------------------------')
            
        except FileNotFoundError:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|     Error: Borrowed books database not found! |')
            print('\t\t\t\t------------------------------------------')

    # This method is used to check fines of the Student
    def check_fines(self):
        try:
            with open('borrowed_books.txt', 'r') as file:
                borrowed_books = file.readlines()
            
            total_fine = 0
            if not borrowed_books:
                print('\t\t\t\t------------------------------------------')
                print('\t\t\t\t|    No books have been borrowed yet!    |')
                print('\t\t\t\t------------------------------------------')
                return total_fine

            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|      Borrowed Books with Fines         |')
            print('\t\t\t\t------------------------------------------')
            for book in borrowed_books:
                if book.startswith(self.student_id):
                    book_details = book.strip().split(',')
                    borrow_date = datetime.strptime(book_details[3], '%d-%m-%Y')
                    return_date_input = input('Enter the return date (DD-MM-YYYY): ')
                    current_date = datetime.strptime(return_date_input, '%d-%m-%Y')
                    days_held = (current_date - borrow_date).days
                    fine = (days_held ) * 20
                    total_fine += fine
                    print(f'{book_details[1]} - Borrowed on {book_details[3]} - Fine: Rs. {fine}')
            print(f'\t\t\t\tTotal Fine: Rs. {total_fine}')
            print('\t\t\t\t------------------------------------------')
            return total_fine
        except FileNotFoundError:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|     Error: Borrowed books database not found! |')
            print('\t\t\t\t------------------------------------------')

    # This method is used to deregister the Student
    def deregister(self):
        fine = self.check_fines()
        if fine > 0:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|     Please return borrowed books and pay fines. |')
            print('\t\t\t\t------------------------------------------')
            return

        print(f'\t\t\t\tAre you sure you want to deregister, {self.student_name}? Y/n')
        option = input('\t\t\t\t-> ')
        if option.lower() == 'y':
            # Remove student from 'students.txt'
            with open('students.txt', 'r') as file:
                students = file.readlines()
            
            updated_students = [student for student in students if not student.startswith(self.student_id)]
            
            with open('students.txt', 'w') as file:
                file.writelines(updated_students)

            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|     You have been deregistered!        |')
            print('\t\t\t\t------------------------------------------')

    # search book from text file
    def search_book_in_file(self):
        book_to_search = input("\t\t\t\t       Enter the book name to search: ").strip()

        try:
            with open('library_data.txt', 'r') as file:
                found = False 
                for line in file:
                    book_details = line.strip().split(',')
                    
                    if book_details[1].lower() == book_to_search.lower():
                        print(f"\t\t\t\t      Book ID: {book_details[0]}")
                        found = True
                        break
                
                if not found:
                    print("\t\t\t\t      No book found")
        except FileNotFoundError:
            print('\t\t\t\t------------------------------------------')
            print('\t\t\t\t|     Error: books database not found! |')
            print('\t\t\t\t------------------------------------------')
        
    def __str__(self):
        return (f"""
                \t\t\tStudent ID     : {self.student_id}
                \t\t\tStudent Name   : {self.student_name}
                \t\t\tStudent Batch  : {self.student_batch}
                """)


# Sample function to save a student to the text file
def save_student(student):
    try:
        with open('students.txt', 'a') as file:
            file.write(f'{student.student_id},{student.student_name},{student.student_password},{student.student_batch}\n')
            print('\t\t\t\tStudent Saved Successfully!')
    except FileNotFoundError:
        print('\t\t\t\tError: Unable to save student to file!')
