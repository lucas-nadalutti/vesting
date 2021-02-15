import csv
from datetime import datetime
from decimal import Decimal

from application.vesting_event.command import ProcessVestingEventsCommand, VestingEventInput
from domain.vesting_event import VestingEvent


class CsvHandler:

    def __init__(self, vesting_event_service):
        self.vesting_event_service = vesting_event_service

    def process_vesting_events(self, filepath, target_date, precision_digits):

        try:
            datetime.strptime(target_date, "%Y-%m-%d")
        except ValueError:
            raise Exception("unexpected date format in target date {}".format(target_date))

        with open(filepath) as csv_file:
            rows = csv.reader(csv_file)
            inputs = [
                self.__parse_row(index, row) for index, row in enumerate(rows, start=1)
            ]
            command = ProcessVestingEventsCommand(target_date=target_date, precision_digits=int(precision_digits),
                                                  vesting_event_inputs=inputs)
            self.vesting_event_service.process(command)

    def __parse_row(self, index, row):
        if row[0] == VestingEvent.EVENT_TYPE_VEST:
            return self.__parse_vest_event(index, row)
        elif row[0] == VestingEvent.EVENT_TYPE_CANCEL:
            return self.__parse_cancel_event(index, row)
        else:
            raise Exception("unexpected event type {} in row {}".format(row[0], index))

    def __parse_vest_event(self, index, row):
        self.__validate_date(row[4], index)

        return VestingEventInput(
            event_type=row[0],
            employee_id=row[1],
            employee_name=row[2],
            equity_award_id=row[3],
            date=row[4],
            shares_quantity=Decimal(row[5]),
        )

    def __parse_cancel_event(self, index, row):
        self.__validate_date(row[3], index)

        return VestingEventInput(
            event_type=row[0],
            employee_id=row[1],
            equity_award_id=row[2],
            date=row[3],
            shares_quantity=Decimal(row[4]),
        )

    def __validate_date(self, date_value, index):
        try:
            datetime.strptime(date_value, "%Y-%m-%d")
        except ValueError:
            raise Exception("unexpected date format for date {} in row {}".format(date_value, index))
