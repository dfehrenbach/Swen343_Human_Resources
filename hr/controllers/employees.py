def get(employee_id=None):
    return {'Magic': 'Im magic for get', 'employee_id': employee_id}


def post(employee):
    return {'Magic': 'Yes, actually magic #POST', 'employee': employee}


def patch(employee):
    return {'Magic': 'Magic, for patching things?', 'employee': employee}


def delete(employee_id):
    return {'Magic': 'Magically making things vanish since 2017', 'employee_id': employee_id}
