from unittest import TestCase

from domain.employee import Employee
from domain.equity_award import EquityAward, NegativeVestedSharesException


class EquityAwardTest(TestCase):

    def test_init(self):
        employee = Employee(employee_id="emp_id", name="Test Employee")
        equity_award = EquityAward(award_id="awd_id", employee=employee)
        self.assertEqual(equity_award.id, "awd_id")
        self.assertEqual(equity_award.employee.id, "emp_id")
        self.assertEqual(equity_award.employee.name, "Test Employee")
        self.assertEqual(equity_award.vested_shares, 0)

    def test_vest_shares(self):
        employee = Employee(employee_id="emp_id", name="Test Employee")
        equity_award = EquityAward(award_id="awd_id", employee=employee)
        equity_award.vest_shares(100)
        equity_award.vest_shares(400)
        equity_award.vest_shares(1000)
        self.assertEqual(equity_award.vested_shares, 1500)

    def test_cancel_shares(self):
        employee = Employee(employee_id="emp_id", name="Test Employee")
        equity_award = EquityAward(award_id="awd_id", employee=employee)
        equity_award.vest_shares(100)
        equity_award.vest_shares(400)
        equity_award.cancel_shares(200)
        self.assertEqual(equity_award.vested_shares, 300)

    def test_get_vested_shares_return_0_when_negative(self):
        employee = Employee(employee_id="emp_id", name="Test Employee")
        equity_award = EquityAward(award_id="awd_id", employee=employee)
        equity_award.vest_shares(500)
        equity_award.cancel_shares(1000)
        self.assertEqual(equity_award.vested_shares, 0)
