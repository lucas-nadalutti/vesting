from unittest import TestCase

from domain.employee import Employee
from domain.vesting_event import InvalidEventTypeException, VestingEvent


class VestingEventTest(TestCase):

    def test_init(self):
        employee = Employee(employee_id="emp_id", name="Test Employee")
        vesting_event = VestingEvent(
            event_type=VestingEvent.EVENT_TYPE_VEST,
            employee=employee,
            equity_award_id="awd_id",
            date="2050-01-01",
            shares_quantity=1000,
        )
        self.assertEqual(vesting_event.employee.id, "emp_id")
        self.assertEqual(vesting_event.employee.name, "Test Employee")
        self.assertEqual(vesting_event.equity_award_id, "awd_id")
        self.assertEqual(vesting_event.date, "2050-01-01")
        self.assertEqual(vesting_event.shares_quantity, 1000)

    def test_init_raises_exception_when_invalid_type(self):
        employee = Employee(employee_id="emp_id", name="Test Employee")

        with self.assertRaises(InvalidEventTypeException):
            VestingEvent(
                event_type="INVALID",
                employee=employee,
                equity_award_id="awd_id",
                date="2050-01-01",
                shares_quantity=1000,
            )
