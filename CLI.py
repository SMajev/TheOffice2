from TheOffice2_Database import Database
import pandas as pd
class CLI:
    def __init__(self):
        self.is_working = True
        self.db = Database()
        self.db.session.begin()
        self.welcome()
        
        self.main_loop()

    def main_loop(self):
        self.print_menu()
        while self.is_working:
            option = self.ask_for_step()
            if option == 1:
                self.employees_menu()

            elif option == 2:
                self.dept_menu()

            elif option == 3:
                self.title_menu()

            elif option == 4:
                self.db.count_full_salary_for_everyone()

            elif option == 5:
                self._save_data_to_csv()

            elif option == 0:
                self.exit()

    def employees_menu(self):
        self.print_employees_menu()        
        option = self.ask_for_step()
        if option == 1:            
            emp_id = input('ID: ')
            employe = self.db._search_by_id(emp_id)        
            self.print_find_employee_menu()
            self.employees_menu_2(employe)
            self.print_find_employee_menu()

        elif option == 2:
            self.search_menu()

        elif option == 3:
            name, surname, pesel = self.get_new_user_data()
            self.db.add_employe(name=name, surname=surname, pesel=pesel)
            self.employees_menu()

        elif option == 9:
            self.main_loop()

        elif option == 0:
            self.exit()
        
        
    def employees_menu_2(self, employe):
        emp_id = employe.emp_id
        option = self.ask_for_step()
        if option == 1:
            number_of_hours = int(input('How many hours do you wanna add for employe: '))
            self.db.add_hour_to_salary(emp_id, number_of_hours)
            self.employees_menu_2(employe)

        elif option == 2:
            employe_data = self.db.show_employe_data(emp_id)
            print(employe_data)
            self.employees_menu_2(employe)

        elif option == 3:
            employe_contact = self.db.show_employe_contact(emp_id)
            print(employe_contact)
            self.employees_menu_2(employe)

        elif option == 4:
            employe_salary = self.db.show_employe_salary(emp_id)
            print(employe_salary)
            self.employees_menu_2(employe)

        elif option == 5:            
            self.edit_employe_menu(employe.emp_id)   

        elif option == 6:
            self.edit_contact_menu(employe.emp_id)
            
        else: 
            print('Wrong option! Try again!')


    def edit_employe_menu(self, emp_id):
        self.print_edit_emp_menu()
        option = int(input('What you wanna do?: '))        
        if option == 1:
            new_name = input('New name: ')
            self.db.edit_emp_name(emp_id, new_name)
            self.edit_employe_menu(emp_id)

        elif option == 2:
            new_surname = (input('New surname: '))
            self.db.edit_emp_surname(emp_id, new_surname)
            self.edit_employe_menu(emp_id)

        elif option == 3:
            new_pesel = input('New pesel: ')
            self.db.edit_emp_pesel(emp_id, new_pesel)
            self.edit_employe_menu(emp_id)

        elif option == 4:
            new_birth_date = input('New birth date: ')
            self.db.edit_emp_birth_date(emp_id, new_birth_date)
            self.edit_employe_menu(emp_id)

        elif option == 5:
            new_hire_date = input('New hire date: ')
            self.db.edit_emp_hire_date(emp_id, new_hire_date)
            self.edit_employe_menu(emp_id)

        elif option == 6:
            new_department_id = int(input('New department id: '))
            self.db.edit_emp_department_id(emp_id, new_department_id)
            self.edit_employe_menu(emp_id)

        elif option == 7:
            new_title_id = int(input('New title id: '))
            self.db.edit_emp_title_id(emp_id, new_title_id)
            self.edit_employe_menu(emp_id)

        elif option == 8:
            new_value = int(input('New value/hour: '))
            self.db.edit_per_hour_value(emp_id, new_value)
            self.edit_employe_menu(emp_id)
    
        elif option == 9:
            self.employees_menu_2(emp_id)

        elif option == 0:
            self.is_working = False


    def edit_contact_menu(self, emp_id):
        option = int(input('What you wanna do?: ')) 
        if option == 1:
            new_phone_number = input('New phone number: ')
            self.db.edit_phone_number(emp_id, new_phone_number)

        elif option == 2:
            new_email = input('New email: ')
            self.db.edit_mail(emp_id, new_email)

        elif option == 3:
            new_address = input('New address: ')
            self.db.edit_street_and_no(emp_id, new_adress)

        elif option == 4:
            new_flat_number = input('Flat number: ')
            self.db.edit_flat_number(emp_id, new_flat_number)


    def dept_menu(self):
        self.print_dept_menu()
        option = int(input('What do you wanna do?:'))
        if option == 1:
            self.db.show_all_deparments()

        elif option == 2:
            dept_name = input('Department name: ')
            self.db.add_department(dept_name)

        elif option == 3:
            self.dept_edit_menu()


    def title_menu(self):
        option = int(input('What do you wanna do?:'))
        if option == 1:
            self.db.show_all_titles()
            
        elif option == 2:
            title_name = input('Title name: ')
            department_id = int(input('Department ID: '))
            self.db.add_title(title_name, department_id)


    def dept_edit_menu(self):
        option = int(input('What do you wanna edit?:'))
        if option == 1:
            dept_id = input('Department id: ')
            new_dept_name = input('New department name: ')
            self.db.edit_dept_name(dept_id, new_dept_name)


    def search_menu(self):
        self.print_search()
        try:
            way = int(input('What you wanna do?: '))
            if way == 1:
                name = input('Name: ')
                print(self.db.find_employe_by_name(name))
                
            elif way == 2:
                surname = input('Surname: ')
                print(self.db.find_employe_by_surname(surname))

            elif way == 3:
                pesel = input('Pesel: ')
                print(self.db.find_employe_by_pesel(pesel))
        except:
            print('Wrong data!')

    def close_session(self):
        self.db.session.close()

    def exit(self):
        self.db.session.close()
        self.is_qorking = False

    def _save_data_to_csv(self):
        self.db.save_data_to_csv('salaries', 'salaries.csv', 'salary_id')


    @staticmethod
    def ask_for_id():
        return int(input('ID: '))

    @staticmethod
    def ask_for_step():
        my_input = int(input('What do you wanna do?: '))
        print('\n')
        return my_input

    @staticmethod
    def get_new_user_data():
        name = input('Name: ')
        surname = input('Surname: ')
        pesel = input('Pesel: ')
        return name, surname, pesel


    @staticmethod
    def welcome():
        print('Hello in your DataBase')

    @staticmethod
    def print_search():
        print('1. Search by name')
        print('2. Search by surname')
        print('3. Search by pesel')

    @staticmethod
    def print_menu():
        print('MENU\n')
        print('1. Employees')
        print('2. Department')
        print('3. Titles')
        print('4. Count full salary for every employe')
        print('5. Save data to csv')
        print('\n\n0. Exit\n')

    @staticmethod
    def print_employees_menu():
        print('1. Choose your employe by id')
        print('2. Find employe')
        print('3. Add new employe')
        print('4. Delete employe')
        print('\n\n9. Return')
        print('0. Exit\n')

    @staticmethod
    def print_find_employee_menu():
        print('1. Add hours to employe')
        print('2. Show employe data')
        print('3. Show employe contact')
        print('4. Show employe salary')
        print('5. Edit employee')
        print('6. Edit employe contact')

        print('\n\n9. Return')
        print('0. Exit\n')   

    @staticmethod
    def print_edit_emp_menu():
        print('1. Edit name')
        print('2. Edit surname')
        print('3. Edit pesel')
        print('4. Edit birth date')
        print('5. Edit hire date')
        print('6. Edit department id')
        print('7. Edit title id')
        print('8. Edit value/hour')
        print('9. Return')
        print('0. Exit\n')

    @staticmethod
    def print_dept_menu():
        print('1. Show all departments')
        print('2. Add new department')
        print('3. Edit departments')