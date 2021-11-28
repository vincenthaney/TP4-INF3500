import logging
import sys
from datetime import datetime, timedelta


class ProgressLog:
    def __init__(self, title: str, total_nb: int):
        log_with_time(title, tab=1)
        self.nb: int = 0
        self.total_nb: int = total_nb
        self.last_displayed_nb = 0

    def display(self):
        self.nb += 1
        if self.nb >= self.last_displayed_nb + self.total_nb // 10:
            if self.nb % 100 == 0:
                self.last_displayed_nb = self.nb
                numerator: str = str(self.nb)
                denominator: str = str(self.total_nb)
                log(
                    ' ' * (6 - len(numerator)) + numerator + ' / '
                    ' ' * (6 - len(denominator)) + denominator + ' done',
                    tab=2
                )


def log(message: str, tab: int = 0, end: str = "\n"):
    tabs: str = '   ' * tab
    logging.info(tabs + message)
    print(' ' * 8 + '  ' + tabs + message, end=end)


def log_with_time(message: str, tab: int = 0, end: str = "\n"):
    tabs: str = '   ' * tab
    logging.info(message)
    time: str = datetime.now().strftime("%H:%M:%S")
    print(time + '  ' + tabs + message, end=end)


def log_done(message: str):
    logging.info(' -> ' + message)
    print(message)


def log_error(message: str, end: str = "\n"):
    logging.error(message)
    print('\033[91m' + message + "\n", sys.exc_info(), '\033[0m', end=end)


def log_function(function_name: str, is_done: bool):
    if not is_done:
        logging.info('')
        logging.info("------" + function_name.upper() + "------")
        print("------" + function_name.upper() + "------")
    else:
        logging.info("------" + function_name.upper() + "------ done" + '\n')
        logging.info('')
        print("------" + function_name.upper() + "------ done" + '\n')


def log_duration(start_time: datetime):
    delta: timedelta = datetime.now() - start_time
    delta_str: str = ""
    hours: int = delta.seconds // 3600
    minutes: int = (delta.seconds - 3600 * hours) // 60
    seconds: int = (delta.seconds - 3600 * hours - 60 * minutes)
    if hours > 0:
        delta_str += str(hours) + " hours, "
    if minutes > 0 or hours > 0:
        delta_str += str(minutes) + " minutes and "
    delta_str += str(seconds) + " seconds"
    log("Finished in " + delta_str)