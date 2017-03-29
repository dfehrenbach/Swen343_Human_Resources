""" This is the controller of the /employee endpoint

The following functions are called from here: GET
"""
from sqlalchemy.exc import SQLAlchemyError
from databasesetup import create_session, Employee
from models.employee_api_model import EmployeeApiModel
from models.employee_response import EmployeeResponse


def get(employee_id):
    """ This is the GET function that will return one or more employee objects within the system.
    :param employee_id:
    :return: a set of Employee Objects
    """
    session = create_session()

    try:
        employee_data_object = session.query(Employee).get(employee_id)
    except SQLAlchemyError:
        session.rollback()
        return {'error_message': 'Error while retrieving employee %s' % employee_id}, 500

    addresses_data_object = None
    title_data_object = None
    department_data_object = None
    salary_data_object = None

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

    # Might want to include company_start_date as a column in the database
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

    session.close()
    return EmployeeResponse(employee).to_dict()
