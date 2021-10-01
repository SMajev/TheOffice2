from sqlalchemy import (
    create_engine, Column, String, 
    Integer, ForeignKey, insert, 
    select, and_, between,
    or_, join, func, text, DateTime
    )
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

ENGINE = create_engine('mysql://root:JupyNote1234!@localhost:3306/theoffice2')
base = declarative_base()
class Database:
    class Employees(base):
        __tablename__ = 'employees'
        emp_id = Column(Integer, primary_key=True, autoincrement=True)
        emp_name = Column(String(40), nullable=False)
        emp_surname = Column(String(40), nullable=False)
        pesel = Column(String(40), nullable=False)
        birth_date = Column(DateTime, nullable=True)
        hire_date = Column(DateTime, nullable=True)
        contact_id = Column(Integer, ForeignKey('contacts.contact_id'))
        contact = relationship('Contacts', back_populates='emp')
        salary_id = Column(Integer(), ForeignKey('salaries.salary_id'))
        salary = relationship('Salary', back_populates='emp')
        department_id = Column(Integer(), ForeignKey('departments.department_id'))
        department = relationship('Departments', back_populates='emp')
        title_id = Column(Integer(), ForeignKey('titles.title_id'))
        title = relationship('Titles', back_populates='emp')

    class Contacts(base):
        __tablename__ = 'contacts'
        contact_id = Column(Integer, primary_key=True, autoincrement=True)
        phone_number = Column(Integer, nullable=True)
        email = Column(String(40), nullable=True)
        street_and_no = Column(String(40), nullable=True)
        flat_number = Column(Integer, nullable=True)
        emp = relationship('Employees', back_populates='contact')


    class Salary(base):
        __tablename__ = 'salaries'
        salary_id = Column(Integer, primary_key=True, autoincrement=True)
        hours = Column(Integer, primary_key=True)
        per_hour = Column(Integer)
        full_salary = Column(Integer)
        emp = relationship('Employees', back_populates='salary')


    class Departments(base):
        __tablename__ = 'departments'
        department_id = Column(Integer, primary_key=True, autoincrement=True)
        dep_name = Column(String(30), nullable=False)
        from_date = Column(DateTime, nullable=True)
        to_date = Column(DateTime, nullable=True)

        emp = relationship('Employees', back_populates='department')
        titles = relationship('Titles', back_populates='department')

    class Titles(base):
        __tablename__ = 'titles'
        title_id = Column(Integer, primary_key=True, autoincrement=True)
        title_name = Column(String(30), nullable=True)
        from_date = Column(String(30), nullable=True)
        to_date = Column(String(30), nullable=True)

        emp = relationship('Employees', back_populates='title')

        department_id = Column(Integer(), ForeignKey('departments.department_id'), nullable=True)
        department = relationship('Departments', back_populates='titles')

base.metadata.create_all(ENGINE)
Session = sessionmaker(bind=ENGINE)
SESSION = Session()

