# Decos

import inspect
import logging
from functools import wraps


class FilenameFilter(logging.Filter):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename

    def filter(self, record):
        record.filename = self.filename
        return True


class Log:
    def __init__(self, logger=None):
        self.logger = logger

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            parent_func_name = inspect.currentframe().f_back.f_code.co_name
            module_name = inspect.currentframe().f_back.f_code.co_filename.split("/")[
                -1
            ]
            if not self.logger:
                if "client" in module_name:
                    self.logger = logging.getLogger(f"client_func")
                elif "server" in module_name:
                    self.logger = logging.getLogger(f"server_func")
                else:
                    self.logger = logging.getLogger()
            self.logger.addFilter(FilenameFilter(module_name))
            self.logger.debug(
                f"Функция (метод) {func.__name__} вызвана из функции (метода) {parent_func_name} "
                f"в модуле {module_name} с аргументами:"
                f"{args}; {kwargs}"
            )
            result = func(*args, **kwargs)
            return result

        return wrapper
