# -*- coding: utf-8 -*-
# _Contact_me_: zhouhaobusy@163/gmail.com
# @Time    : 2021/8/12 14:44
# @Author  : Busy To Live
# @FileName: log.py
# @Software: Neovim
# @Blog    : http://www.zhouhaobusy.com

import inspect
import os
from luck.utils import get_terminal_width
from luck.embellish import Color,printf
from luck.consts import STATIC_LOG_STYLE, RUNNING_ENVIRONMENT


class Log:
    log_style = {
        # color style sentence
        "warning": ("yellow", "!", "Warning"),
        "info": ("blue", "*", "Info"),
        "danger": ("danger", "-", "Error"),
        "error": ("red", "-", "Some error occurred!"),
        "debug": ("info", "=", "Debug"),
        "process": ("purple", "+", "Processing..."),
        "complete": ("green", "0", "Complated!"),
        "text": ("white", "", ""),
        "prompt": ("cyan", "", ""),
    }

    __instance = None

    def __init__(self):

        self.__save_file = None
        self.__path = self.line_info()[0]
        self.__file_name = os.path.basename(self.__path)
        self.__func_name = self.line_info()[1]
        self.__lineno = self.line_info()[2]

    def _prepare_line_end(self, the_str):
        # prepare the line end TODO
        if the_str is None:
            return ""

    #  if display_end is False:
    #      return the_str
        else:
            the_buffer = len(self.filename)
            str_len = len(the_str)
            the_space_count = get_terminal_width() - the_buffer - 10 - str_len
            if the_space_count < 0:
                return the_str + self.filename + " " + str(self.lineno)
            else:
                return the_str + " " * the_space_count + self.filename + " " + str(
                    self.lineno)

    @staticmethod
    def line_info():
        f = inspect.currentframe()
        i = inspect.getframeinfo(f.f_back.f_back)
        return i.filename, i.function, i.lineno

    @staticmethod
    def _prepare_log_style(style, the_length: int = 12) -> tuple:
        mini_log = (get_terminal_width() or 84) <= 60
        if style in Log.log_style:
            if mini_log:
                log_str = STATIC_LOG_STYLE[0][0] + Log.log_style[style][1] + STATIC_LOG_STYLE[0][1] + " " + \
                          STATIC_LOG_STYLE[1] * 4 + " "
            else:
                log_str = STATIC_LOG_STYLE[0][0] + Log.log_style[style][1] + STATIC_LOG_STYLE[0][1] + " " + \
                          STATIC_LOG_STYLE[1] * the_length + " "
            log_color = Log.log_style[style][0]
            log_quote = Log.log_style[style][2]

        else:
            log_str = STATIC_LOG_STYLE[0][0] + Log.log_style["text"][1] + STATIC_LOG_STYLE[0][1] + \
                      STATIC_LOG_STYLE[1] * the_length + " "
            log_color = "white"
            log_quote = "None"

        return log_str, log_color, log_quote

    @property
    def filename(self):
        return self.__file_name

    @property
    def path(self):
        # gain the file's path
        return self.__path

    @property
    def func_name(self):
        # gain the calling function's name
        return self.__func_name

    @property
    def lineno(self):
        # gain the calling function's line number
        return self.__lineno

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            return cls.__instance
        else:
            return cls.__instance

    def info(self, msg=None):
        info_result = self._prepare_log_style("info")
        if msg is None:
            printf(info_result[0] + info_result[2], color=info_result[1])
        else:
            printf(info_result[0] + msg, color=info_result[1])

    def debug(self, msg=None):
        info_result = self._prepare_log_style("debug")
        if msg is None:
            printf(self._prepare_line_end(info_result[0] + info_result[2]),
                   color=info_result[1])
        else:
            printf(self._prepare_line_end(info_result[0] + msg),
                   color=info_result[1])

    def error(self, msg=None):
        info_result = self._prepare_log_style("error")
        if msg is None:
            printf(self._prepare_line_end(info_result[0] + info_result[2]),
                   color=info_result[1])
        else:
            printf(self._prepare_line_end(info_result[0] + msg),
                   color=info_result[1])

    def warning(self, msg=None):
        info_result = self._prepare_log_style("warning")
        if msg is None:
            printf(self._prepare_line_end(info_result[0] + info_result[2]),
                   color=info_result[1])
        else:
            printf(self._prepare_line_end(info_result[0] + msg),
                   color=info_result[1])

    def process(self, msg=None):
        info_result = self._prepare_log_style("process")
        if msg is None:
            printf(info_result[0] + info_result[2], color=info_result[1])
        else:
            printf(info_result[0] + msg, color=info_result[1])

    def complete(self, msg=None):
        info_result = self._prepare_log_style("complete")
        if msg is None:
            printf(info_result[0] + info_result[2], color=info_result[1])
        else:
            printf(info_result[0] + msg, color=info_result[1])

    def prompt(self, msg=None):
        info_result = self._prepare_log_style("prompt")
        if msg is None:
            printf(info_result[0] + info_result[2], color=info_result[1])
        else:
            printf(info_result[0] + msg, color=info_result[1])

    def __repr__(self):
        return self.__file_name + " " + self.__func_name + " " + str(
            self.__lineno)


if __name__ == '__main__':
    log1 = Log()
    log1.info()
    log1.debug()
    log1.error()
    log1.warning()
    log1.process()
    log1.complete()
