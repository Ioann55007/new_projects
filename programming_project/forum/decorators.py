from smtplib import SMTPRecipientsRefused

from requests import RequestException

logger = logging.getLogger(__name__)


def except_shell(errors=(Exception,), default_value=''):
    def decorator(func):
        def new_func(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except errors as e:
                logging.error(e)
                return default_value or None
        return new_func
    return decorator


smtp_shell = except_shell((SMTPRecipientsRefused,))
request_shell = except_shell((RequestException,))
