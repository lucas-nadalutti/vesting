
class ProcessVestingEventsCommand:

    def __init__(self, target_date, precision_digits, vesting_event_inputs):
        self.target_date = target_date
        self.precision_digits = precision_digits
        self.inputs = vesting_event_inputs


class VestingEventInput:

    def __init__(self, event_type, employee_id, equity_award_id, date, shares_quantity, employee_name=None):
        self.event_type = event_type
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.equity_award_id = equity_award_id
        self.date = date
        self.shares_quantity = shares_quantity
