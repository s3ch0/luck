import copy
import os.path
import random
import sys
import pandas as pd
import numpy as np
from typing import Union
from .__log import *
from .embellish import printf
from . import excel
from .__base import *

ANALYSE_LOG = Log()

#TODO


class File:

    def __init__(self, path, sep=None):
        # 支持这三种文件格式（ xlsx，xls，csv）
        ANALYSE_LOG.process('The program is importing data...')
        ANALYSE_LOG.process('please wait a moment.')
        self.__name = os.path.basename(path)

        try:
            if file_suffix(path) == 'xlsx' or file_suffix(path) == 'xls':
                self.df = pd.DataFrame(excel.read_column(path)) # df
                self.all_cols = excel.read_column(
                    path) # all_cols:{第一列名字:第一列所有数据...}
                self.__head = [key for key in excel.read_column(path).keys()
                               ] # 获取excel里面的列名
                # 可以使用 list(self.df.columns)获取相应的列名列表

            elif file_suffix(path) == 'csv' and sep is None:
                ANALYSE_LOG.warning(
                    'You did not choose a separator for the csv data!')
                printf('Please enter your sep in your dataset:', end='')
                user_sep = str(input())
                self.df = pd.read_csv(path, sep=user_sep)
                self.__head = [key for key in dict(self.df.iloc[0]).keys()]

            # 待开发 (或许这里可以设置一个条件检查,数据有没有列名,没有的话,可以让用户添加)
            # data = pd.read_csv(path, header=None, names=['Population', 'Profit'])

            elif file_suffix(path) == 'csv' and sep is not None:
                self.df = pd.read_csv(path, sep=sep)
                self.__head = [key for key in dict(self.df.iloc[0]).keys()]
            else:
                ANALYSE_LOG.error('Maybe your file is not an excel file')
                sys.exit(1)

        except Exception as err:
            ANALYSE_LOG.error(f"Sorry! Import the {self.name} failed!")
            ANALYSE_LOG.error(str(err))
            exit(1)

        self.__all_rows = self.df.iloc[:, :].values
        self.__row_number: int = self.df.shape[0]
        self.__column_number: int = self.df.shape[1]
        self.dict_list = []
        self.__col_max: Union[None, int, float] = 1
        self.__col_min: Union[None, int, float] = 0
        ANALYSE_LOG.complete('Congratulations!!!')
        ANALYSE_LOG.complete(f'The dataset: {self.name} imported successfully')

    @property
    def name(self):
        return self.__name

    # 返回对应的行数

    @property
    def rows(self):
        return self.__row_number

    @property
    def head(self):
        return self.__head

    @property
    def columns(self):
        return self.__column_number

    # 返回对应列的最大值
    def max_col(self, col_name):
        if is_number(self.select_col(col_name)[0]):
            tmp = max(self.select_col(col_name))
            self.__col_max = tmp
        return self.__col_max

    # 返回对应列的最小值
    def min_col(self, col_name):
        if is_number(self.select_col(col_name)[0]):
            tmp = min(self.select_col(col_name))
            self.__col_min = tmp
        return self.__col_min

    def count(self, col_name: Union[str, list]) -> Union[dict, list]:
        # study!
        """
        :param col_name:
        :return:
        """
        if isinstance(col_name, list):
            res_list = [self.count(i) for i in col_name]
            return res_list
        elif isinstance(col_name, str):
            col_name_index = self.__head.index(col_name) # 获取对应列名的索引
            tmp_list = copy.deepcopy(self.__head) # 深度拷贝列表
            tmp_list.pop(col_name_index)
            count_dict = dict(
                self.df.groupby(col_name).count()[tmp_list[random.randint(
                    0,
                    len(tmp_list) - 1)]]) # 分组求和
            # 并随机获取其中的一组来代表y的值
            self.dict_list.append(count_dict)
            return count_dict
        else:
            ANALYSE_LOG.error('The input is not a string or list')
            exit(1)

    def select_col(self, col_name: Union[str, list, int]) -> list:
        # 判断
        if isinstance(col_name, list): # 支持一次性选择多行数据
            if set(col_name).issubset(self.__head):
                selected_col = []
                tmp_select_col = [list(self.df[i]) for i in col_name]
                for item in tmp_select_col:
                    if is_number(item[0]):
                        tmp_list = list(map(change_num,
                                            item)) # 将item里的数字转换成相应类型
                        selected_col.append(tmp_list)
                    else:
                        selected_col.append(item)
                return selected_col
            else:
                ANALYSE_LOG.warning('The parameter you entered is wrong!')
                ANALYSE_LOG.warning(
                    'maybe your col_name list have elements not in columns')

        elif isinstance(col_name, str):
            if col_name in self.__head:
                selected_col = list(self.df[col_name])
                if is_number(selected_col[0]): # 判断是否为'数字类型'
                    selected_col = [change_num(i) for i in selected_col]
                    return selected_col
            else:
                ANALYSE_LOG.warning(
                    'The parameter you entered is wrong (maybe the col_name not in columns)!'
                )
        elif isinstance(col_name, int):
            if col_name < self.__column_number:
                return list(self.df.iloc[:, col_name])
            else:
                ANALYSE_LOG.warning(
                    "The parameter you entered is above the columns' number!")
        else:
            ANALYSE_LOG.error(
                "The type of parameter you entered is wrong (not str or list)")

    # 获取所有的列(除了第一列)

    @property
    def all_row(self):
        return self.__all_rows

    def select_row(self, row_number):
        # 默认从0开始
        tmp_list = self.__all_rows
        result = tmp_list[row_number]
        return list(result)

    def search_one(self, col_name: str, condition):
        if isinstance(condition, list):
            pass
        else:
            result = self.df[self.df[col_name] == condition]
            return result.values

    def __str__(self):
        return str(self.df.head())


if __name__ == '__main__':
    pass
