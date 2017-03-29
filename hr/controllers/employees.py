""" This is the controller of the /employees endpoint

The following functions are called from here: GET, POST, PATCH, and DELETE.
"""
import json
import os
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

    IMPLEMENTATION:
    1. Initialize the EmployeeResponse object
    2. Make request to database for all employees.
        2a. In the case that an employee_id is not None make the request to the database for all of 
            the employees who have have matching id's (Remember employee_id can contain multiple
            id's, not just 1)
    3. For each employee (<for employee in employees>)
        3a. create a new EmployeeApi object and fill in all of the appropriate information into it
            3aa. For things like salary, address, etc. only include the most recent information
                 into the EmployeeApi object
        3b. Add the EmployeeApi object into the EmployeeResponse object
    4. Return the EmployeeResponse object
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
                                        fname=employee_data_object.first_name,
                                        lname=employee_data_object.last_name,
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
                                        fname=employee_data_object.first_name,
                                        lname=employee_data_object.last_name,
                                        birth_date=employee_data_object.birth_date,
                                        address=addresses_data_object.to_str(),
                                        department=department_data_object.to_str(),
                                        role=title_data_object.to_str(),
                                        team_start_date=department_data_object.start_date,
                                        start_date=employee_data_object.start_date,
                                        salary=salary_data_object.to_str())
            collection.append(employee)

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
        # Include the following format into the description. Important to do some validation checking here!
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
    try:
        address = employee['address'].split(',')
        state_zip = address[2].split(' ')
        state_zip = ' '.join(state_zip[:2]), ' '.join(state_zip[2:])
        street_address = address[0]
        city = address[1]
        state = state_zip[0]
        address_zip = state_zip[1]
        address_date = datetime.strptime(employee['start_date'], '%Y-%m-%d').date()  # e.g. 2017-03-28
        session.add(Address(is_active=True, street_address=street_address, city=city, state=state, zip=address_zip,
                            start_date=address_date,
                            employee=new_employee))
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while importing employee address'}, 500

    # ADD DEPARTMENT
    try:
        team_start_date = datetime.strptime(employee['start_date'], '%Y-%m-%d').date()  # e.g. 2017-03-28
        session.add(Department(is_active=True, start_date=team_start_date, name=employee['department'],
                               employee=new_employee))
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while importing employee department'}, 500

    # ADD TITLE
    # Note: This should be the same as the team_start_date for POST'ing a new employee
    try:
        session.add(Title(is_active=True, name=employee['role'], start_date=team_start_date, employee=new_employee))
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while importing employee title'}, 500

    # ADD SALARY
    try:
        session.add(Salary(is_active=True, amount=randrange(50000, 100000, 1000), employee=new_employee))
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while importing employee salary'}, 500

    session.commit()

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
        session.query(Employee).filter_by(id=employee_id).delete()
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while deleting employee %s' % employee_id}, 500

    session.commit()
    session.close()

    return {'Magic': 'Magically making things vanish since 2017', 'employee_id': employee_id}, 200
