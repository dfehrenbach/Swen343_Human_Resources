""" This is the controller of the /employees endpoint

The following functions are called from here: GET, POST, PATCH, and DELETE.
"""
def get(employee_id=None):
    """ This is the GET function that will return one or more employee objects within the system.
    :param employee_id:
    :return: a set of Employee Objects

    IMPLEMENTATION:
    1. Initialize the EmployeeResponse object
    2. Make request to database for all employees.
        2a. In the case that an employee_id is not None make the request to the database for all of the employees who have
            have matching id's (Remember employee_id can contain multiple id's, not just 1)
    3. For each employee (<for employee in employees>)
        3a. create a new EmployeeApi object and fill in all of the appropriate information into it
            3aa. For things like salary, address, etc. only include the most recent information into the EmployeeApi
                 object
        3b. Add the EmployeeApi object into the EmployeeResponse object
    4. Return the EmployeeResponse object
    """
    return {'Magic': 'Im magic for get', 'employee_id': employee_id}


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
