import json
import os
def get(employee_id=None):
    scriptdir = '/'.join(os.path.dirname(os.path.abspath(__file__)).split('/')[:-2])
    sp_file = os.path.join(scriptdir, 'static/dummy.txt')
    obj = json.load(open(sp_file))
    if employee_id != None and employee_id[0] < 3:
        return obj["employee_array"][employee_id[0]-1]
    return obj["employee_array"]


def post(employee):
    return {'Magic': 'Yes, actually magic #POST', 'employee': employee}


def patch(employee):
    return {'Magic': 'Magic, for patching things?', 'employee': employee}


def delete(employee_id):
    return {'Magic': 'Magically making things vanish since 2017', 'employee_id': employee_id}
