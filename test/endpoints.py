import unittest
from controllers import employee, employees
from hr.databasesetup import defaultInfo
import datetime
import os


class EndPointTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        defaultInfo()

    def test_getEmployee(self):
        mock_employee = {
            'employee_array':
                {
                    'name': 'Joseph Campione',
                    'team_start_date': datetime.date(2017, 1, 23),
                    'is_active': True,
                    'start_date': datetime.date(2017, 1, 23),
                    'role': 'Developer',
                    'department': 'Sales',
                    'salary': '83860',
                    'employee_id': 1,
                    'birth_date': datetime.date(1992, 2, 12),
                    'address': '0 Lomb Memorial Drive, Rochester, New York 14623'
                }
        }
        retrieved_employee = employee.get(1)
        self.assertEqual(retrieved_employee['employee_array']['name'],mock_employee['employee_array']['name'])

    def test_getEmployees(self):
        retrieved_employee = employees.get([1])
        mock_employee = {'employee_array':
            [
                {
                    'name': 'Joseph Campione',
                    'team_start_date': datetime.date(2017, 1, 23),
                    'is_active': True,
                    'start_date': datetime.date(2017, 1, 23),
                    'role': 'Developer',
                    'department': 'Sales',
                    'salary': '83860',
                    'employee_id': 1,
                    'birth_date': datetime.date(1992, 2, 12),
                    'address': '0 Lomb Memorial Drive, Rochester, New York 14623'
                }
            ]
        }
        self.assertEqual(retrieved_employee['employee_array'][0]['name'],mock_employee['employee_array'][0]['name'])
        retrieved_employees = employees.get([1,2])
        mock_employees = {'employee_array':
            [
                {
                    'name': 'Joseph Campione',
                    'start_date': datetime.date(2017, 1, 23),
                    'birth_date': datetime.date(1992, 2, 12),
                    'employee_id': 1,
                    'is_active': True,
                    'address': '0 Lomb Memorial Drive, Rochester, New York 14623',
                    'salary': '83860',
                    'team_start_date': datetime.date(2017, 1, 23),
                    'department': 'Sales',
                    'role': 'Developer'
                },
                {
                    'name': 'Matthew Chickering',
                    'start_date': datetime.date(2017, 1, 23),
                    'birth_date': datetime.date(1992, 2, 12),
                    'employee_id': 2,
                    'is_active': True,
                    'address': '1 Lomb Memorial Drive, Rochester, New York 14623',
                    'salary': '51943',
                    'team_start_date': datetime.date(2017, 1, 23),
                    'department': 'Manufacturing',
                    'role': 'Developer'
                }
            ]
        }
        self.assertEqual(retrieved_employees['employee_array'][0]['name'],mock_employees['employee_array'][0]['name'])
        self.assertEqual(retrieved_employees['employee_array'][1]['name'], mock_employees['employee_array'][1]['name'])

    def test_postEmployee(self):
        employee_to_post = {
            "address": "1 test dr, rochester, ny 14623",
            "birth_date": "2017-04-19",
            "department": "HR",
            "fname": "TEST",
            "is_active": True,
            "lname": "TEST",
            "role": "TEST",
            "start_date": "2017-04-19"
        }

        test = {
            'employee_array':
                [
                    {'birth_date': datetime.date(2017, 4, 19),
                     'is_active': True,
                     'department': 'HR',
                     'team_start_date': datetime.date(2017, 4, 19),
                     'role': 'TEST',
                     'salary': '72000',
                     'name': 'TEST TEST',
                     'employee_id': 33,
                     'address': '1 test dr,  rochester,  ny 14623',
                     'start_date': datetime.date(2017, 4, 19)
                     }
                ]
        }

        employees.post(employee_to_post)
        all_employees = employees.get()
        self.assertTrue(all_employees['employee_array'][-1], employee_to_post['fname'] + " " + employee_to_post['lname'])

    def test_patchEmployee(self):
        pass

    def test_deleteEmployee(self):
        pass

    # TODO get teardown to remove testDB.
    @classmethod
    def tearDownClass(cls):
        os.remove("hr.sqlite3")
        print("Things in current dir", os.listdir("."))
