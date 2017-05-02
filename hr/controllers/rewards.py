""" This is the controller of the /rewards endpoint

The following functions are called from here: GET, POST.
"""
import json
import os
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import exists, and_
from databasesetup import create_session, Employee
from models.employee_reward_api_model import EmployeeRewardApiModel
from models.employee_response import EmployeeResponse
import logging

logging.basicConfig(filename='./log.txt',format='%(asctime)s :: %(name)s :: %(message)s')
logger = logging.getLogger(__name__)


def get():
    session = create_session()
    employee_collection = []
    info = "Get Employees - Found the following employees - "

    try:
        if not session.query(Employee).first():
            session.rollback()
            logger.warning("Get Employees - No employees exist in the system")
            return {'error message': 'No employees exist in the system'}, 500

        all_employee_objects = session.query(Employee).all()

        for employee_object in all_employee_objects:
            employee = EmployeeRewardApiModel(employee_id=employee_object.id,
                                              name=employee_object.first_name + ' ' + employee_object.last_name,
                                              phones=employee_object.phones,
                                              orders=employee_object.orders)
            if employee_object.phones != 0 and employee_object.orders != 0:
                employee_collection.append(employee)

    except SQLAlchemyError:
        session.rollback()
        error_message = 'Error while retrieving all employee rewards'
        logger.warning("Employees.py Get - " + error_message)
        return {'error_message': error_message}, 500

    # CLOSE
    session.close()
    logger.warning(info)
    if not employee_collection:
        logger.warning("Get Employees - No employees that can receive rewards are in the system")
        return {'error message': 'No employees that can receive rewards are in the system'}, 500
    else:
        return EmployeeResponse(employee_collection).to_dict()


def post(payload):
    """
    :param payload:
    :return:

    1. check employee exists and grab it
    2. add information to that employee
    3. for each id in the array check for status from manufacturing
    4. if low/medium increment
    5. increment by 1.
    """
    return ""