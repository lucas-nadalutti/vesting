from datetime import datetime
import os
import sys

from application.vesting_event.service import VestingEventService
from adapter.input.file.csv_handler import CsvHandler
from adapter.output.stdout.handler import StdoutHandler


FILES_DIR = "files"


def get_process_vesting_events_input():
    output = StdoutHandler()
    vesting_event_service = VestingEventService(output=output)
    return CsvHandler(vesting_event_service=vesting_event_service)


def process_vesting_events(filename, target_date, precision_digits):
    input = get_process_vesting_events_input()

    dirname = os.path.join(os.path.dirname(os.path.abspath(__file__)), FILES_DIR)
    filepath = os.path.join(dirname, filename)

    input.process_vesting_events(filepath, target_date, precision_digits)


if __name__ == "__main__":
    args = sys.argv

    try:
        filename = args[1]
    except IndexError:
        raise Exception('no file name was passed')

    try:
        target_date = args[2]
    except IndexError:
        raise Exception('no target date was passed')

    precision_digits = 0
    try:
        precision_digits = args[3]
    except IndexError:
        pass

    process_vesting_events(filename, target_date, precision_digits)
