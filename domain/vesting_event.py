

class InvalidEventTypeException(Exception):
    pass


class VestingEvent:

    EVENT_TYPE_VEST = 'VEST'
    EVENT_TYPE_CANCEL = 'CANCEL'

    def __init__(self, event_type, employee, equity_award_id, date, shares_quantity):
        if event_type not in [VestingEvent.EVENT_TYPE_VEST, VestingEvent.EVENT_TYPE_CANCEL]:
            raise InvalidEventTypeException("invalid event type: {}".format(event_type))

        self.event_type = event_type
        self.employee = employee
        self.equity_award_id = equity_award_id
        self.date = date
        self.shares_quantity = shares_quantity
