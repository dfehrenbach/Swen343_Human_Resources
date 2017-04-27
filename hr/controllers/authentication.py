""" This is the controller of the /confirm_login endpoint

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

def get(department="",token=""):
    """ This is the GET function that will return an object with an employee id if they are authenticated.
    :param token:
    :return: an object with employee_id
    """
    if token and department:
        return {"employee_id":0}
    return {'error_message': 'User is not authenticated'}, 400
