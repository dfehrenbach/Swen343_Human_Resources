""" This is the controller of the /confirm_login endpoint

The following functions are called from here: GET
"""
from sqlalchemy.exc import SQLAlchemyError
from databasesetup import create_session, Employee
from models.employee_api_model import EmployeeApiModel
from models.employee_response import EmployeeResponse
from helpers.db_object_helper import get_all_children_objects
import logging
import requests
import employees


logging.basicConfig(filename='./log.txt',format='%(asctime)s :: %(name)s :: %(message)s')
logger = logging.getLogger(__name__)

def get(department="",token=""):
    """ This is the GET function that will return an object with an employee id if they are authenticated.
    :param token:
    :return: an object with employee_id
    """

    response = requests.post('https://www.googleapis.com/oauth2/v3/tokeninfo',{'access_token': token})
    logger.info(response)
    if response.status_code == 200:
        email = response.json()["email"]
        emps = employees.get()
        for e in emps["employee_array"]:
            employee_department = e["department"].replace(" ","")
            if e["email"] == email and (employee_department == department or employee_department == "Board"):
                return {"employee_id": e["employee_id"]}
    return {'error_message': 'User is not authenticated'}, 400
