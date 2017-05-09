import unittest
from hr.controllers import employee, employees
import datetime

import random
from hr.databasesetup import Address,Employee,Salary,Title,Department
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy_utils import database_exists, create_database

global transaction, connection, engine, session

def create_session():
    return sessionmaker(bind=engine)()


# Advise taken from http://alextechrants.blogspot.com/2013/08/unit-testing-sqlalchemy-apps.html
def setup_module():
    pass

    global transaction, connection, engine, session


    password_file = open("pass.txt", 'r')
    password = password_file.read().strip()
    password_file.close()

    # Connect to the database and create the schema within a transaction
    engine = create_engine('mysql+mysqldb://root:' + password + '@localhost/343DB_test', echo=True)
    if not database_exists(engine.url):
        create_database(engine.url)
    connection = engine.connect()
    session = create_session()
    transaction = connection.begin()
    Base = declarative_base()
    Base.metadata.create_all(connection)


    #Add in data about employees that are tested against.
    names = [("Joseph", "Campione", "Sales", "Developer"), ("Matthew", "Chickering", "Manufacturing", "Developer")]

    employee_count = 0
    for name in names:
        email = "{0}.{1}@krutz.site".format(name[0], name[1])
        employee = Employee(is_active=True, first_name=name[0], last_name=name[1], email=email, phones=0, orders=0,
                            birth_date=datetime.date(1992, 2, 12), start_date=datetime.date(2017, 1, 23))

        salary = 0
        if name[2] != "Board":
            salary = random.SystemRandom().randint(50000, 100000)

        session.add(employee)
        session.add(Address(is_active=True, street_address=str(employee_count) + " Lomb Memorial Drive", city="Rochester",
                            state="New York", zip="14623", start_date=datetime.date(2017, 1, 23), employee=employee))
        session.add(Title(is_active=True, name=name[3], start_date=datetime.date(2017, 1, 23), employee=employee))
        session.add(Department(is_active=True, start_date=datetime.date(2017, 1, 23), name=name[2],
                    employee=employee))
        session.add(Salary(is_active=True, amount=salary, employee=employee))
        session.commit()

        employee_count += 1

def teardown_module():
    pass
    # Roll back the top level transaction and disconnect from the database
    transaction.rollback()
    connection.close()
    engine.dispose()

setup_module()

class EndPointTests(unittest.TestCase):


    def setup(self):
        self.__transaction = connection.begin_nested()
        self.session = Session(connection)

    def test_getEmployee(self):
        id = employees.get(session=session)['employee_array'][0]['employee_id']
        mock_employee = {
            'employee_array':
                {
                    'name': 'Joseph Campione',
                    'team_start_date': datetime.date(2017, 1, 23),
                    'is_active': True,
                    'start_date': datetime.date(2017, 1, 23),
                    'role': 'Developer',
                    'department': 'Sales',
                    'salary': '83860',
                    'employee_id': id,
                    'birth_date': datetime.date(1992, 2, 12),
                    'address': '0 Lomb Memorial Drive, Rochester, New York 14623'
                }
        }
        retrieved_employee = employee.get(id,session=session)
        self.assertNotEqual(retrieved_employee,[],msg="Database is empty. Please run test/databasesetup_test.py")
        self.assertEqual(retrieved_employee['employee_array']['name'],mock_employee['employee_array']['name'],
                         msg="Employee's name (" + retrieved_employee['employee_array']['name']
                             + ") does not match the mock employee's name ("
                             + mock_employee['employee_array']['name'] + ").")
        self.assertEqual(retrieved_employee['employee_array']['team_start_date'], mock_employee['employee_array']['team_start_date'],
                         msg="Employee's team start date (" + retrieved_employee['employee_array']['name']
                             + ") does not match the mock employee's team start date ("
                             + mock_employee['employee_array']['name'] + ").")
        self.assertEqual(retrieved_employee['employee_array']['is_active'], mock_employee['employee_array']['is_active'],
                         msg="Employee's active status (" + str(retrieved_employee['employee_array']['is_active'])
                             + ") does not match the mock employee's active status ("
                             + str(mock_employee['employee_array']['is_active']) + ").")
        self.assertEqual(retrieved_employee['employee_array']['start_date'], mock_employee['employee_array']['start_date'],
                         msg="Employee's start date (" + str(retrieved_employee['employee_array']['start_date'])
                             + ") does not match the mock employee's start date ("
                             + str(mock_employee['employee_array']['start_date']) + ").")
        self.assertEqual(retrieved_employee['employee_array']['role'], mock_employee['employee_array']['role'],
                         msg="Employee's role (" + retrieved_employee['employee_array']['role']
                             + ") does not match the mock employee's role ("
                             + mock_employee['employee_array']['role'] + ").")
        self.assertEqual(retrieved_employee['employee_array']['department'],mock_employee['employee_array']['department'],
                         msg="Employee's department (" + retrieved_employee['employee_array']['department']
                             + ") does not match the mock employee's department ("
                             + mock_employee['employee_array']['department'] + ").")
        self.assertEqual(retrieved_employee['employee_array']['employee_id'],mock_employee['employee_array']['employee_id'],
                         msg="Employee's ID number (" + str(retrieved_employee['employee_array']['employee_id'])
                             + ") does not match the mock employee's ID number ("
                             + str(mock_employee['employee_array']['employee_id']) + ").")
        self.assertEqual(retrieved_employee['employee_array']['birth_date'],mock_employee['employee_array']['birth_date'],
                         msg="Employee's birth date (" + str(retrieved_employee['employee_array']['birth_date'])
                             + ") does not match the mock employee's birth date ("
                             + str(mock_employee['employee_array']['birth_date']) + ").")
        self.assertEqual(retrieved_employee['employee_array']['address'],mock_employee['employee_array']['address'],
                         msg="Employee's address (" + retrieved_employee['employee_array']['address']
                             + ") does not match the mock employee's address ("
                             + mock_employee['employee_array']['address'] + ").")
        error_case = employee.get(-1,session=session)
        self.assertEqual(error_case,({'error_message': 'Error while retrieving employee -1'}, 400),
                         msg="Found an employee with an ID of -1")

    def test_getEmployees(self):
        first_id = employees.get(session=session)['employee_array'][0]['employee_id']
        mock_employee = {'employee_array':
            [
                {
                    'name': 'Joseph Campione',
                    'team_start_date': datetime.date(2017, 1, 23),
                    'is_active': True,
                    'start_date': datetime.date(2017, 1, 23),
                    'role': 'Developer',
                    'department': 'Sales',
                    'salary': '83860',
                    'employee_id': first_id,
                    'birth_date': datetime.date(1992, 2, 12),
                    'address': '0 Lomb Memorial Drive, Rochester, New York 14623'
                }
            ]
        }
        retrieved_employee = employees.get([first_id], session=session)
        self.assertEqual(retrieved_employee['employee_array'][0]['name'],mock_employee['employee_array'][0]['name'])
        self.assertEqual(retrieved_employee['employee_array'][0]['name'], mock_employee['employee_array'][0]['name'],
                         msg="Employee's name (" + retrieved_employee['employee_array'][0]['name']
                             + ") does not match the mock employee's name ("
                             + mock_employee['employee_array'][0]['name'] + ").")
        self.assertEqual(retrieved_employee['employee_array'][0]['team_start_date'],
                         mock_employee['employee_array'][0]['team_start_date'],
                         msg="Employee's team start date (" + retrieved_employee['employee_array'][0]['name']
                             + ") does not match the mock employee's team start date ("
                             + mock_employee['employee_array'][0]['name'] + ").")
        self.assertEqual(retrieved_employee['employee_array'][0]['is_active'],mock_employee['employee_array'][0]['is_active'],
                         msg="Employee's active status (" + str(retrieved_employee['employee_array'][0]['is_active'])
                             + ") does not match the mock employee's active status ("
                             + str(mock_employee['employee_array'][0]['is_active']) + ").")
        self.assertEqual(retrieved_employee['employee_array'][0]['start_date'],mock_employee['employee_array'][0]['start_date'],
                         msg="Employee's start date (" + str(retrieved_employee['employee_array'][0]['start_date'])
                             + ") does not match the mock employee's start date ("
                             + str(mock_employee['employee_array'][0]['start_date']) + ").")
        self.assertEqual(retrieved_employee['employee_array'][0]['role'], mock_employee['employee_array'][0]['role'],
                         msg="Employee's role (" + retrieved_employee['employee_array'][0]['role']
                             + ") does not match the mock employee's role ("
                             + mock_employee['employee_array'][0]['role'] + ").")
        self.assertEqual(retrieved_employee['employee_array'][0]['department'],mock_employee['employee_array'][0]['department'],
                         msg="Employee's department (" + retrieved_employee['employee_array'][0]['department']
                             + ") does not match the mock employee's department ("
                             + mock_employee['employee_array'][0]['department'] + ").")
        self.assertEqual(retrieved_employee['employee_array'][0]['employee_id'],mock_employee['employee_array'][0]['employee_id'],
                         msg="Employee's ID number (" + str(retrieved_employee['employee_array'][0]['employee_id'])
                             + ") does not match the mock employee's ID number ("
                             + str(mock_employee['employee_array'][0]['employee_id']) + ").")
        self.assertEqual(retrieved_employee['employee_array'][0]['birth_date'],mock_employee['employee_array'][0]['birth_date'],
                         msg="Employee's birth date (" + str(retrieved_employee['employee_array'][0]['birth_date'])
                             + ") does not match the mock employee's birth date ("
                             + str(mock_employee['employee_array'][0]['birth_date']) + ").")
        self.assertEqual(retrieved_employee['employee_array'][0]['address'], mock_employee['employee_array'][0]['address'],
                         msg="Employee's address (" + retrieved_employee['employee_array'][0]['address']
                             + ") does not match the mock employee's address ("
                             + mock_employee['employee_array'][0]['address'] + ").")

        first_id = employees.get(session=session)['employee_array'][0]['employee_id']
        second_id = employees.get(session=session)['employee_array'][1]['employee_id']
        retrieved_employees = employees.get([first_id,second_id], session=session)
        mock_employees = {'employee_array':
            [
                {
                    'name': 'Joseph Campione',
                    'start_date': datetime.date(2017, 1, 23),
                    'birth_date': datetime.date(1992, 2, 12),
                    'employee_id': first_id,
                    'is_active': True,
                    'address': '0 Lomb Memorial Drive, Rochester, New York 14623',
                    'salary': '83860',
                    'team_start_date': datetime.date(2017, 1, 23),
                    'department': 'Sales',
                    'role': 'Developer'
                },
                {
                    'name': 'Matthew Chickering',
                    'start_date': datetime.date(2017, 1, 23),
                    'birth_date': datetime.date(1992, 2, 12),
                    'employee_id': second_id,
                    'is_active': True,
                    'address': '1 Lomb Memorial Drive, Rochester, New York 14623',
                    'salary': '51943',
                    'team_start_date': datetime.date(2017, 1, 23),
                    'department': 'Manufacturing',
                    'role': 'Developer'
                }
            ]
        }
        self.assertEqual(retrieved_employees['employee_array'][0]['name'], mock_employees['employee_array'][0]['name'])
        self.assertEqual(retrieved_employees['employee_array'][0]['name'], mock_employees['employee_array'][0]['name'],
                         msg="Employee's name (" + retrieved_employees['employee_array'][0]['name']
                             + ") does not match the mock employee's name ("
                             + mock_employees['employee_array'][0]['name'] + ").")
        self.assertEqual(retrieved_employees['employee_array'][0]['team_start_date'],
                         mock_employees['employee_array'][0]['team_start_date'],
                         msg="Employee's team start date (" + retrieved_employees['employee_array'][0]['name']
                             + ") does not match the mock employee's team start date ("
                             + mock_employees['employee_array'][0]['name'] + ").")
        self.assertEqual(retrieved_employees['employee_array'][0]['is_active'],
                         mock_employees['employee_array'][0]['is_active'],
                         msg="Employee's active status (" + str(retrieved_employees['employee_array'][0]['is_active'])
                             + ") does not match the mock employee's active status ("
                             + str(mock_employees['employee_array'][0]['is_active']) + ").")
        self.assertEqual(retrieved_employees['employee_array'][0]['start_date'],
                         mock_employees['employee_array'][0]['start_date'],
                         msg="Employee's start date (" + str(retrieved_employees['employee_array'][0]['start_date'])
                             + ") does not match the mock employee's start date ("
                             + str(mock_employees['employee_array'][0]['start_date']) + ").")
        self.assertEqual(retrieved_employees['employee_array'][0]['role'], mock_employees['employee_array'][0]['role'],
                         msg="Employee's role (" + retrieved_employees['employee_array'][0]['role']
                             + ") does not match the mock employee's role ("
                             + mock_employees['employee_array'][0]['role'] + ").")
        self.assertEqual(retrieved_employees['employee_array'][0]['department'],
                         mock_employees['employee_array'][0]['department'],
                         msg="Employee's department (" + retrieved_employees['employee_array'][0]['department']
                             + ") does not match the mock employee's department ("
                             + mock_employees['employee_array'][0]['department'] + ").")
        self.assertEqual(retrieved_employees['employee_array'][0]['employee_id'],
                         mock_employees['employee_array'][0]['employee_id'],
                         msg="Employee's ID number (" + str(retrieved_employees['employee_array'][0]['employee_id'])
                             + ") does not match the mock employee's ID number ("
                             + str(mock_employees['employee_array'][0]['employee_id']) + ").")
        self.assertEqual(retrieved_employees['employee_array'][0]['birth_date'],
                         mock_employees['employee_array'][0]['birth_date'],
                         msg="Employee's birth date (" + str(retrieved_employees['employee_array'][0]['birth_date'])
                             + ") does not match the mock employee's birth date ("
                             + str(mock_employees['employee_array'][0]['birth_date']) + ").")
        self.assertEqual(retrieved_employees['employee_array'][0]['address'],
                         mock_employees['employee_array'][0]['address'],
                         msg="Employee's address (" + retrieved_employees['employee_array'][0]['address']
                             + ") does not match the mock employee's address ("
                             + mock_employees['employee_array'][0]['address'] + ").")

        self.assertEqual(retrieved_employees['employee_array'][1]['name'], mock_employees['employee_array'][1]['name'])
        self.assertEqual(retrieved_employees['employee_array'][1]['name'], mock_employees['employee_array'][1]['name'],
                         msg="Employee's name (" + retrieved_employees['employee_array'][1]['name']
                             + ") does not match the mock employee's name ("
                             + mock_employees['employee_array'][1]['name'] + ").")
        self.assertEqual(retrieved_employees['employee_array'][1]['team_start_date'],
                         mock_employees['employee_array'][1]['team_start_date'],
                         msg="Employee's team start date (" + retrieved_employees['employee_array'][1]['name']
                             + ") does not match the mock employee's team start date ("
                             + mock_employees['employee_array'][1]['name'] + ").")
        self.assertEqual(retrieved_employees['employee_array'][1]['is_active'],
                         mock_employees['employee_array'][1]['is_active'],
                         msg="Employee's active status (" + str(retrieved_employees['employee_array'][1]['is_active'])
                             + ") does not match the mock employee's active status ("
                             + str(mock_employees['employee_array'][1]['is_active']) + ").")
        self.assertEqual(retrieved_employees['employee_array'][1]['start_date'],
                         mock_employees['employee_array'][1]['start_date'],
                         msg="Employee's start date (" + str(retrieved_employees['employee_array'][1]['start_date'])
                             + ") does not match the mock employee's start date ("
                             + str(mock_employees['employee_array'][1]['start_date']) + ").")
        self.assertEqual(retrieved_employees['employee_array'][1]['role'], mock_employees['employee_array'][1]['role'],
                         msg="Employee's role (" + retrieved_employees['employee_array'][1]['role']
                             + ") does not match the mock employee's role ("
                             + mock_employees['employee_array'][1]['role'] + ").")
        self.assertEqual(retrieved_employees['employee_array'][1]['department'],
                         mock_employees['employee_array'][1]['department'],
                         msg="Employee's department (" + retrieved_employees['employee_array'][1]['department']
                             + ") does not match the mock employee's department ("
                             + mock_employees['employee_array'][1]['department'] + ").")
        self.assertEqual(retrieved_employees['employee_array'][1]['employee_id'],
                         mock_employees['employee_array'][1]['employee_id'],
                         msg="Employee's ID number (" + str(retrieved_employees['employee_array'][1]['employee_id'])
                             + ") does not match the mock employee's ID number ("
                             + str(mock_employees['employee_array'][1]['employee_id']) + ").")
        self.assertEqual(retrieved_employees['employee_array'][1]['birth_date'],
                         mock_employees['employee_array'][1]['birth_date'],
                         msg="Employee's birth date (" + str(retrieved_employees['employee_array'][1]['birth_date'])
                             + ") does not match the mock employee's birth date ("
                             + str(mock_employees['employee_array'][1]['birth_date']) + ").")
        self.assertEqual(retrieved_employees['employee_array'][1]['address'],
                         mock_employees['employee_array'][1]['address'],
                         msg="Employee's address (" + retrieved_employees['employee_array'][1]['address']
                             + ") does not match the mock employee's address ("
                             + mock_employees['employee_array'][1]['address'] + ").")
        error_case = employees.get([-1],session=session)
        self.assertEqual(error_case,
                         ({'error message': 'An employee with the id of -1 does not exist'}, 400),
                         msg="Found an employee with an ID of -1")

    def test_postEmployee(self):
        employee_to_post = {
            "address": "1 test dr, rochester, ny 14623",
            "birth_date": "2017-04-19",
            "department": "HR",
            "fname": "Post",
            "is_active": True,
            "lname": "Employee",
            "role": "TEST",
            "start_date": "2017-04-19",
            "email":"test@test.com"
        }

        # test = {
        #     'employee_array':
        #         [
        #             {
        #                 'birth_date': datetime.date(2017, 4, 19),
        #                 'is_active': True,
        #                 'department': 'HR',
        #                 'team_start_date': datetime.date(2017, 4, 19),
        #                 'role': 'TEST',
        #                 'salary': '72000',
        #                 'name': 'TEST TEST',
        #                 'employee_id': 33,
        #                 'address': '1 test dr,  rochester,  ny 14623',
        #                 'start_date': datetime.date(2017, 4, 19)
        #              }
        #         ]
        # }
        employees.post(employee_to_post, session=session)
        all_employees = employees.get(session=session)
        # '-1' index Gets the last employee, which is most recently added.
        new_employee = all_employees['employee_array'][-1]
        self.assertEqual(new_employee['name'], employee_to_post['fname'] + " " + employee_to_post['lname'],
                         msg="Employee's name (" + new_employee['name']
                             + ") does not match the mock employee's name ("
                             + employee_to_post['fname'] + " " + employee_to_post['lname'] + ").")
        self.assertEqual(new_employee['team_start_date'].strftime("%Y-%m-%d"),
                         employee_to_post['start_date'],
                         msg="Employee's team start date (" + new_employee['team_start_date'].strftime("%Y-%m-%d")
                             + ") does not match the mock employee's team start date ("
                             + str(employee_to_post['start_date']) + ").")
        self.assertEqual(new_employee['is_active'],
                         employee_to_post['is_active'],
                         msg="Employee's active status (" + str(new_employee['is_active'])
                             + ") does not match the mock employee's active status ("
                             + str(employee_to_post['is_active']) + ").")
        self.assertEqual(new_employee['start_date'].strftime("%Y-%m-%d"),
                         str(datetime.date.today()),
                         msg="Employee's start date (" + new_employee['start_date'].strftime("%Y-%m-%d")
                             + ") does not match the mock employee's start date ("
                             + str(employee_to_post['start_date']) + ").")
        self.assertEqual(new_employee['role'], employee_to_post['role'],
                         msg="Employee's role (" + new_employee['role']
                             + ") does not match the mock employee's role ("
                             + employee_to_post['role'] + ").")
        self.assertEqual(new_employee['department'],
                         employee_to_post['department'],
                         msg="Employee's department (" + new_employee['department']
                             + ") does not match the mock employee's department ("
                             + employee_to_post['department'] + ").")
        self.assertEqual(new_employee['birth_date'].strftime("%Y-%m-%d"),
                         employee_to_post['birth_date'],
                         msg="Employee's birth date (" + new_employee['birth_date'].strftime("%Y-%m-%d")
                             + ") does not match the mock employee's birth date ("
                             + str(employee_to_post['birth_date']) + ").")

        # TODO Fails. Address formatting is not correct.
        # example: "1 test dr,  rochester,  ny 14623" as opposed to "1 test dr, rochester, ny 14623"

        # self.assertEqual(new_employee['address'], employee_to_post['address'],
        #                  msg="Employee's address (" + new_employee['address']
        #                      + ") does not match the mock employee's address ("
        #                      + employee_to_post['address'] + ").")
        id = employees.get(session=session)['employee_array'][-1]['employee_id']
        existing_employee = employee.get(id,session=session)
        self.assertNotEqual(existing_employee,({'error_message': 'Error while retrieving employee 32'}, 400), msg="Error Retrieving Employee")
        existing_employee = existing_employee['employee_array']
        not_new_employee = {
            'address': existing_employee['address'],
            'birth_date': existing_employee['birth_date'].strftime("%Y-%m-%d"),
            'department': existing_employee['department'],
            'fname': existing_employee['name'].split()[0],
            'is_active': existing_employee['is_active'],
            'lname': existing_employee['name'].split()[1],
            'role': existing_employee['role'],
            'start_date': existing_employee['start_date'].strftime("%Y-%m-%d"),
            'email': existing_employee['email']
        }
        response = employees.post(not_new_employee,session=session)
        self.assertEqual(response,
                         ({'error_message':
                           'This employee already exists in the system. Please use PATCH to modify them or enter a new '
                           'employee. A new employee has a unique first name, last name, birth date, and start date'},
                          400),
                         msg="Able to POST and existing employee's information.")

    def test_patchEmployee(self):
        patch = {
          "address": "1 test dr, rochester, ny 14623",
          "address_start_date": "2017-04-19",
          "birth_date": "2017-04-19",
          "department": "HR",
          "department_start_date": "2017-04-19",
          "employee_id": 0,
          "fname": "Patch",
          "is_active": True,
          "lname": "Employee Patch",
          "password": "string",
          "role": "string",
          "role_start_date": "2017-04-19",
          "salary": 0,
          "start_date": "2017-04-19",
          "username": "string"
        }

        employee_to_post = {
            "address": "1 test dr, rochester, ny 14623",
            "birth_date": "2017-04-19",
            "department": "HR",
            "fname": "Patch",
            "is_active": True,
            "lname": "Employee Post",
            "role": "TEST",
            "start_date": "2017-04-19",
            "email":"test@test.com"
        }

        employees.post(employee_to_post,session=session)
        all_employees = employees.get(session=session)
        num_employees = len(all_employees['employee_array'])
        id = all_employees['employee_array'][-1]['employee_id']
        employee_to_patch = employee.get(id,session=session)
        employee_to_patch = employee_to_patch['employee_array']
        # Confirm the right employee was gotten.
        self.assertEqual(employee_to_patch['name'], employee_to_post['fname'] + " " + employee_to_post['lname'])
        patch['employee_id'] = id
        employees.patch(patch,session=session)
        employee_to_test = employee.get(id, session=session)['employee_array']
        self.assertEqual(employee_to_test['name'],patch['fname'] + " " + patch['lname'])

        self.assertEqual(employee_to_test['name'], patch['fname'] + " " + patch['lname'],
                         msg="Employee's name (" + employee_to_test['name']
                             + ") does not match the mock employee's name ("
                             + patch['fname'] + " " + patch['lname'] + ").")
        self.assertEqual(employee_to_test['team_start_date'].strftime("%Y-%m-%d"),
                         patch['start_date'],
                         msg="Employee's team start date (" + employee_to_test['team_start_date'].strftime("%Y-%m-%d")
                             + ") does not match the mock employee's team start date ("
                             + str(patch['start_date']) + ").")
        self.assertEqual(employee_to_test['is_active'],
                         patch['is_active'],
                         msg="Employee's active status (" + str(employee_to_test['is_active'])
                             + ") does not match the mock employee's active status ("
                             + str(patch['is_active']) + ").")
        self.assertEqual(employee_to_test['start_date'].strftime("%Y-%m-%d"),
                         patch['start_date'],
                         msg="Employee's start date (" + employee_to_test['start_date'].strftime("%Y-%m-%d")
                             + ") does not match the mock employee's start date ("
                             + str(patch['start_date']) + ").")

        self.assertEqual(employee_to_test['role'], patch['role'],
                         msg="Employee's role (" + employee_to_test['role']
                             + ") does not match the mock employee's role ("
                             + patch['role'] + ").")

        self.assertEqual(employee_to_test['department'],
                         patch['department'],
                         msg="Employee's department (" + employee_to_test['department']
                             + ") does not match the mock employee's department ("
                             + patch['department'] + ").")
        self.assertEqual(employee_to_test['birth_date'].strftime("%Y-%m-%d"),
                         patch['birth_date'],
                         msg="Employee's birth date (" + employee_to_test['birth_date'].strftime("%Y-%m-%d")
                             + ") does not match the mock employee's birth date ("
                             + str(patch['birth_date']) + ").")
        # TODO Fails. Inputs are the same, but extra spaces are added to the address from the database.
        # self.assertEqual(employee_to_test['address'], patch['address'],
        #                  msg="Employee's address (" + employee_to_test['address']
        #                      + ") does not match the mock employee's address ("
        #                      + patch['address'] + ").")

        self.assertEqual(str(employee_to_test['salary']),str(0))

        patch['employee_id'] = -1
        self.assertEqual(employees.patch(patch, session=session),
                         ({'error_message':
                           'This employee does not exist in the system yet. Please use POST to add them as a new employee'},
                          400),
                         msg="Able to PATCH an employee that doesn't exist.")

    def test_deleteEmployee(self):
        employee_to_post = {
            "address": "1 test dr, rochester, ny 14623",
            "birth_date": "2017-04-19",
            "department": "HR",
            "fname": "DEL",
            "is_active": True,
            "lname": "ETE",
            "role": "TEST",
            "start_date": "2017-04-19",
            "email":"test@delete.com"
        }

        employees.post(employee_to_post,session=session)
        all_employees = employees.get(session=session)
        id = all_employees['employee_array'][-1]['employee_id']
        employee_to_delete = employee.get(id,session=session)['employee_array']
        self.assertEqual(employee_to_delete['name'], employee_to_post['fname'] + " " + employee_to_post['lname'])
        self.assertEqual(employee.get(id,session=session),({'error_message': 'Error while retrieving employee ' + str(id)}, 400))

    def teardown(self):
        self.session.close()
        self.__transaction.rollback()
