""" This is the controller of the /rewards endpoint

The following functions are called from here: GET, POST.
"""
import json
import os
from datetime import datetime
from random import randrange
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import exists, and_
from databasesetup import create_session, Employee, User, Salary, Address, Title, Department
from helpers.db_object_helper import \
    get_all_children_objects, get_active_address, \
    get_active_title, get_active_department, get_active_salary
from helpers.regex_helper import validate_address
from models.employee_api_model import EmployeeApiModel
from models.employee_response import EmployeeResponse
import logging

logging.basicConfig(filename='./log.txt',format='%(asctime)s :: %(name)s :: %(message)s')
logger = logging.getLogger(__name__)

def get():


def post():