from sqlalchemy import (
    create_engine, Column, String, Integer, ForeignKey, Date,
    insert, select, and_, between, or_, join, func, text, bindparam
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime

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


    class Departments(BASE):
        __tablename__ = 'departments'
        department_id = Column(Integer, primary_key=True, autoincrement=True)
        dep_name = Column(String(30), nullable=False)
        from_date = Column(Date, nullable=True)
        to_date = Column(Date, nullable=True)

        emp = relationship('Employees', back_populates='department')
        titles = relationship('Titles', back_populates='department')

    class Titles(BASE):
        __tablename__ = 'titles'
        title_id = Column(Integer, primary_key=True, autoincrement=True)
        title_name = Column(String(30), nullable=True)
        from_date = Column(String(30), nullable=True)
        to_date = Column(String(30), nullable=True)

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

    def _add_salary(self, hours=0, per_hour=0, full_salary=0):
        new_salary = self.Salary(hours=hours, per_hour=per_hour, full_salary=full_salary)
        self._add_object(new_salary)
        return new_salary.salary_id

    def _add_contact(self, phone_number=None, email=None, street_and_no=None, flat_number=None):
        new_contact = self.Contacts(phone_number=phone_number, email=email,
                                    street_and_no=street_and_no, flat_number=flat_number)
        self._add_object(new_contact)
        return new_contact.contact_id


