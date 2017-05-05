""" This is the controller of the /rewards endpoint

The following functions are called from here: GET, POST.
"""
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import exists
from databasesetup import create_session, Employee
from models.employee_reward_api_model import EmployeeRewardApiModel
from models.employee_response import EmployeeResponse
import requests
import logging

logging.basicConfig(filename='./log.txt', format='%(asctime)s :: %(name)s :: %(message)s')
logger = logging.getLogger(__name__)


def get():
    session = create_session()
    employee_collection = []
    info = "Get Employees - Found the following employees - "

    try:
        if not session.query(Employee).first():
            session.rollback()
            logger.warning("Get Employees - No employees exist in the system")
            return {'error message': 'No employees exist in the system'}, 400

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
        return {'error_message': error_message}, 400

    # CLOSE
    session.close()
    logger.warning(info)
    if not employee_collection:
        logger.warning("Get Employees - No employees that can receive rewards are in the system")
        return {'error message': 'No employees that can receive rewards are in the system'}, 400
    else:
        return EmployeeResponse(employee_collection).to_dict(), 200


def post(employee):
    """
    :param employee:
    :return:

    1. check employee exists and grab it
    2. add information to that employee
    3. for each id in the array check for status from manufacturing
    4. if low/medium increment
    5. increment by 1.
    """
    session = create_session()

    try:
        # Check if Employee exists
        if not session.query(exists().where(Employee.id == employee['employeeId'])).scalar():
            error_message = 'This employee does not exist in the system yet. ' \
                            'Please use employees POST to add them as a new employee'
            logger.warning("rewards.py POST - "
                           "The employee does not exist in the system")
            return {'error_message': error_message}, 400

        employee_object = session.query(Employee).get(employee['employeeId'])
        if employee['replace']:
            return {'message': 'No rewards were counted for the employee {0}'.format(employee['employeeId'])}
        else:
            for serial_id in employee['serialIds']:
                try:
                    phone_payload = requests.get("http://vm343b.se.rit.edu:5000/inventory/phones/{0}".format(str(serial_id)))
                    phone = phone_payload.json()
                except:
                    session.rollback()
                    error_message = 'Error while information from inventory with phone_serial_id: {0}'.format(str(serial_id))
                    logger.warning(error_message)
                    return {'error_message': error_message}, 400

                if phone[0]['fields']['modelId'] == 2 or phone[0]['fields']['modelId'] == 3:
                    employee_object.phones += + 1
            employee_object.orders += 1

    except:
        session.rollback()
        error_message = 'Error while modifying employee base in rewards.py'
        logger.warning("rewards.py employees POST - "
                       "Error while modifying the employee:")
        return {'error_message': error_message}, 400

    return_message = "Employee {0}'s count for phones has incremented now is {1} and now has {2} " \
                     "eligible orders".format(employee['employeeId'], employee_object.phones, employee_object.orders)

    session.commit()
    session.close()
    return {'message': return_message}, 200
