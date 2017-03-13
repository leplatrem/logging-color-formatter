import logging

import colorama


def decode_value(value):
    try:
        return str(value)
    except UnicodeDecodeError:  # pragma: no cover
        return bytes(value).decode('utf-8')


class ColorFormatter(logging.Formatter):
    EXCLUDED_LOGRECORD_ATTRS = set((
        'args', 'asctime', 'created', 'exc_info', 'exc_text', 'filename',
        'funcName', 'levelname', 'levelno', 'lineno', 'module', 'msecs',
        'message', 'msg', 'name', 'pathname', 'process', 'processName',
        'relativeCreated', 'stack_info', 'thread', 'threadName'
    ))

    def format(self, record):
        RESET_ALL = colorama.Style.RESET_ALL
        BRIGHT = colorama.Style.BRIGHT
        CYAN = colorama.Fore.CYAN
        MAGENTA = colorama.Fore.MAGENTA
        YELLOW = colorama.Fore.YELLOW

        event_dict = {**record.__dict__}

        if 'path' in event_dict:
            pattern = (BRIGHT +
                       '"{method: <5} {path}{querystring}"' +
                       RESET_ALL +
                       YELLOW + ' {code} ({t} ms)' +
                       RESET_ALL +
                       ' {event} {context}')
        else:
            pattern = BRIGHT + '{event}' + RESET_ALL + ' {context}'

        raw_msg = str(event_dict.pop('msg', '?')) % event_dict.pop('args', [])
        msg_interpolated = raw_msg.format(**event_dict)

        output = {
            'event': msg_interpolated
        }
        for field in ['method', 'path', 'code', 't']:
            output[field] = decode_value(event_dict.pop(field, '?'))

        querystring = event_dict.pop('querystring', {})
        params = [decode_value('{}={}'.format(*qs)) for qs in querystring.items()]
        output['querystring'] = '?{}'.format('&'.join(params) if params else '')

        output['context'] = " ".join(
            CYAN + key + RESET_ALL +
            "=" +
            MAGENTA + decode_value(event_dict[key]) +
            RESET_ALL
            for key in sorted([k for k in event_dict.keys()
                               if k not in self.EXCLUDED_LOGRECORD_ATTRS])
        )

        log_msg = pattern.format_map(output)

        if record.exc_info:
            log_msg += "\n" + self.formatException(record.exc_info)
        if record.stack_info:
            log_msg += "\n" + self.formatStack(record.stack_info)

        return log_msg
