""" This is the controller of the /employee endpoint

The following functions are called from here: GET
"""
from sqlalchemy.exc import SQLAlchemyError
from databasesetup import create_session, Employee
from models.employee_api_model import EmployeeApiModel
from models.employee_response import EmployeeResponse
from helpers.db_object_helper import get_all_children_objects
import logging

logging.basicConfig(filename='./log.txt',format='%(asctime)s :: %(name)s :: %(message)s')
logger = logging.getLogger(__name__)

def get(employee_id):
    """ This is the GET function that will return one or more employee objects within the system.
    :param employee_id:
    :return: a set of Employee Objects
    """
    session = create_session()

    try:
        employee_object = session.query(Employee).get(employee_id)
    except SQLAlchemyError:
        session.rollback()
        logger.error("Failed to retrieve employee number " + str(employee_id) + ". Invalid statement.")
        return {'error_message': 'Error while retrieving employee %s' % employee_id}, 500

    try:
        children = get_all_children_objects(employee_object)
    except AttributeError:
        logger.error("Get Employee: failed to retrieve employee number " + str(employee_id) + ". Employee does not exist.")
        return {'error_message': 'Error while retrieving employee %s' % employee_id}, 500
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

    session.close()
    logger.warning("Get Empolyee: Retrieved employee number " + str(employee_id) +
                " (Name: %s, Birth date: %s, Department: %s, role: %s)" %
                (employee_object.first_name + ' ' + employee_object.last_name,
                 employee_object.birth_date,
                 children['department'].to_str(),
                 children['title'].to_str()))
    return EmployeeResponse(employee).to_dict()
