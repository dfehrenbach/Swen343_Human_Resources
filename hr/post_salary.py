import logging
import requests

logging.basicConfig(filename='./log.txt',format='%(asctime)s :: %(name)s :: %(message)s')
logger = logging.getLogger(__name__)

employees_payload = requests.get("http://vm343a.se.rit.edu:8080/employee")
employees = employees_payload.json()

for employee in employees["employee_array"]:
    salary_request_body = { "Amount" : employee["salary"], "Department" : employee["department"], "UserID" :
        employee["employee_id"], "Name" : employee["name"] }
    response = requests.post("http://vm343e.se.rit.edu/salary", salary_request_body)
    logger.info(response.text)