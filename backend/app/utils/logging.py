import os 
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime, timedelta, timezone
from app.utils.file_system import PROJECT_ROOT
from app.utils.file_system import ensure_dir
from app.utils.file_system import combine_relative_path

KST = timezone(timedelta(hours=9))


class KSTFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt="%Y-%m-%d %H:%M:%S", style="%"):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)
        self.datefmt = datefmt

    def formatTime(self, record, datefmt=None):
        kst_time = datetime.fromtimestamp(record.created, tz=KST)
        if datefmt:
            s = kst_time.strftime(datefmt)
        else:
            s = kst_time.strftime(self.datefmt)
        return s

    def format(self, record):
        log_message = super().format(record)
        divide = "-" * 100
        return f"\n{divide}\n\n{log_message}"


def get_folder_path(target_path, dt=None, type='error'):
    if dt is None:
        dt = datetime.now(KST)
    log_dir = combine_relative_path(PROJECT_ROOT, 
                                    target_path, 
                                    dt.strftime('%Y-%m-%d'))
    ensure_dir(log_dir)
    return log_dir + os.sep + type + '.log'


LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL = logging.DEBUG
LOG_FILE = get_folder_path('app/monitoring/logs/backend')

formatter = KSTFormatter(LOG_FORMAT)

# 핸들러 설정 (날짜별 회전 설정)
file_handler = TimedRotatingFileHandler(
    LOG_FILE,          
    when="midnight", 
    interval=1, 
    backupCount=30, 
    utc=False
)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
logger.addHandler(file_handler)


def log_exception(exception: Exception):
    exc_info = (type(exception), exception, exception.__traceback__)
    logger.error("Exception occurred.", exc_info=exc_info)
