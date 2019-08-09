from functools import wraps
from time import sleep
import os
from datetime import datetime


def retry_call(exception_class, tries=50, delay=2, backoff=1.5, logger=None):
    """Retry calling the decorated function using an exponential backoff.
    We wanted to store the error in database if maximum retries attempted and failed,
    'backoff' package doesn't allow that, hence implemented own retry_attempt

    source: http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry

    :param exception_class: the exception to check. may be a tuple of
        exceptions to check
    :type exception_class: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """

    def log_msg(msg):
        if logger:
            logger.warning(msg)
        else:
            print(msg)

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            local_delay = delay

            for i in range(tries):
                try:
                    data = f(*args, **kwargs)
                    return data
                except KeyboardInterrupt:
                    raise
                except exception_class as e:
                    if i == tries:
                        log_msg('Attempt failed')
                        return []
                    msg = '{}, Retrying in {} seconds...(trying {}/{})'.format(str(e), local_delay, i+1, tries)
                    log_msg(msg)
                    sleep(local_delay)
                    local_delay = round(local_delay * backoff, 2)
            else:
                return []  # max reties fail returning empty array, not raising error
            # return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def print_log(txt_log):
    log_file = os.path.join('.', 'log.txt')
    try:
        with open(log_file, 'at') as log:
            log.write("{}   ==>   {}\n".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), txt_log))
        print(txt_log)
    except Exception as e:
        print(e)
