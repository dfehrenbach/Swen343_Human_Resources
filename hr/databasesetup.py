from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///hr.sqlite3', echo=True)
engine.connect()

Base = declarative_base()


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

    def __repr__(self):
        return "<Employee(id='%s', last='%s', first='%s', DOB='%s', isActive='%s')>" % (
            self.id, self.last_name, self.first_name, self.birth_date, self.is_active)


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
    start_date = Column(DateTime)
    is_active = Column(Boolean)
    name = Column(String(25))

    # Allows for reference to the employee object without search
    employee_id = Column(Integer, ForeignKey(Employee.id))
    employee = relationship("Employee", back_populates="departments")

    def __repr__(self):
        return "<Department(id='%s', employee_id='%s', start_date='%s', is_active='%s', " \
               "name='%s')>" % (self.id, self.employee_id, self.start_date, self.is_active, self.name)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    import datetime

    session = Session()
    session.add_all([
        Employee(is_active=True, first_name='Wendy', last_name='Williams', birth_date=datetime.date(1995, 4, 25)),
        # User(username='wwilliams', password='xxg527', ),

        Employee(is_active=False, first_name='Mary', last_name='Contrary', birth_date=datetime.date(1992, 2, 12))
    ])
    session.commit()
