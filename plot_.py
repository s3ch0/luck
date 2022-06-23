from typing import Union
from pyecharts.faker import Faker
from embellish import printf
import analyse
# from luck.consts import CHART_DEAULT_DATA
from __base import *
from pyecharts.charts import Bar, Pie, Line, Scatter
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from functools import partial

PLOT_LOG = Log()


class Chart:

    def __init__(self):
        self.bg_color: str = 'rgba(255,254,250,0.2)' # 图表背景的颜色
        self.page_title: str = "Chart" # 网页的名字
        self.theme: str = ThemeType.WHITE # 主题
        self.animation: bool = False # 动画效果
        self.chart_title: Union[str, None] = None # 父标题
        self.chart_subtitle: Union[str, None] = None # 子标题
        self.tool_box: bool = False # 工具栏
        self.visual_map: bool = False # 视觉映射配置
        self.page: Union[bool, int, None] = False # 页面布局配置
        self.__width: str = '1200px'
        self.__height: str = '550px'
        self.__x_data: Union[None, list] = None # key_data
        self.__y_data: Union[None, list] = None # value_data
        self.__legend = None

    @property
    def data(self):
        return self.__x_data, self.__y_data

    @data.setter
    def data(self, data: dict):
        if isinstance(data, dict):
            tmp_x, tmp_y = separate(data) # 将字典转换成两个列表
            tmp_y = change_num_list(tmp_y) # 将y_data可能出现的字符串类型的数字变成相应的类型
            self.__x_data = tmp_x
            self.__y_data = tmp_y
        else:
            PLOT_LOG.error('The data must be type of dict!')

    @property
    def x_data(self):
        return self.__x_data

    @x_data.setter
    def x_data(self, x_data: list):
        if not isinstance(x_data, list):
            type_var = show_type(x_data)
            PLOT_LOG.error('The x_data must be list can not be %s' % type_var)
        else:
            self.__x_data = x_data

    @property
    def y_data(self):
        return self.__y_data

    @y_data.setter
    def y_data(self, y_data: list):
        if not isinstance(y_data, list):
            type_var = show_type(y_data)
            PLOT_LOG.error('The y_data must be list can not be %s' % type_var)
        else:
            # [[],[]]这种情况的检测
            if isinstance(y_data[0], list):
                if len(y_data) == 1: # 将[[]] 转成 []
                    y_data = change_num_list(y_data[0])
                    if type_check(y_data):
                        self.__y_data = y_data
                    else:
                        PLOT_LOG.error('y_dataformat error!')
                else:
                    tmp_y_data_list = []
                    for i in y_data:
                        i = change_num_list(i)
                        if type_check(i):
                            tmp_y_data_list.append(i)
                        else:
                            PLOT_LOG.error('y_data format error!')
                            break
                    else:
                        self.__y_data = tmp_y_data_list
            else:
                y_data = change_num_list(y_data)
                if type_check(y_data):
                    self.__y_data = y_data
                else:
                    PLOT_LOG.error('y_data format error!')

    @property
    def width(self):
        return self.__width

    @width.setter # 图表宽度设置
    def width(self, width: Union[str, int, None]):
        if isinstance(width, int):
            width = str(width) + 'px'
            self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter # 图表高度设置
    def height(self, height: Union[str, int, None]):
        if isinstance(height, int):
            height = str(height) + 'px'
        self.__height = height

    def get_canvas(self):
        return self.__width, self.__height


class BarChart(Chart):

    def __init__(self):
        super().__init__()


class PieChart(Chart):
    pass


class LineChart(Chart):
    pass


class ScatterChart(Chart):
    pass
