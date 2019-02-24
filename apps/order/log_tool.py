import os
import logging
import logging.config
import logging.handlers
from datetime import datetime

try:
    from StayOrder.settings import BASE_DIR
except Exception as im_err:
    try:
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    except Exception as im_err:
        print("包错入异常：{}".format(im_err))


class _InfoFilter(logging.Filter):
    def filter(self, record):
        if logging.DEBUG <= record.levelno < logging.ERROR:
            return super().filter(record)
        else:
            return 0


def _get_filename(*, filename='app.log', log_level='info'):
    date_str = datetime.today().strftime('%Y%m%d')
    file_address = BASE_DIR + '/logFiles/'
    log_name = filename + '_' + log_level + '_' + date_str
    return file_address + log_name


class _LogFactory:
    # 每个日志文件，使用 1G
    _SINGLE_FILE_MAX_BYTES = 1 * 1024 * 1024 * 1024
    # 轮转数量是 400 个
    _BACKUP_COUNT = 400

    # 基于 dictConfig，做再次封装
    _LOG_CONFIG_DICT = {
        'version': 1,

        'disable_existing_loggers': False,

        'formatters': {
            # 开发环境下的配置
            'dev': {
                'class': 'logging.Formatter',
                'filemode': 'a',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'format': ('%(levelname)s %(asctime)s %(created)f %(name)s %(module)s '
                           '[%(filename)s %(lineno)s %(funcName)s] %(message)s')
            },
            # 生产环境下的格式(越详细越好)
            'prod': {
                'class': 'logging.Formatter',
                'filemode': 'a',
                'datefmt': '%Y-%m-%d %H:%M:%S',
                'format': '{%(message)s,"handle_date":"%(asctime)s","level":"%(levelname)s"}'
            }

        },

        # 针对 LogRecord 的筛选器
        'filters': {
            'debug_filter': {
                '()': _InfoFilter,
            },
            'info_filter': {
                '()': _InfoFilter,
            },
            'warning_filter': {
                '()': _InfoFilter,
            },
            'error_filter': {
                '()': _InfoFilter,
            }
        },

        # 处理器(被loggers使用)
        'handlers': {
            'debug_console': {  # 按理来说, console只收集ERROR级别的较好
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'dev'
            },

            'debug_file_product': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': _get_filename(filename='prod.log'),
                'maxBytes': _SINGLE_FILE_MAX_BYTES,  # 1G
                'encoding': 'UTF-8',
                'backupCount': _BACKUP_COUNT,
                'formatter': 'prod',
                'delay': True,
                'filters': ['debug_filter', ]  # only DEBUG, no ERROR
            },
            'debug_file_test': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': _get_filename(filename='test.log'),
                'maxBytes': _SINGLE_FILE_MAX_BYTES,  # 1G
                'encoding': 'UTF-8',
                'backupCount': _BACKUP_COUNT,
                'formatter': 'prod',
                'delay': True,
                'filters': ['info_filter', ]  # only INFO
            },
            'debug_file_simu': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': _get_filename(filename='simu.log'),
                'maxBytes': _SINGLE_FILE_MAX_BYTES,  # 1G
                'encoding': 'UTF-8',
                'backupCount': _BACKUP_COUNT,
                'formatter': 'prod',
                'delay': True,
                'filters': ['warning_filter', ]  # only WARNING
            },
            'debug_file_line': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': _get_filename(filename='line.log'),
                'maxBytes': _SINGLE_FILE_MAX_BYTES,  # 1G
                'encoding': 'UTF-8',
                'backupCount': _BACKUP_COUNT,
                'formatter': 'prod',
                'delay': True,
                'filters': ['error_filter', ]  # only ERROR
            },
            'debug_file_error': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': _get_filename(filename='error.log'),
                'maxBytes': _SINGLE_FILE_MAX_BYTES,  # 1G
                'encoding': 'UTF-8',
                'backupCount': _BACKUP_COUNT,
                'formatter': 'prod',
                'delay': True,
                'filters': ['error_filter', ]  # only ERROR
            },
            'debug_file_ding': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': _get_filename(filename='ding.log'),
                'maxBytes': _SINGLE_FILE_MAX_BYTES,  # 1G
                'encoding': 'UTF-8',
                'backupCount': _BACKUP_COUNT,
                'formatter': 'prod',
                'delay': True,
                'filters': ['error_filter', ]  # only ERROR
            },

        },

        # 真正的logger(by name), 可以有丰富的配置
        'loggers': {
            'DEBUGGER_PRODUCT': {
                # 输送到3个handler，它们的作用分别如下
                #   1. console：控制台输出，方便我们直接查看，只记录ERROR以上的日志就好
                #   2. file： 输送到文件，记录INFO以上的日志，方便日后回溯分析
                #   3. file_error：输送到文件（与上面相同），但是只记录ERROR级别以上的日志，方便研发人员排错
                'handlers': ['debug_file_product'],
                'level': 'INFO',
            },
            'DEBUGGER_TEST': {
                # 输送到3个handler，它们的作用分别如下
                #   1. console：控制台输出，方便我们直接查看，只记录ERROR以上的日志就好
                #   2. file： 输送到文件，记录INFO以上的日志，方便日后回溯分析
                #   3. file_error：输送到文件（与上面相同），但是只记录ERROR级别以上的日志，方便研发人员排错
                'handlers': ['debug_file_test'],
                'level': 'INFO',
            },
            'DEBUGGER_SIMU': {
                # 输送到3个handler，它们的作用分别如下
                #   1. console：控制台输出，方便我们直接查看，只记录ERROR以上的日志就好
                #   2. file： 输送到文件，记录INFO以上的日志，方便日后回溯分析
                #   3. file_error：输送到文件（与上面相同），但是只记录ERROR级别以上的日志，方便研发人员排错
                'handlers': ['debug_file_simu'],
                'level': 'INFO',
            },
            'DEBUGGER_LINE': {
                # 输送到3个handler，它们的作用分别如下
                #   1. console：控制台输出，方便我们直接查看，只记录ERROR以上的日志就好
                #   2. file： 输送到文件，记录INFO以上的日志，方便日后回溯分析
                #   3. file_error：输送到文件（与上面相同），但是只记录ERROR级别以上的日志，方便研发人员排错
                'handlers': ['debug_file_line'],
                'level': 'INFO',
            },
            'DEBUGGER_ERROR': {
                # 输送到3个handler，它们的作用分别如下
                #   1. console：控制台输出，方便我们直接查看，只记录ERROR以上的日志就好
                #   2. file： 输送到文件，记录INFO以上的日志，方便日后回溯分析
                #   3. file_error：输送到文件（与上面相同），但是只记录ERROR级别以上的日志，方便研发人员排错
                'handlers': ['debug_file_error'],
                'level': 'INFO',
            },
            'DEBUGGER_DING': {
                # 输送到3个handler，它们的作用分别如下
                #   1. console：控制台输出，方便我们直接查看，只记录ERROR以上的日志就好
                #   2. file： 输送到文件，记录INFO以上的日志，方便日后回溯分析
                #   3. file_error：输送到文件（与上面相同），但是只记录ERROR级别以上的日志，方便研发人员排错
                'handlers': ['debug_file_ding'],
                'level': 'INFO',
            },
        },
    }

    logging.config.dictConfig(_LOG_CONFIG_DICT)

    @classmethod
    def get_logger(cls, logger_name):
        return logging.getLogger(logger_name)


DEBUGGER_PRODUCT = logging.getLogger('DEBUGGER_PRODUCT')
DEBUGGER_TEST = logging.getLogger('DEBUGGER_TEST')
DEBUGGER_SIMU = logging.getLogger('DEBUGGER_SIMU')
DEBUGGER_LINE = logging.getLogger('DEBUGGER_LINE')
DEBUGGER_ERROR = logging.getLogger('DEBUGGER_ERROR')
DEBUGGER_DING = logging.getLogger('DEBUGGER_DING')


def product_log(product_name, username, action, details):
    DEBUGGER_PRODUCT.info('"logType":"{0}",'
                          '"productName":"{1}",'
                          '"handle_person":"{2}",'
                          '"action":"{3}",'
                          '"detail":"{4}"'.format(0,
                                                  product_name,
                                                  username,
                                                  action,
                                                  details))


def test_log(product_name, username, action, details):
    DEBUGGER_TEST.info('"logType":"{0}",'
                       '"productName":"{1}",'
                       '"handle_person":"{2}",'
                       '"action":"{3}",'
                       '"detail":"{4}"'.format(1,
                                               product_name,
                                               username,
                                               action,
                                               details))


def simu_log(product_name, username, action, details):
    DEBUGGER_SIMU.info('"logType":"{0}",'
                       '"productName":"{1}",'
                       '"handle_person":"{2}",'
                       '"action":"{3}",'
                       '"detail":"{4}"'.format(2,
                                               product_name,
                                               username,
                                               action,
                                               details))


def line_log(product_name, username, action, details):
    DEBUGGER_LINE.info('"logType":"{0}",'
                       '"productName":"{1}",'
                       '"handle_person":"{2}",'
                       '"action":"{3}",'
                       '"detail":"{4}"'.format(3,
                                               product_name,
                                               username,
                                               action,
                                               details))


def error_log(product_name, username, action, details):
    DEBUGGER_ERROR.info('"logType":"{0}",'
                        '"productName":"{1}",'
                        '"handle_person":"{2}",'
                        '"action":"{3}",'
                        '"detail":"{4}"'.format(4,
                                                product_name,
                                                username,
                                                action,
                                                details))


def ding_log(details):
    DEBUGGER_DING.info('"logType":"{0}",'
                       '{1}'.format(5, details))
