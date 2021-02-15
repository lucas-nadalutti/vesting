from decimal import Decimal, ROUND_DOWN

from domain.employee import Employee
from domain.equity_award import EquityAward
from domain.vesting_event import VestingEvent


class InvalidPrecisionDigitsException(Exception):
    pass


class VestingEventService:

    def __init__(self, output):
        self.output = output

    def process(self, command):
        if not 0 <= command.precision_digits <= 6:
            raise InvalidPrecisionDigitsException(
                "precision digits must be between 0 and 6, but was {}".format(command.precision_digits))

        vesting_events = self.assemble_vesting_events(command)
        equity_awards = self.assemble_equity_awards(vesting_events)
        self.output.generate_vesting_schedule(equity_awards)

    def assemble_vesting_events(self, command):
        vesting_events = []
        employees = {}
        for input in command.inputs:
            if input.date > command.target_date:
                continue

            if input.employee_id not in employees:
                employees[input.employee_id] = Employee(employee_id=input.employee_id, name=input.employee_name)
            employee = employees[input.employee_id]

            truncated_shares_quantity = input.shares_quantity.quantize(
                Decimal(str(10 ** -command.precision_digits)), rounding=ROUND_DOWN)
            vesting_event = VestingEvent(
                event_type=input.event_type,
                employee=employee,
                equity_award_id=input.equity_award_id,
                date=input.date,
                shares_quantity=truncated_shares_quantity,
            )
            vesting_events.append(vesting_event)

        return vesting_events

    def assemble_equity_awards(self, vesting_events):
        equity_awards = {}
        for vesting_event in vesting_events:
            if vesting_event.equity_award_id not in equity_awards:
                equity_awards[vesting_event.equity_award_id] = EquityAward(
                    award_id=vesting_event.equity_award_id,
                    employee=vesting_event.employee,
                    vested_shares=Decimal('0'),
                )
            equity_award = equity_awards[vesting_event.equity_award_id]

            if vesting_event.event_type == VestingEvent.EVENT_TYPE_VEST:
                equity_award.vest_shares(vesting_event.shares_quantity)
            elif vesting_event.event_type == VestingEvent.EVENT_TYPE_CANCEL:
                equity_award.cancel_shares(vesting_event.shares_quantity)

        return list(equity_awards.values())
