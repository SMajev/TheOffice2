from sqlalchemy import (
    create_engine, Column, String, Integer, ForeignKey, Date,
    insert, select, and_, between, or_, join, func, text, bindparam
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import csv
import pandas as pd


class Database:
    BASE = declarative_base()

    class Employees(BASE):
        __tablename__ = 'employees'
        emp_id = Column(Integer, primary_key=True, autoincrement=True)
        emp_name = Column(String(40), nullable=False)
        emp_surname = Column(String(40), nullable=False)
        pesel = Column(String(40), nullable=False)
        birth_date = Column(Date, nullable=True)
        hire_date = Column(Date, nullable=True)
        contact_id = Column(Integer, ForeignKey('contacts.contact_id'))
        contact = relationship('Contacts', back_populates='emp')
        salary_id = Column(Integer(), ForeignKey('salaries.salary_id'))
        salary = relationship('Salary', back_populates='emp')
        department_id = Column(Integer(), ForeignKey('departments.department_id'))
        department = relationship('Departments', back_populates='emp')
        title_id = Column(Integer(), ForeignKey('titles.title_id'))
        title = relationship('Titles', back_populates='emp')

        def __repr__(self):
            return f'\n\n\nID: {self.emp_id}, Name: {self.emp_name}, Surname: {self.emp_surname},\n       Pesel:{self.pesel}\n\n\n'

    class Contacts(BASE):
        __tablename__ = 'contacts'
        contact_id = Column(Integer, primary_key=True, autoincrement=True)
        phone_number = Column(Integer, nullable=True)
        email = Column(String(40), nullable=True)
        street_and_no = Column(String(40), nullable=True)
        flat_number = Column(Integer, nullable=True)
        emp = relationship('Employees', back_populates='contact')


    class Salary(BASE):
        __tablename__ = 'salaries'
        salary_id = Column(Integer, primary_key=True, autoincrement=True)
        hours = Column(Integer, primary_key=True)
        per_hour = Column(Integer)
        full_salary = Column(Integer)
        emp = relationship('Employees', back_populates='salary')
        def __repr__(self):
            return f'salary_id'


    class Departments(BASE):
        __tablename__ = 'departments'
        department_id = Column(Integer, primary_key=True, autoincrement=True)
        dep_name = Column(String(30), nullable=False)

        emp = relationship('Employees', back_populates='department')
        titles = relationship('Titles', back_populates='department')

    class Titles(BASE):
        __tablename__ = 'titles'
        title_id = Column(Integer, primary_key=True, autoincrement=True)
        title_name = Column(String(30), nullable=True)


        emp = relationship('Employees', back_populates='title')

        department_id = Column(Integer(), ForeignKey('departments.department_id'), nullable=True)
        department = relationship('Departments', back_populates='titles')


    def __init__(self):
        self.engine = create_engine('mysql://root:JupyNote1234!@localhost:3306/theoffice2')
        self.BASE.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()


    def _add_object(self, object):
        self.session.add(object)
        self.session.commit()


    def add_employe(self, name: str, surname: str, pesel: str,
                    birth_date=None, hire_date=None, department_id=None, title_id=None):

        new_employe = self.Employees(
            emp_name=name, emp_surname=surname, pesel=pesel,
            birth_date=birth_date, hire_date=hire_date, contact_id=self._add_contact(),
            salary_id=self._add_salary(), department_id=department_id, title_id=title_id
        )        
        self._add_object(new_employe)


    def add_department(self, dep_name: str):
        new_department = self.Departments(dep_name=dep_name)
        self._add_object(new_department)


    def add_title(self, title_name: str, department_id: int):
        new_title = self.Titles(title_name=title_name, department_id=department_id)
        self._add_object(new_title)


    def edit_emp_name(self, emp_id: int, new_name: str):
        with self.session.begin():
            employe = self._search_by_id(emp_id)
            employe.emp_name = new_name


    def add_hour_to_salary(self, emp_id: int, number_of_hours: int):
        with self.session.begin():
            salary = self._search_salary_by_emp_id(emp_id)
            salary.hours += number_of_hours


    def edit_per_hour_value(self, emp_id: int, value):
        with self.session.begin():
            salary = self._search_salary_by_emp_id(emp_id)
            salary.per_hour = value


    def show_all_employees(self):
        df = self._get_data_frame('employees', 'emp_id')
        print(df)


    def monthly_reset(self):
        with self.session.begin():
            salaries = self._get_every_salary()
            print(salaries)
            self.save_data_to_csv('salaries', 'full_salary.csv', 'salary_id')
            for salary in salaries:
                print(salary)
                salary.hours = 0
                salary.full_salary = 0


    def count_full_salary_for_everyone(self):        
        with self.session.begin():
            salaries = self._get_every_salary()
            for salary in salaries:
                salary.full_salary = salary.hours * salary.per_hour


    def save_data_to_csv(self,  table_name, file_name, idx):
        df = self._get_data_frame(table_name, idx)
        df.to_csv(file_name)


    def edit_emp_surname(self, emp_id: int, new_surname: str):
        with self.session.begin():
            employe = self._search_by_id(emp_id)
            employe.emp_surname = new_surname


    def edit_emp_pesel(self, emp_id:int, new_pesel: str):
        with self.session.begin():
            employe = self._search_by_id(emp_id)
            employe.pesel = new_pesel


    def edit_emp_birth_date(self, emp_id: int, new_birth_date: str):
        with self.session.begin():
            employe = self._search_by_id(emp_id)
            employe.birth_date = new_birth_date


    def edit_emp_hire_date(self, emp_id: int, new_hire_date: str):
        with self.session.begin():
            employe = self._search_by_id(emp_id)
            employe.hire_date = new_hire_date


    def edit_emp_department_id(self, emp_id: int, new_department_id: int):
        with self.session.begin():
            employe = self._search_by_id(emp_id)
            employe.department_id = new_department_id


    def edit_emp_title_id(self, emp_id: int, new_title_id: int):
        with self.session.begin():
            employe = self._search_by_id(emp_id)
            employe.department_id = new_title_id


    def edit_phone_number(self, emp_id: int, new_phone_number: str):
        with self.session.begin():
            contact = self._search_contact_by_emp_id(emp_id)
            contact.phone_number = new_phone_number


    def edit_mail(self, emp_id: int, new_email: str):
        with self.session.begin():
            contact = self._search_contact_by_emp_id(emp_id)
            contact.email = new_email


    def edit_street_and_no(self, emp_id: int, new_adress: str):
        with self.session.begin():
            contact = self._search_contact_by_emp_id(emp_id)
            contact.street_and_no = new_adress


    def edit_flat_number(self, emp_id: int, new_flat_number: str):
        with self.session.begin():
            contact = self._search_contact_by_emp_id(emp_id)
            contact.flat_number = new_flat_number


    def edit_dept_name(self, dep_id: int, new_dept_name: str):
        with self.session.begin():
            dept = self._search_dept_by_id(dep_id)
            dept.dep_name = new_dept_name


    def edit_title_name(self, title_id: int, new_title_name: str):
        with self.session.begin():
            title = self._search_title_by_id(title_id)
            title.name = new_title_name


    def edit_title_dept(self, title_id: int, new_dept_id: int):
        with self.session.begin():
            title = self._search_title_by_id(title_id)
            title.department_id = new_dept_id

    def delete_employee(self, emp_id):
        with self.session.begin():
            try:
                self.session.delete(self._search_salary_by_emp_id(emp_id))
                self.session.delete(self._search_contact_by_emp_id(emp_id))
                self.session.delete(self._search_by_id(emp_id))
            except:
                print('Nie ma takiego rekordu')


    def _get_data_frame(self, table_name, idx):
        df = pd.read_sql_table(table_name, self.engine, index_col=idx)
        return df


    def _get_every_salary(self):
        salaries = self.session.query(self.Salary).all()
        return salaries


    def _add_salary(self, hours=0, per_hour=0, full_salary=0):
        new_salary = self.Salary(hours=hours, per_hour=per_hour, full_salary=full_salary)
        self._add_object(new_salary)
        return new_salary.salary_id


    def _add_contact(self, phone_number=None, email=None, street_and_no=None, flat_number=None):
        new_contact = self.Contacts(phone_number=phone_number, email=email,
                                    street_and_no=street_and_no, flat_number=flat_number)
        self._add_object(new_contact)
        return new_contact.contact_id


    def _search_by_id(self, id_to_find: int):
        try:        
            employe = (self.session.query(self.Employees)
                    .filter(self.Employees.emp_id == id_to_find).first())
            
            return employe
        except:
            print('Niepoprawne ID')
                  


    def _search_contact_by_emp_id(self, id_to_find: int):
        try:    
            contact_id = self._search_by_id(id_to_find).contact_id
            contact = (self.session.query(self.Contacts)
                    .filter(self.Contacts.contact_id == contact_id).first())
            return contact
        except:
            print('Niepoprawne ID')


    def _search_salary_by_emp_id(self, id_to_find: int):  
        try:
            salary_id = self._search_by_id(id_to_find).salary_id
            salary = (self.session.query(self.Salary)
                    .filter(self.Salary.salary_id == salary_id
                    ).first())
            return salary
        except:
            print('Niepoprawne ID')

    def _search_dept_by_id(self, id_to_find: int):
        dept = (self.session.query(self.Departments)
               .filter(self.Departments.department_id == id_to_find).first())
        return dept


    def _search_title_by_id(self, id_to_find: int):
        title = (self.session.query(self.Titles)
               .filter(self.Title.title_id == id_to_find).first())
        return title