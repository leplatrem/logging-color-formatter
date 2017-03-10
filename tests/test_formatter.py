import re
import unittest

import mock

from logging_color_formatter import ColorFormatter


def strip_ansi(text):
    """
    Strip ANSI sequences (colors) from text.
    Source: http://stackoverflow.com/a/15780675
    """
    SEQUENCES = r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?'
    return re.sub(SEQUENCES, '', text)


class ColorFormatterTest(unittest.TestCase):
    def setUp(self):
        self.formatter = ColorFormatter()

    def test_output_is_serialized_as_string(self):
        value = self.formatter.format(mock.MagicMock())
        self.assertIsInstance(value, str)

    def test_output_is_simple_if_no_request_is_bound(self):
        value = self.formatter.format(mock.MagicMock())
        self.assertNotIn('? ms', value)

    def test_values_are_defaulted_to_question_mark(self):
        record = mock.MagicMock()
        record.path = '/'
        value = self.formatter.format(record)
        self.assertIn('? ms', value)

    def test_querystring_is_rendered_as_string(self):
        record = mock.MagicMock()
        record.path = '/'
        record.querystring = {'param': 'val'}
        value = self.formatter.format(record)
        self.assertIn('/?param=val', value)

    def test_extra_event_infos_is_rendered_as_key_values(self):
        record = mock.MagicMock()
        record.nb_records = 5
        value = self.formatter.format(record)
        self.assertIn('nb_records=5', strip_ansi(value))

    def test_every_event_dict_entry_appears_in_log_message(self):
        record = mock.MagicMock()
        record.__dict__ = {
            'msg': 'Pouet',
            'method': 'GET',
            'path': '/v1/',
            'querystring': {'_sort': 'field'},
            'code': 200,
            't': 32,
            'event': 'app.event',
            'nb_records': 5
        }
        value = self.formatter.format(record)
        self.assertEqual(('"GET   /v1/?_sort=field" 200 (32 ms)'
                          ' Pouet event=app.event nb_records=5'), strip_ansi(value))

    def test_fields_values_support_unicode(self):
        record = mock.MagicMock()
        record.value = '\u2014'
        value = self.formatter.format(record)
        self.assertIn('\u2014', value)