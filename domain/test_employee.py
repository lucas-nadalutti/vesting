from unittest import TestCase

from domain.employee import Employee


class EmployeeTest(TestCase):

    def test_init(self):
        employee = Employee(employee_id="emp_id", name="Test Employee")
        self.assertEqual(employee.id, "emp_id")
        self.assertEqual(employee.name, "Test Employee")
