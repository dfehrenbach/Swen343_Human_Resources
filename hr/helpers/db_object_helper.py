""" This aids with grabbing appropriate "active" child objects of a particular employee
"""


def get_all_children_objects(employee_object):
    """
    :param employee_object:
    :return: return dictionary of child objects with the following keys,
            address, title, department, salary
    """
    for address in employee_object.addresses:
        if address.is_active:
            addresses_object = address
            break
    for title in employee_object.titles:
        if title.is_active:
            title_object = title
            break
    for department in employee_object.departments:
        if department.is_active:
            department_object = department
            break
    for salary in employee_object.salary:
        if salary.is_active:
            salary_object = salary
            break

    return {'address': addresses_object, 'title': title_object,
            'department': department_object, 'salary': salary_object}


def get_active_address(employee_object):
    for address in employee_object.addresses:
        if address.is_active:
            addresses_object = address
            break
    return addresses_object


def get_active_title(employee_object):
    for title in employee_object.titles:
        if title.is_active:
            title_object = title
            break
    return title_object


def get_active_department(employee_object):
    for department in employee_object.departments:
        if department.is_active:
            department_object = department
            break
    return department_object


def get_active_salary(employee_object):
    for salary in employee_object.salary:
        if salary.is_active:
            salary_object = salary
            break
    return salary_object
