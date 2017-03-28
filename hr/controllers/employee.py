""" This is the controller of the /employee endpoint

The following functions are called from here: GET
"""
def get(employee_id):
    """ This is the GET function that will return one or more employee objects within the system.
    :param employee_id:
    :return: a set of Employee Objects

    IMPLEMENTATION:
    1. Initialize the EmployeeResponse object
    2. Make request to database for all employees.
    3. For the employee
        3a. create a new EmployeeApi object and fill in all of the appropriate information into it
            3aa. For things like salary, address, etc. only include the most recent information into the EmployeeApi
                 object
        3b. Add the EmployeeApi object into the EmployeeResponse object
    4. Return the EmployeeResponse object
    """
    return {'Magic': 'Im magic for get', 'employee_id': employee_id}
