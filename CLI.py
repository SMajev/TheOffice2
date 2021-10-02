from TheOffice2_Database import Database
import pandas as pd
class CLI:
    def __init__(self):
        self.is_working = True
        self.db = Database()
        self.welcome()
        self.print_menu()
        self.main_loop()

    def main_loop(self):
        while self.is_working:
            option = self.ask_for_step()
            if option == 1:
                self.employees_menu_loop()
            elif option == 2:
                self.department_menu_loop()
            elif option == 3:
                self.title_menu_loop()
            elif option == 0:
                self.exit()

    def employees_menu_loop(self):
        self.print_employees_menu()
        option = self.ask_for_step()
        if option == 1:        
            employe = self.db._search_by_id(self.ask_for_id())
            print(employe)

            self.close_session()
            self.print_find_employee_menu()

            option = self.ask_for_step()
            if option == 1:
                number_of_hours = int(input('How many hours do you wanna add for employe: '))
                self.db.add_hour_to_salary(employe.salary_id, number_of_hours)
                self.employees_menu_loop()

            elif option == 2:
                print(self.db.pd_query_for_employee(employe.emp_id))

        elif option == 3:
            name, surname, pesel = self.get_new_user_data()
            self.db.add_employe(name=name, surname=surname, pesel=pesel)
        elif option == 9:
            self.main_loop()
        elif option == 0:
            self.exit()

    def close_session(self):
        self.db.session.close()

    def exit(self):
        self.is_qorking = False

    @staticmethod
    def ask_for_id():
        return int(input('ID: '))

    @staticmethod
    def ask_for_step():
        return int(input('Whera are we going?: '))

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
    def print_menu():
        print('MENU\n')
        print('1. Employees')
        print('2. Department')
        print('3. Titles')
        print('\n\n0. Exit')

    @staticmethod
    def print_employees_menu():
        print('1. Find employe')
        print('2. Add new employe')
        print('3. Delete employe')
        print('\n\n9. Return')
        print('0. Exit')

    @staticmethod
    def print_find_employee_menu():
        print('1. Add hours to employe')
        print('2. Show employe data')
        print('3. Show employe contact')
        print('4. Show employe salary')
        print('5. Edit employee')
        print('\n\n9. Return')
        print('0. Exit')   
