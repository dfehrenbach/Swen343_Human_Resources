""" This is the controller of the /employees endpoint

The following functions are called from here: GET, POST, PATCH, and DELETE.
"""
import json
import os
from databasesetup import create_session, Employee
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
    
        if employee_id != None and employee_id[0] < 3:
            return obj["employee_array"][employee_id[0]-1]
        return obj["employee_array"]
        
    session = create_session()
    employee_data_object = None
    addresses_data_object = None
    title_data_object = None
    department_data_object = None
    salary_data_object = None

    collection = []

    if employee_id is None:
        all_employee_object = session.query(Employee).all()
        for employee_data_object in all_employee_object:
            # print employee_data_object
            for address_object in employee_data_object.addresses:
                if address_object.is_active:
                    addresses_data_object = address_object
            # print addresses_data_object
            for title_object in employee_data_object.titles:
                if title_object.is_active:
                    title_data_object = title_object
            # print title_data_object
            for department_object in employee_data_object.departments:
                if department_object.is_active:
                    department_data_object = department_object
            # print department_data_object
            for salary_object in employee_data_object.salary:
                if salary_object.is_active:
                    salary_data_object = salary_object
            # print salary_data_object

            employee = EmployeeApiModel(is_active=employee_data_object.is_active,
                                      employee_id=employee_data_object.id,
                                      fname=employee_data_object.first_name,
                                      lname=employee_data_object.last_name,
                                      birth_date=employee_data_object.birth_date,
                                      address=addresses_data_object,
                                      department=department_data_object,
                                      role=title_data_object.name,
                                      team_start_date=department_data_object.start_date,
                                      company_start_date=department_data_object.start_date,
                                      salary=salary_data_object.amount)
            collection.append(employee)

    else:
        for e_id in employee_id:
            employee_data_object = session.query(Employee).get(e_id)
            # print employee_data_object
            for address_object in employee_data_object.addresses:
                if address_object.is_active:
                    addresses_data_object = address_object
            # print addresses_data_object
            for title_object in employee_data_object.titles:
                if title_object.is_active:
                    title_data_object = title_object
            # print title_data_object
            for department_object in employee_data_object.departments:
                if department_object.is_active:
                    department_data_object = department_object
            # print department_data_object
            for salary_object in employee_data_object.salary:
                if salary_object.is_active:
                    salary_data_object = salary_object
            # print salary_data_object

            employee = EmployeeApiModel(is_active=employee_data_object.is_active,
                                      employee_id=employee_data_object.id,
                                      fname=employee_data_object.first_name,
                                      lname=employee_data_object.last_name,
                                      birth_date=employee_data_object.birth_date,
                                      address=addresses_data_object,
                                      department=department_data_object,
                                      role=title_data_object.name,
                                      team_start_date=department_data_object.start_date,
                                      company_start_date=department_data_object.start_date,
                                      salary=salary_data_object.amount)
            collection.append(employee)

    return EmployeeResponse(collection).to_dict()


def post(employee):
    """
    :param employee:
    :return:
    """
    return {'Magic': 'Yes, actually magic #POST', 'employee': employee}


def patch(employee):
    """
    :param employee:
    :return:
    """
    return {'Magic': 'Magic, for patching things?', 'employee': employee}


def delete(employee_id):
    """
    :param employee_id:
    :return:
    """
    return {'Magic': 'Magically making things vanish since 2017', 'employee_id': employee_id}
