from student import Student
from librarian import Librarian
from database import Database
from book import Book
from pwinput import pwinput
import os

# This method is the starting point of the application
def start():
    wrong_option = 5
    failed_auth = 5
    while True:
        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\t|                  Home                  |')
        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\t|          1. Student Login              |')
        print('\t\t\t\t|          2. Student Register           |')
        print('\t\t\t\t|          3. Librarian Login            |')
        print('\t\t\t\t|          4. Librarian Register         |')
        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\t\tPress 0 to exit')
        print('\t\t\t\t\tEnter your option')
        choice = input('\t\t\t\t\t-> ').strip()

        if choice == '0':  # Exit condition
            print("\t\t\t\t\tExiting the program...")
            break  # Exit the loop
        
        if len(choice) == 0 or wrong_option == 0:
            break

        match choice:
            case '1':
                if failed_auth < 0:
                    break
                print('\t\t\t\t\tEnter your ID ')
                stud_id = input('\t\t\t\t\t-> ').strip()

                print('\t\t\t\t\tEnter your Password')
                stud_pass = pwinput('\t\t\t\t\t-> ', mask='*').strip()

                if len(stud_id) == 0 or len(stud_pass) == 0:
                    print('\t\t\t\t------------------------------------------')
                    print('\t\t\t\t|         Error : Invalid Entry!         |')
                    print(f'\t\t\t\t\t|      Remaining attempts : {failed_auth}      |')
                    print('\t\t\t\t------------------------------------------')
                    failed_auth -= 1
                    continue

                stud_obj = stud_auth(stud_id, stud_pass)

                if stud_obj:
                    print('\t\t\t\t------------------------------------------')
                    print('\t\t\t\t|                 Hello!                 |')
                    print('\t\t\t\t------------------------------------------')
                    print(stud_obj)
                    print('\t\t\t\t------------------------------------------')

                    stud_options(stud_obj)
                else:
                    print('\t\t\t\t------------------------------------------')
                    print('\t\t\t\t|    Error : Authentication Failed!      |')
                    print(f'\t\t\t\t|    Remaining attempts : {failed_auth}              |')
                    print('\t\t\t\t------------------------------------------')
                    failed_auth -= 1

            case '2':
                status = False
                while True:
                    print('\t\t\t\t\tEnter your Name')
                    stud_name = input('\t\t\t\t\t-> ').strip()

                    print('\t\t\t\t\tEnter your Password')
                    stud_pass_1 = pwinput('\t\t\t\t\t-> ', mask='*').strip()

                    print('\t\t\t\t\tRe-enter your Password')
                    stud_pass_2 = pwinput('\t\t\t\t\t-> ', mask='*').strip()

                    if stud_pass_1 != stud_pass_2:
                        print('\t\t\t\t------------------------------------------')
                        print('\t\t\t\t|          Password not matching         |')
                        print('\t\t\t\t|           Press enter to exit          |')
                        print('\t\t\t\t------------------------------------------')
                        ch = input('\t\t\t\t\t-> ')
                        break

                    print('\t\t\t\t\tEnter Batch')
                    stud_batch = input('\t\t\t\t\t-> ')

                    if len(stud_name) < 1 or len(stud_pass_1) < 1 or len(stud_pass_2) < 1 or len(stud_batch) < 1:
                        print('\t\t\t\t\tPlease enter a valid student details.')
                        ch = input('\t\t\t\t\tPress Enter to continue....')
                        if len(ch) <= 0:
                            break
                    else:
                        status = True
                        break

                if status:
                    stud = Student(student_id=create_id(),
                                   student_name=stud_name,
                                   student_password=stud_pass_1,
                                   student_batch=stud_batch)

                    save_student(stud)

            case '3':
                if failed_auth < 0:
                    break
                print('\t\t\t\t\tEnter your ID')
                lib_id = input('\t\t\t\t\t-> ').strip()

                print('\t\t\t\t\tEnter your Password')
                lib_pass = pwinput('\t\t\t\t\t-> ', mask='*').strip()

                if len(lib_id) == 0 or len(lib_pass) == 0:
                    print('\t\t\t\t------------------------------------------')
                    print('\t\t\t\t|         Error : Invalid Entry!         |')
                    print(f'\t\t\t\t\t|      Remaining attempts : {failed_auth}      |')
                    print('\t\t\t\t------------------------------------------')
                    failed_auth -= 1
                    continue

                lib_obj = lib_auth(lib_id, lib_pass)

                if lib_obj:
                    print('\t\t\t\t------------------------------------------')
                    print('\t\t\t\t|                 Hello!                 |')
                    print('\t\t\t\t------------------------------------------')
                    print(lib_obj)
                    print('\t\t\t\t------------------------------------------')

                    lib_options(lib_obj)
                else:
                    print('\t\t\t\t------------------------------------------')
                    print('\t\t\t\t|    Error : Authentication Failed!      |')
                    print(f'\t\t\t\t|    Remaining attempts : {failed_auth}              |')
                    print('\t\t\t\t------------------------------------------')
                    failed_auth -= 1
            
            case '4':
                status = True
                while status:
                    print('\t\t\t\t\tEnter your Name')
                    lib_name = input('\t\t\t\t\t-> ').strip()

                    print('\t\t\t\t\tEnter your Password')
                    lib_pass_1 = pwinput('\t\t\t\t\t-> ', mask='*').strip()

                    print('\t\t\t\t\tRe-enter your Password')
                    lib_pass_2 = pwinput('\t\t\t\t\t-> ', mask='*').strip()

                    if lib_pass_1 != lib_pass_2:
                        print('\t\t\t\t------------------------------------------')
                        print('\t\t\t\t|          Password not matching         |')
                        print('\t\t\t\t|           Press enter to exit          |')
                        print('\t\t\t\t------------------------------------------')
                        ch = input('\t\t\t\t\t-> ')
                        break

                    if len(lib_name) < 1 or len(lib_pass_1) < 1 or len(lib_pass_2) < 1:
                        print('\t\t\t\t\tPlease enter a valid details.')
                        ch = input('\t\t\t\t\tPress Enter to continue....')
                        if len(ch) <= 0:
                            break
                    else:
                        status = True
                        break

                if status:
                    lib = Librarian(librarian_id=create_lib_id(),
                                   librarian_name=lib_name,
                                   librarian_password=lib_pass_1)

                    save_librarian(lib)
            
            case _:
                print('\t\t\t\t------------------------------------------')
                print('\t\t\t\t|       Enter the mentioned choices      |')
                print(f'\t\t\t\t|       Remaining attempts : {wrong_option}           |')
                print('\t\t\t\t------------------------------------------')
                wrong_option -= 1

# This method lists all the actions that student can perform
def stud_options(stud_obj):
    wrong_option = 5
    Data=Database()
    
    while True:
        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\t|              Student Menu              |')
        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\t|             1. View Books              |')
        print('\t\t\t\t|             2. Borrow Books            |')
        print('\t\t\t\t|             3. Return Books            |')
        print('\t\t\t\t|             4. Compute Fines           |')
        print('\t\t\t\t|             5. De-Register             |')
        print('\t\t\t\t|             6. Search Books             |')
        print('\t\t\t\t------------------------------------------')

        print('\t\t\t\t\tPress enter to exit')
        print('\t\t\t\t\tEnter your option ')
        choice = input('\t\t\t\t\t-> ')

        if len(choice) == 0 or wrong_option == 0:
            break

        match choice:
            case '1':
                stud_obj.view_books()
            case '2':
                stud_obj.borrow_book()
                print("\t\t\t\tEnter confirm Book ID to borrow: ")
                book_id = input('\t\t\t\t\t-> ').strip()
                Data.borrow_book(stud_obj,book_id)
            case '3':
                stud_obj.return_book()
                print("\t\t\t\tEnter confirm Book ID to return: ")
                book_id = input('\t\t\t\t\t-> ').strip()
                Data.return_book(stud_obj,book_id)
            case '4':
                stud_obj.check_fines()
            case '5':
                status = stud_obj.deregister()
                if status:
                    break
            case '6':
                stud_obj.search_book_in_file()
            case _:
                print('\t\t\t\t-------------------------------------------------------')
                print('\t\t\t\t|       Enter the mentioned choices      |')
                print(f'\t\t\t\t|       Remaining attempts : {wrong_option}           |')
                print('\t\t\t\t-------------------------------------------------------')
                wrong_option -= 1

# This method lists all the actions that librarian can perform
def lib_options(lib_obj):
    wrong_option = 5

    while True:
        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\t|              Librarian Menu            |')
        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\t|             1. View Books              |')
        print('\t\t\t\t|             2. Add Books               |')
        print('\t\t\t\t|             3. Update Books            |')
        print('\t\t\t\t|             4. Remove Books            |')
        print('\t\t\t\t------------------------------------------')
        print('\t\t\t\t\tPress enter to exit')
        print('\t\t\t\t\tEnter your option ')
        choice = input('\t\t\t\t\t-> ')

        if len(choice) == 0 or wrong_option == 0:
            break

        match choice:
            case '1':
                lib_obj.view_books()
            case '2':
                lib_obj.add_books()
            case '3':
                lib_obj.update_book()
            case '4':
                lib_obj.remove_book()
            case _:
                print('\t\t\t\t------------------------------------------')
                print('\t\t\t\t|       Enter the mentioned choices      |')
                print(f'\t\t\t\t|       Remaining attempts : {wrong_option}           |')
                print('\t\t\t\t------------------------------------------')
                wrong_option -= 1

    
# This method is used to get the last student id from the database
def fetch_last_student_id():
    try:
        with open('students.txt', 'r') as file:
            last_line = file.readlines()[-1]  # Read the last line
            return last_line.split(',')[0]
    except IndexError:
        return 'st0000'  # If the file is empty, return 'st0000'

# This method is used to save student to database
def save_student(student):
    with open('students.txt', 'a') as file:
        file.write(f"{student.student_id},{student.student_name},{student.student_password},{student.student_batch}\n")

    print('\t\t\t\t------------------------------------------')
    print('\t\t\t\t|       Student Saved successfully       |')
    print('\t\t\t\t------------------------------------------')
    print(student)
    print('\t\t\t\t------------------------------------------')

# This method is used to authenticate students
def stud_auth(student_id, student_password):
    with open('students.txt', 'r') as file:
        for line in file:
            student_data = line.strip().split(',')
            if student_data[0] == student_id and student_data[2] == student_password:
                return Student(student_id=student_data[0], student_name=student_data[1], student_password=student_data[2], student_batch=student_data[3])
    return None

# This method is used to generate Student ID
def create_id():
    try:
        with open('students.txt', 'r') as file:
            last_line = file.readlines()[-1]  # Read the last line
            last_student_id = last_line.split(',')[0]
            new_id = int(last_student_id[2:]) + 1
        num_of_zeros = 4
        return f"st{new_id:0{num_of_zeros}}"
    except IndexError:
        return 'st0001'  # If the file is empty, start from 'st0001'

# This method is used to save librarian to database
def save_librarian(lib):
    with open('librarians.txt', 'a') as file:
        file.write(f"{lib.librarian_id},{lib.librarian_name},{lib.librarian_password}\n")

    print('\t\t\t\t------------------------------------------')
    print('\t\t\t\t|      Librarian Saved successfully      |')
    print('\t\t\t\t------------------------------------------')
    print(lib)
    print('\t\t\t\t------------------------------------------')

# This method is used to authenticate librarians
def lib_auth(lib_id, lib_pass):
    with open('librarians.txt', 'r') as file:
        for line in file:
            lib_data = line.strip().split(',')
            if lib_data[0] == lib_id and lib_data[2] == lib_pass:
                return Librarian(librarian_id=lib_data[0], librarian_name=lib_data[1], librarian_password=lib_data[2])
    return None

# This method is used to create the librarian id.
def create_lib_id():
    try:
        with open('librarians.txt', 'r') as file:
            last_line = file.readlines()[-1]  # Read the last line
            last_lib_id = last_line.split(',')[0]
            new_id = int(last_lib_id[2:]) + 1
        num_of_zeros = 4
        return f"lb{new_id:0{num_of_zeros}}"
    except IndexError:
        return 'lb0001'  # If the file is empty, start from 'lb0001'

start()