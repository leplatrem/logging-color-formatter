import logging
import re
import unittest
from io import StringIO

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
        self.record = mock.MagicMock()
        self.record.exc_info = self.record.stack_info = None

    def test_output_is_serialized_as_string(self):
        value = self.formatter.format(self.record)
        self.assertIsInstance(value, str)

    def test_output_is_simple_if_no_request_is_bound(self):
        value = self.formatter.format(self.record)
        self.assertNotIn('? ms', value)

    def test_values_are_defaulted_to_question_mark(self):
        self.record.path = '/'
        value = self.formatter.format(self.record)
        self.assertIn('? ms', value)

    def test_querystring_is_rendered_as_string(self):
        self.record.path = '/'
        self.record.querystring = {'param': 'val'}
        value = self.formatter.format(self.record)
        self.assertIn('/?param=val', value)

    def test_extra_event_infos_is_rendered_as_key_values(self):
        self.record.nb_records = 5
        value = self.formatter.format(self.record)
        self.assertIn('nb_records=5', strip_ansi(value))

    def test_every_event_dict_entry_appears_in_log_message(self):
        self.record.__dict__ = {
            'msg': 'Pouet',
            'method': 'GET',
            'path': '/v1/',
            'querystring': {'_sort': 'field'},
            'code': 200,
            't': 32,
            'event': 'app.event',
            'nb_records': 5,
            'exc_info': None,
            'stack_info': None,
        }
        value = self.formatter.format(self.record)
        self.assertEqual(('"GET   /v1/?_sort=field" 200 (32 ms)'
                          ' Pouet event=app.event nb_records=5'), strip_ansi(value))

    def test_fields_values_support_unicode(self):
        self.record.value = '\u2014'
        value = self.formatter.format(self.record)
        self.assertIn('\u2014', value)

    def test_extra_event_infos_is_rendered_as_key_values(self):
        self.record.msg = '%r login.'
        self.record.args = ('bob',)
        value = self.formatter.format(self.record)
        self.assertIn("'bob' login.", value)


class LoggerTest(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("test.module")
        self.logger.setLevel(logging.DEBUG)
        formatter = ColorFormatter()
        self.stream = StringIO()
        handler = logging.StreamHandler(self.stream)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def test_advanced_logging_message(self):
        userid = 'bob'
        resource = '/file'

        self.logger.info("%r authorized on {resource}", userid,
                         extra=dict(userid=userid, resource=resource))

        self.assertEqual(strip_ansi(self.stream.getvalue()),
            "'bob' authorized on /file resource=/file userid=bob\n")

    def test_exception_formatting(self):
        try:
            1 / 0
        except:
            self.logger.exception("Oups.")
        output = self.stream.getvalue()
        self.assertIn("Oups. \n", strip_ansi(output))
        self.assertIn("Traceback (most recent call last):", output)
