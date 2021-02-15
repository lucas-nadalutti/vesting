from decimal import Decimal
from unittest import TestCase
from unittest.mock import MagicMock

from application.vesting_event.service import InvalidPrecisionDigitsException, VestingEventService
from application.vesting_event.command import ProcessVestingEventsCommand, VestingEventInput


class VestingEventServiceTest(TestCase):

    def test_process_vests(self):
        output_mock = MagicMock()

        service = VestingEventService(output=output_mock)

        inputs = [
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2020-01-01",
                shares_quantity=Decimal("1000"),
            ),
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2021-01-01",
                shares_quantity=Decimal("2000"),
            ),
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2022-01-01",
                shares_quantity=Decimal("5000"),
            ),
        ]
        command = ProcessVestingEventsCommand("2021-01-01", 1, inputs)
        service.process(command)

        output_mock.generate_vesting_schedule.assert_called_once()

        equity_awards_arg = output_mock.generate_vesting_schedule.call_args[0][0]
        self.assertEqual(equity_awards_arg[0].id, "awd_id")
        self.assertEqual(equity_awards_arg[0].vested_shares, Decimal("3000"))

    def test_process_vests_and_cancels(self):
        output_mock = MagicMock()

        service = VestingEventService(output=output_mock)

        inputs = [
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2020-01-01",
                shares_quantity=Decimal("1000"),
            ),
            VestingEventInput(
                event_type="CANCEL",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2021-01-01",
                shares_quantity=Decimal("500"),
            ),
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2022-01-01",
                shares_quantity=Decimal("5000"),
            ),
        ]
        command = ProcessVestingEventsCommand("2021-01-01", 1, inputs)
        service.process(command)

        output_mock.generate_vesting_schedule.assert_called_once()

        equity_awards_arg = output_mock.generate_vesting_schedule.call_args[0][0]
        self.assertEqual(equity_awards_arg[0].id, "awd_id")
        self.assertEqual(equity_awards_arg[0].vested_shares, Decimal("500"))

    def test_process_vests_and_cancels_with_cancels_higher_than_vests(self):
        output_mock = MagicMock()

        service = VestingEventService(output=output_mock)

        inputs = [
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2020-01-01",
                shares_quantity=Decimal("1000"),
            ),
            VestingEventInput(
                event_type="CANCEL",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2020-02-01",
                shares_quantity=Decimal("3000"),
            ),
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2020-03-01",
                shares_quantity=Decimal("500"),
            ),
        ]
        command = ProcessVestingEventsCommand("2021-01-01", 1, inputs)
        service.process(command)

        output_mock.generate_vesting_schedule.assert_called_once()

        equity_awards_arg = output_mock.generate_vesting_schedule.call_args[0][0]
        self.assertEqual(equity_awards_arg[0].id, "awd_id")
        self.assertEqual(equity_awards_arg[0].vested_shares, Decimal("0"))

    def test_process_vests_and_cancels_multiple_employees(self):
        output_mock = MagicMock()

        service = VestingEventService(output=output_mock)

        inputs = [
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2020-01-01",
                shares_quantity=Decimal("1000"),
            ),
            VestingEventInput(
                event_type="CANCEL",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2021-01-01",
                shares_quantity=Decimal("500"),
            ),
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id_2",
                employee_name="Test Employee 2",
                equity_award_id="awd_id_2",
                date="2020-01-01",
                shares_quantity=Decimal("2000"),
            ),
            VestingEventInput(
                event_type="CANCEL",
                employee_id="emp_id_2",
                employee_name="Test Employee 2",
                equity_award_id="awd_id_2",
                date="2020-06-01",
                shares_quantity=Decimal("700"),
            ),
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id_2",
                employee_name="Test Employee 2",
                equity_award_id="awd_id_2",
                date="2020-07-01",
                shares_quantity=Decimal("200"),
            ),
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id_3",
                employee_name="Test Employee 3",
                equity_award_id="awd_id_3",
                date="2020-02-01",
                shares_quantity=Decimal("3000"),
            ),
        ]
        command = ProcessVestingEventsCommand("2021-01-01", 1, inputs)
        service.process(command)

        output_mock.generate_vesting_schedule.assert_called_once()

        equity_awards_arg = output_mock.generate_vesting_schedule.call_args[0][0]
        equity_awards_arg.sort(key=lambda e: e.employee.id)
        self.assertEqual(equity_awards_arg[0].employee.id, "emp_id")
        self.assertEqual(equity_awards_arg[0].vested_shares, Decimal("500"))
        self.assertEqual(equity_awards_arg[1].employee.id, "emp_id_2")
        self.assertEqual(equity_awards_arg[1].vested_shares, Decimal("1500"))
        self.assertEqual(equity_awards_arg[2].employee.id, "emp_id_3")
        self.assertEqual(equity_awards_arg[2].vested_shares, Decimal("3000"))

    def test_process_raises_exception_when_invalid_precision_digits(self):
        output_mock = MagicMock()

        service = VestingEventService(output=output_mock)

        inputs = [
            VestingEventInput(
                event_type="VEST",
                employee_id="emp_id",
                employee_name="Test Employee",
                equity_award_id="awd_id",
                date="2020-01-01",
                shares_quantity=Decimal("1000"),
            )
        ]
        command = ProcessVestingEventsCommand("2021-01-01", 15, inputs)

        with self.assertRaises(InvalidPrecisionDigitsException):
            service.process(command)

        output_mock.generate_vesting_schedule.assert_not_called()
