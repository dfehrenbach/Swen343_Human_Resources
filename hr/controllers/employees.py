""" This is the controller of the /employees endpoint

The following functions are called from here: GET, POST, PATCH, and DELETE.
"""
import json
import os
import re
from datetime import datetime
from random import randrange
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import exists, and_
from databasesetup import create_session, Employee, User, Salary, Address, Title, Department
from models.employee_api_model import EmployeeApiModel
from models.employee_response import EmployeeResponse


def get(employee_id=None, static_flag=False):
    """ This is the GET function that will return one or more employee objects within the system.
    :param employee_id:
    :param static_flag:
    :return: a set of Employee Objects
    """
    if static_flag:
        scriptdir = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-2])
        sp_file = os.path.join(scriptdir, 'static/dummy.txt')
        obj = json.load(open(sp_file))

        if employee_id is not None and employee_id[0] < 3:
            return obj["employee_array"][employee_id[0]-1]
        return obj["employee_array"]

    session = create_session()
    addresses_data_object = None
    title_data_object = None
    department_data_object = None
    salary_data_object = None

    collection = []

    if employee_id is None:
        try:
            all_employee_object = session.query(Employee).all()
        except SQLAlchemyError:
            session.rollback()
            return {'error_message': 'Error while retrieving all employees'}, 500

        for employee_data_object in all_employee_object:
            for address_object in employee_data_object.addresses:
                if address_object.is_active:
                    addresses_data_object = address_object
                    break
            for title_object in employee_data_object.titles:
                if title_object.is_active:
                    title_data_object = title_object
                    break
            for department_object in employee_data_object.departments:
                if department_object.is_active:
                    department_data_object = department_object
                    break
            for salary_object in employee_data_object.salary:
                if salary_object.is_active:
                    salary_data_object = salary_object
                    break

            employee = EmployeeApiModel(is_active=employee_data_object.is_active,
                                        employee_id=employee_data_object.id,
                                        name=employee_data_object.first_name + ' ' + employee_data_object.last_name,
                                        birth_date=employee_data_object.birth_date,
                                        address=addresses_data_object.to_str(),
                                        department=department_data_object.to_str(),
                                        role=title_data_object.to_str(),
                                        team_start_date=department_data_object.start_date,
                                        start_date=employee_data_object.start_date,
                                        salary=salary_data_object.to_str())
            collection.append(employee)

    else:
        for e_id in employee_id:
            try:
                employee_data_object = session.query(Employee).get(e_id)
            except SQLAlchemyError:
                session.rollback()
                return {'error_message': 'Error while retrieving employee %s' % employee_id}, 500

            for address_object in employee_data_object.addresses:
                if address_object.is_active:
                    addresses_data_object = address_object
                    break
            for title_object in employee_data_object.titles:
                if title_object.is_active:
                    title_data_object = title_object
                    break
            for department_object in employee_data_object.departments:
                if department_object.is_active:
                    department_data_object = department_object
                    break
            for salary_object in employee_data_object.salary:
                if salary_object.is_active:
                    salary_data_object = salary_object
                    break

            employee = EmployeeApiModel(is_active=employee_data_object.is_active,
                                        employee_id=employee_data_object.id,
                                        name=employee_data_object.first_name + ' ' + employee_data_object.last_name,
                                        birth_date=employee_data_object.birth_date,
                                        address=addresses_data_object.to_str(),
                                        department=department_data_object.to_str(),
                                        role=title_data_object.to_str(),
                                        team_start_date=department_data_object.start_date,
                                        start_date=employee_data_object.start_date,
                                        salary=salary_data_object.to_str())
            collection.append(employee)

    # CLOSE
    session.close()

    return EmployeeResponse(collection).to_dict()


def post(employee):
    """
    :param employee:
    :return:
    """
    session = create_session()

    # ADD EMPLOYEE
    try:
        # Check if Employee Already exists
        if session.query(exists().where(and_(
                Employee.first_name == employee['fname'],
                Employee.last_name == employee['lname'],
                Employee.birth_date == datetime.strptime(employee['birth_date'], '%Y-%m-%d').date(),
                Employee.start_date == datetime.strptime(employee['start_date'], '%Y-%m-%d').date()))).scalar():
            session.rollback()
            return {'error_message':
                    'This employee already exists in the system. Please use PATCH to modify them or enter a new '
                    'employee. A new employee has a unique first name, last name, birth date, and start date'}, 500

        birthday = datetime.strptime(employee['birth_date'], '%Y-%m-%d').date()  # e.g. 1993-12-17
        start_date = datetime.strptime(employee['start_date'], '%Y-%m-%d').date()  # e.g. 2017-03-28
        new_employee = Employee(is_active=employee['is_active'], first_name=employee['fname'],
                                last_name=employee['lname'], birth_date=birthday, start_date=start_date)
        session.add(new_employee)
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while importing employee base'}, 500

    # ADD USER
    try:
        session.add(User(username='default', password='default', employee=new_employee))
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while importing employee user security information'}, 500

    # ADD ADDRESS
    # Use regex to check that the format is "00 StreetAddress St., City, State 11111"
    # Regex will help split these into groups too (rather than the silly split and joins I have)
    try:
        regex = r'^([\d]+[\s[a-zA-Z/.\u00C0-\u017F]+),([\s[a-zA-Z\u00C0-\u017F]+),([\s[a-zA-Z\u00C0-\u017F]+)\s([\d]+)$'
        regex_object = re.compile(regex)

        if not regex_object.match(employee['address']):
            return {'error_message': 'Address is formatted incorrectly. Instead, it needs to be formatted like so: '
                                     '(replace everything in <> with the appropriate value)', 
                    'address': {'format': '<Street Number> <Street Name> <Street Modifier if necessary>, '
                                          '<City>, <State> <Zipcode>',
                                'example': '12345 Example St., Example City, State 12345',
                                'provided': employee['address']}}, 500

        street_address = re.search(regex, employee['address']).group(1)
        city = re.search(regex, employee['address']).group(2)
        state = re.search(regex, employee['address']).group(3)
        address_zip = re.search(regex, employee['address']).group(4)
        address_date = datetime.strptime(employee['start_date'], '%Y-%m-%d').date()  # e.g. 2017-03-28
        session.add(Address(is_active=True, street_address=street_address, city=city, state=state, zip=address_zip,
                            start_date=address_date, employee=new_employee))
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while importing employee address'}, 500

    # ADD DEPARTMENT
    try:
        department_start_date = datetime.strptime(employee['start_date'], '%Y-%m-%d').date()  # e.g. 2017-03-28
        session.add(Department(is_active=True, start_date=department_start_date, name=employee['department'],
                               employee=new_employee))
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while importing employee department'}, 500

    # ADD TITLE
    # Note: This should be the same as the team_start_date for POST'ing a new employee
    try:
        session.add(Title(is_active=True, name=employee['role'], start_date=department_start_date,
                          employee=new_employee))
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while importing employee title'}, 500

    # ADD SALARY
    try:
        session.add(Salary(is_active=True, amount=randrange(50000, 100000, 1000), employee=new_employee))
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while importing employee salary'}, 500

    # COMMIT & CLOSE
    session.commit()
    session.close()

    return {'Magic': 'Yes, actually magic #POST', 'employee': employee}, 200


def patch(employee):
    """
    :param employee:
    :return:
    """
    session = create_session()

    return {'Magic': 'Magic, for patching things? Bipity Bop! You are now a frog!'
                     '(Not really, but the following employee has been changed!)', 'employee': employee}, 200


def delete(employee_id):
    """
    :param employee_id:
    :return:
    """
    session = create_session()

    try:
        if not session.query(exists().where(Employee.id == employee_id)).scalar():
            session.rollback()
            return {'error message': 'An employee with the id of %s does not exist' % employee_id}, 500
        employee = get(str(employee_id))
        session.query(Employee).filter_by(id=employee_id).delete()
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while deleting employee %s' % employee_id}, 500

    # COMMIT & CLOSE
    session.commit()
    session.close()

    return {'Magic': 'Magically making things vanish since 2017', 'deleted_employee': employee}, 200
