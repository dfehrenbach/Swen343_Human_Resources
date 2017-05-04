from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, class_mapper
import os
import logging
import random
import string

logging.basicConfig(filename='./log.txt',format='%(asctime)s :: %(name)s :: %(message)s')
logger = logging.getLogger(__name__)

logger.info("Creating database.")

password_file = open("pass.txt", 'r')
password = password_file.read().strip()
password_file.close()

file_name = "hr.myd"
engine = create_engine('mysql+mysqldb://root:' + password + '@localhost/343DB', echo=True)
engine.connect()
Base = declarative_base()

logger.info("Database Created.")


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    last_name = Column(String(25))
    first_name = Column(String(25))
    email = Collumn(String(50))
    birth_date = Column(Date)
    start_date = Column(Date)
    orders = Column(Integer)
    phones = Column(Integer)

    # This allows for reference to this employee's details without extra searching
    user = relationship("User", uselist=False, back_populates="employee", cascade="all, delete-orphan")
    addresses = relationship("Address", back_populates="employee", cascade="all, delete-orphan")
    titles = relationship("Title", back_populates="employee", cascade="all, delete-orphan")
    departments = relationship("Department", back_populates="employee", cascade="all, delete-orphan")
    salary = relationship("Salary", back_populates="employee", cascade="all, delete-orphan")

    def __repr__(self):
        return "<Employee(id='{0}', last='{1}', first='{2}', email='{5}', DOB='{4}', " \
               "company_start_date='{5}', isActive='{6}')>".format(self.id, self.last_name, self.first_name, self.email,
                                                                   self.birth_date, self.start_date, self.is_active)


class Salary(Base):
    __tablename__ = 'salary'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    amount = Column(Integer)  # Will be an Integer of Cents. So for a salary of $100, the amount will be 10000

    # This allows for reference to this employee's details without extra searching
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship("Employee", back_populates="salary")

    def __repr__(self):
        return "<Salary(id='%s', is_active='%s', amount='%s')>" % (self.id, self.is_active, self.amount)

    def to_str(self):
        return "%s" % self.amount


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
    start_date = Column(Date)

    # Allows for reference to the employee object without search
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship("Employee", back_populates="addresses")

    def __repr__(self):
        return "<Address(id='%s', is_active='%s', employee_id='%s', street_address='%s', city='%s', state='%s', " \
               "zip='%s', start_date='%s')>" % (self.id, self.is_active, self.employee_id, self.street_address,
                                                self.city, self.state, self.zip, self.start_date)

    def to_str(self):
        return "%s, %s, %s %s" % (self.street_address, self.city, self.state, self.zip)


class Title(Base):
    __tablename__ = 'title'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    name = Column(String(25))
    start_date = Column(Date)

    # Allows for reference to the employee object without search
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship("Employee", back_populates="titles")

    def __repr__(self):
        return "<Title(id='%s', employee_id='%s', is_active='%s', name='%s', " \
               "start_date='%s')>" % (self.id, self.employee_id, self.is_active, self.name, self.start_date)

    def to_str(self):
        return "%s" % self.name


class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    start_date = Column(Date)
    name = Column(String(25))

    # Allows for reference to the employee object without search
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship("Employee", back_populates="departments")

    def __repr__(self):
        return "<Department(id='%s', employee_id='%s', start_date='%s', is_active='%s', " \
               "name='%s')>" % (self.id, self.employee_id, self.start_date, self.is_active, self.name)

    def to_str(self):
        return "%s" % self.name


def create_session():
    return sessionmaker(bind=engine)()


def defaultInfo():
    Base.metadata.create_all(engine)

    import datetime

    session = create_session()

    names = [("Joseph", "Campione", "Sales", "Developer"), ("Matthew", "Chickering", "Manufacturing", "Developer"),
             ("Thomas", "DiMauro", "Inventory", "Developer"), ("Daniel", "Fehrenbach", "HR", "Developer"),
             ("Daniel", "Fisher", "Customer Support", "Developer"), ("Samuel", "Friedman", "HR", "Developer"),
             ("Joseph", "Gambino", "Manufacturing", "Developer"), ("Alexander", "Garrity", "Accounting", "Developer"),
             ("Quentin", "Goyert", "Manufacturing", "Developer"), ("Luke", "Harrold", "Inventory", "Developer"),
             ("George", "Herde", "Accounting", "Developer"), ("Paul", "Hulbert", "HR", "Developer"),
             ("Joseph", "Jankowiak", "Sales", "Developer"), ("Laura", "King", "Inventory", "Developer"),
             ("Melissa", "Laskowski", "Customer Support", "Developer"), ("Cailin", "Li", "Sales", "Developer"),
             ("Rafael", "Lopez", "Manufacturing", "Developer"), ("Junwen", "Mai", "Inventory", "Developer"),
             ("Corban", "Mailloux", "Customer Support", "Developer"), ("Shannon", "McIntosh", "Accounting", "Developer"),
             ("Joshua", "Miller", "Accounting", "Developer"), ("Samuel", "Mosher", "Inventory", "Developer"),
             ("Justin", "Nietzel", "Sales", "Developer"), ("Nathan", "Oesterle", "HR", "Developer"),
             ("Johnathan", "Sellers", "Manufacturing", "Developer"), ("Nicholas", "Swanson", "Sales", "Developer"),
             ("William", "Tarr", "Accounting", "Developer"), ("Jeremy", "Vargas", "HR", "Developer"),
             ("Bryon", "Wilkins", "Customer Support", "Developer"), ("Eric", "Yoon", "Customer Support", "Developer"),
             ("Daniel", "Krutz", "Board", "Board"), ("Silva", "Matti", "Board", "Board")]

    usernames = generateRandomProperties(len(names))
    passwords = generateRandomProperties(len(names))
    employee_count = 0

    for name in names:
        email = "{0}.{1}@krutz.site".format(name[0], name[1])
        employee = Employee(is_active=True, first_name=name[0], last_name=name[1], email=email, phones=0, orders=0,
                            birth_date=datetime.date(1992, 2, 12), start_date=datetime.date(2017, 1, 23))

        salary = 0
        if name[2] != "Board":
            salary = random.SystemRandom().randint(50000, 100000)

        session.add(employee)
        session.add(User(username=usernames[employee_count], password=passwords[employee_count], employee=employee))
        session.add(Address(is_active=True, street_address=str(employee_count) + " Lomb Memorial Drive", city="Rochester",
                            state="New York", zip="14623", start_date=datetime.date(2017, 1, 23), employee=employee))
        session.add(Title(is_active=True, name=name[3], start_date=datetime.date(2017, 1, 23), employee=employee))
        session.add(Department(is_active=True, start_date=datetime.date(2017, 1, 23), name=name[2],
                    employee=employee))
        session.add(Salary(is_active=True, amount=salary, employee=employee))
        session.commit()

        employee_count += 1

def generateRandomProperties(size):
    properties = []
    while len(properties) < size:
        rand_prop = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for i in range(8))
        if properties.count(rand_prop) < 1:
            properties.append(rand_prop)
    return properties

def serialize(model):
    """Transforms a model into a dictionary which can be dumped to JSON."""
    # first we get the names of all the columns on your model
    columns = [c.key for c in class_mapper(model.__class__).columns]
    # then we return their values in a dict
    return dict((c, getattr(model, c)) for c in columns)

logger.warning("Added default objects to database.")
print("Added all objects to database.")

if __name__ == "__main__":
    # Populate database if it is empty.  Set this to true to repopulate
    if False:
        defaultInfo()
