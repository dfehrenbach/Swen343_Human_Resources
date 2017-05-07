import logging
import requests

logging.basicConfig(filename='./log.txt',format='%(asctime)s :: %(name)s :: %(message)s')
logger = logging.getLogger(__name__)

employees_payload = requests.get("http://vm343a.se.rit.edu:80/employee")
employees = employees_payload.json()

# Number to divide annual employee salary by to get salary for a given time period
# Currently paying a biweekly salary
pay_period = 26

for employee in employees["employee_array"]:
    if employee["department"] != "Board":
        salary_request_body = { "amount" : employee["salary"]/pay_period, "department" : employee["department"],
                                "userID" : employee["employee_id"], "name" : employee["name"] }
        response = requests.post("http://vm343e.se.rit.edu/salary", salary_request_body)
        logger.info(response.text)