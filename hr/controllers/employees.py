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
from helpers.db_object_helper import \
    get_all_children_objects, get_active_address, \
    get_active_title, get_active_department, get_active_salary
from helpers.regex_helper import validate_address
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
    employee_collection = []

    if employee_id is None:
        try:
            if not session.query(Employee).first():
                session.rollback()
                return {'error message': 'No employees exist in the system'}, 500

            all_employee_objects = session.query(Employee).all()

            for employee_object in all_employee_objects:
                children = get_all_children_objects(employee_object)
                employee = EmployeeApiModel(is_active=employee_object.is_active,
                                            employee_id=employee_object.id,
                                            name=employee_object.first_name + ' ' + employee_object.last_name,
                                            birth_date=employee_object.birth_date,
                                            address=children['address'].to_str(),
                                            department=children['department'].to_str(),
                                            role=children['title'].to_str(),
                                            team_start_date=children['department'].start_date,
                                            start_date=employee_object.start_date,
                                            salary=children['salary'].to_str())
                employee_collection.append(employee)

        except SQLAlchemyError:
            session.rollback()
            return {'error_message': 'Error while retrieving all employees'}, 500

    else:
        for e_id in employee_id:
            try:
                if not session.query(exists().where(Employee.id == e_id)).scalar():
                    session.rollback()
                    return {'error message': 'An employee with the id of %s does not exist' % e_id}, 500

                employee_object = session.query(Employee).get(e_id)
                children = get_all_children_objects(employee_object)
                employee = EmployeeApiModel(is_active=employee_object.is_active,
                                            employee_id=employee_object.id,
                                            name=employee_object.first_name + ' ' + employee_object.last_name,
                                            birth_date=employee_object.birth_date,
                                            address=children['address'].to_str(),
                                            department=children['department'].to_str(),
                                            role=children['title'].to_str(),
                                            team_start_date=children['department'].start_date,
                                            start_date=employee_object.start_date,
                                            salary=children['salary'].to_str())
                employee_collection.append(employee)

            except SQLAlchemyError:
                session.rollback()
                return {'error_message': 'Error while retrieving employee %s' % employee_id}, 500

    # CLOSE
    session.close()

    return EmployeeResponse(employee_collection).to_dict()


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
    # Use regex to check that the format is "0200 StreetAddress St., City, State 11111"
    try:
        address = validate_address(employee['address'])
        address_date = datetime.strptime(employee['start_date'], '%Y-%m-%d').date()  # e.g. 2017-03-28
        session.add(Address(is_active=True, street_address=address['street_address'], city=address['city'],
                            state=address['state'], zip=address['zip'], start_date=address_date, employee=new_employee))
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

    try:
        # Check if Employee exists
        if not session.query(exists().where(Employee.id == employee['employee_id'])).scalar():
            return {'error_message': 'This employee does not exist in the system yet. '
                                     'Please use POST to add them as a new employee.'}, 500

        employee_object = session.query(Employee).get(employee['employee_id'])

        # MODIFY EMPLOYEE
        if 'is_active' in employee:
            employee_object.is_active = employee['is_active']
        if 'fname' in employee:
            employee_object.first_name = employee['fname']
        if 'lname' in employee:
            employee_object.last_name = employee['lname']
        if 'birth_date' in employee:
            employee_object.birth_date = datetime.strptime(employee['birth_date'], '%Y-%m-%d').date()
        if 'start_date' in employee:
            employee_object.start_date = datetime.strptime(employee['start_date'], '%Y-%m-%d').date()

    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while modifying employee base'}, 500

    # MODIFY USER
    try:
        if 'username' in employee:
            employee_object.user.username = employee['username']
        if 'password' in employee:
            employee_object.user.password = employee['password']

    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while modifying employee user security information'}, 500

    # MODIFY ADDRESS
    try:
        if 'address' or 'address_start_date' in employee:
            address_object = get_active_address(employee_object)

            if 'address' in employee:
                address = validate_address(employee['address'])
                address_object.is_active = False
                session.add(Address(is_active=True, street_address=address['street_address'], city=address['city'],
                                    state=address['state'], zip=address['zip'], employee=employee_object))

            if 'address_start_date' in employee:
                address_object.start_date = datetime.strptime(employee['address_start_date'], '%Y-%m-%d').date()

    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while modifying employee address'}, 500

    # MODIFY SALARY
    try:
        if 'salary' in employee:
            salary_object = get_active_salary(employee_object)
            salary_object.is_active = False
            session.add(Salary(is_active=True, amount=employee['salary'], employee=employee_object))
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while modifying employee salary'}, 500

    # MODIFY TITLE
    try:
        if 'role' or 'role_start_date' in employee:
            title_object = get_active_title(employee_object)

            if 'role' in employee:
                title_object.is_active = False
                now_date = datetime.strptime(str(datetime.now().year) + '-' +
                                             str(datetime.now().month) + '-' +
                                             str(datetime.now().day), '%Y-%m-%d').date()
                session.add(Title(is_active=True, name=employee['role'], start_date=now_date, employee=employee_object))

            if 'role_start_date' in employee:
                title_object.start_date = datetime.strptime(employee['role_start_date'], '%Y-%m-%d').date()

    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while modifying employee role & title'}, 500

    # MODIFY DEPARTMENT
    try:
        if 'department' or 'department_start_date' in employee:
            department_object = get_active_department(employee_object)

            if 'department' in employee:
                department_object.is_active = False
                now_date = datetime.strptime(str(datetime.now().year) + '-' +
                                             str(datetime.now().month) + '-' +
                                             str(datetime.now().day), '%Y-%m-%d').date()
                session.add(Department(is_active=True, name=employee['department'], start_date=now_date,
                                       employee=employee_object))

            if 'department_start_date' in employee:
                department_object.start_date = datetime.strptime(employee['department_start_date'], '%Y-%m-%d').date()

    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while modifying employee department & team'}, 500

    # COMMIT & CLOSE
    session.commit()
    session.close()

    return {'Magic': 'Magic, for patching things? Bipity Bop! You are now a frog!'
                     '(Not really, but the following employee has been changed!)', 'new_employee': employee}, 200


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
        employee = get(employee_id=[employee_id])
        session.query(Employee).filter_by(id=employee_id).delete()
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while deleting employee %s' % employee_id}, 500

    # COMMIT & CLOSE
    session.commit()
    session.close()
    return {'Magic': 'Magically making things vanish since 2017', 'deleted_employee': employee}, 200
