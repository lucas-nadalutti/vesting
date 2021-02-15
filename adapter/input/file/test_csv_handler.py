from decimal import Decimal
import os
from unittest import TestCase
from unittest.mock import MagicMock

from adapter.input.file.csv_handler import CsvHandler

TEST_FILES_DIR = "test_files"

class CsvHandlerTest(TestCase):

    def test_process_vesting_events(self):
        application_service = MagicMock()

        handler = CsvHandler(application_service)

        filepath = self.__get_filepath("success.csv")
        handler.process_vesting_events(filepath, "2050-01-01", 1)

        application_service.process.assert_called_once()

    def test_process_vesting_events_raises_exception_when_invalid_target_date(self):
        application_service = MagicMock()

        handler = CsvHandler(application_service)

        filepath = self.__get_filepath("success.csv")

        with self.assertRaises(Exception) as context:
            handler.process_vesting_events(filepath, "01-01-2050", 1)

        self.assertEqual(str(context.exception), "unexpected date format in target date 01-01-2050")

        application_service.process.assert_not_called()

    def test_process_vesting_events_raises_exception_when_row_contains_invalid_date(self):
        application_service = MagicMock()

        handler = CsvHandler(application_service)

        filepath = self.__get_filepath("invalid_date.csv")

        with self.assertRaises(Exception) as context:
            handler.process_vesting_events(filepath, "2050-01-01", 1)

        self.assertEqual(str(context.exception), "unexpected date format for date 2020-01-0 in row 1")

        application_service.process.assert_not_called()

    def test_process_vesting_events_raises_exception_when_row_contains_invalid_event_type(self):
        application_service = MagicMock()

        handler = CsvHandler(application_service)

        filepath = self.__get_filepath("invalid_event_type.csv")

        with self.assertRaises(Exception) as context:
            handler.process_vesting_events(filepath, "2050-01-01", 1)

        self.assertEqual(str(context.exception), "unexpected event type INVALID in row 8")

        application_service.process.assert_not_called()

    def __get_filepath(self, filename):
        test_files_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), TEST_FILES_DIR)
        return os.path.join(test_files_dir, filename)
