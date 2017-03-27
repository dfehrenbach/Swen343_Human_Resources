from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

def setUp():
    global engine
    engine = create_engine('sqlite:///hr.sqlite3', echo=True)
    engine.connect()
    global Base
    Base = declarative_base()

setUp()  # 'Base' and 'engine' need to be delcared gloablly, but inorder to test, the method needs to be accessable.

class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    last_name = Column(String(25))
    first_name = Column(String(25))
    birth_date = Column(DateTime)

    # This allows for reference to this employee's details without extra searching
    user = relationship("User", uselist=False, back_populates="employee")
    addresses = relationship("Address", back_populates="employee")
    titles = relationship("Title", back_populates="employee")
    departments = relationship("Department", back_populates="employee")
    salary = relationship("Salary", back_populates="employee")

    def __repr__(self):
        return "<Employee(id='%s', last='%s', first='%s', DOB='%s', isActive='%s')>" % (
            self.id, self.last_name, self.first_name, self.birth_date, self.is_active)

class Salary(Base):
    __tablename__ = 'salary'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    amount = Column(Integer) # Will be an Integer of Cents. So for a salary of $100, the amount will be 10000

    # This allows for reference to this employee's details without extra searching
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship("Employee", back_populates="salary")

    def __repr__(self):
        return "<Salary(id='%s', is_active='%s', amount='%s')>" % (self.id, self.is_active, self.amount)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25))
    password = Column(String(25))

    # Allows for reference to the employee object without search
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship("Employee", back_populates="user")

    def __repr__(self):
        return "<User(username='%s', password='%s', id='%s')>" % (
            self.username, self.password, self.id)


class Address(Base):
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    street_address = Column(String(50))
    city = Column(String(25))
    state = Column(String(25))
    zip = Column(String(5))
    start_date = Column(DateTime)

    # Allows for reference to the employee object without search
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship("Employee", back_populates="addresses")

    def __repr__(self):
        return "<Address(id='%s', is_active='%s', employee_id='%s', street_address='%s', city='%s', state='%s', " \
               "zip='%s', start_date='%s')>" % (self.id, self.is_active, self.employee_id, self.street_address,
                                                self.city, self.state, self.zip, self.start_date)


class Title(Base):
    __tablename__ = 'title'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    name = Column(String(25))
    start_date = Column(DateTime)

    # Allows for reference to the employee object without search
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship("Employee", back_populates="titles")

    def __repr__(self):
        return "<Title(id='%s', employee_id='%s', is_active='%s', name='%s', " \
               "start_date='%s')>" % (self.id, self.employee_id, self.is_active, self.name, self.start_date)


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    start_date = Column(DateTime)
    name = Column(String(25))

    # Allows for reference to the employee object without search
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship("Employee", back_populates="departments")

    def __repr__(self):
        return "<Department(id='%s', employee_id='%s', start_date='%s', is_active='%s', " \
               "name='%s')>" % (self.id, self.employee_id, self.start_date, self.is_active, self.name)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def main():
    import datetime

    session = Session()
    wendy_employee = Employee(is_active=True, first_name='Wendy', last_name='Williams',
                              birth_date=datetime.date(1995, 4, 25))
    session.add(wendy_employee)
    session.commit()

    mary_employee = Employee(is_active=False, first_name='Mary', last_name='Contrary',
                             birth_date=datetime.date(1992, 2, 12))
    session.add(mary_employee)
    session.commit()

    session.add(User(username='wwilliams', password='xxg527', employee=wendy_employee))
    session.add(User(username='mcontrary', password='asdf1234', employee=mary_employee))
    session.commit()

    session.add_all([
        Address(is_active=True, street_address="42 Wallaby Way", city="Rochester", state="New York", zip="14623",
                start_date=datetime.date(2016, 3, 23), employee=wendy_employee),
        Address(is_active=False, street_address="152 Wallingford Rd", city="Milford", state="New Hampshire",
                zip="03055", start_date=datetime.date(2006, 11, 10), employee=wendy_employee),

        Address(is_active=True, street_address="4 Forest Hills Dr", city="Nashua", state="New Hampshire", zip="03060",
                start_date=datetime.date(2014, 8, 23), employee=mary_employee),
        Address(is_active=False, street_address="42 Wallaby Way", city="Rochester", state="New York", zip="14623",
                start_date=datetime.date(1996, 5, 10), employee=mary_employee)
    ])
    session.commit()

    session.add_all([
        Title(is_active=True, name='HR Admin', start_date=datetime.date(2006, 11, 10), employee=wendy_employee),
        Title(is_active=True, name='HR Employee', start_date=datetime.date(1996, 5, 10), employee=mary_employee)
    ])
    session.commit()

    session.add_all([
        Department(is_active=True, start_date=datetime.date(2006, 11, 10), name='Human Resources',
                   employee=wendy_employee),
        Department(is_active=True, start_date=datetime.date(1996, 5, 10), name='Human Resources',
                   employee=mary_employee)
    ])
    session.commit()

if __name__ == "__main__":
    main()
