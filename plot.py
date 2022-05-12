from typing import Sequence

from pyecharts import options as opts
from pyecharts.charts import Bar, Pie, Line, Scatter, chart
from pyecharts.globals import ThemeType

from .__base import *
from .embellish import printf

PLOT_LOG = Log()


# TODO: when the data not set the program will crash and exit <++>


def __data_checker(lhs_data, rhs_data):
    """
    This function will check if the data is valid.
    for example: check the y_column_name and y_data list length if or not match
    """
    pass


class Chart:
    def __init__(self):
        self.bg_color: str = 'rgba(255,254,250,0.2)'     # char's background color
        self.page_title: str = "Chart"                   # the web page's name
        self.theme: str = ThemeType.WHITE                # the theme of the chart
        self.__file_name: Union[str, None] = None        # the name will be used to save the chart
        self.animation: bool = True                      # animation of the chart
        self.chart_title: Union[str, None] = None        # the title of the chart
        self.chart_subtitle: Union[str, None] = None     # the subtitle of the chart
        self.tool_box: bool = True                       # the tool box of the chart
        self.visual_map: bool = True                     # the visual map of the chart
        self.page: Union[bool, int, None] = False        # the layout of the chart
        self.__width: str = '1200px'                     # the width of the chart
        self.__height: str = '550px'                     # the height of the chart
        self.__x_data: Union[Sequence, None] = None      # key_data of the chart : xaxis
        self.__y_data: Union[Sequence, None] = None      # value_data of the chart : yaxis

        self.__yaxis_options: dict = {}                  # the options of the yaxis
        self.__extra_data: Union[Sequence, None] = None  # extra_data of the chart
        self.y_column_name: Union[Sequence, None] = None # the name of the y_axis

        self.legend = True

    @property
    def yaxis_options(self):
        my_yaxis_options = {

            #  series_name: str,
            #  y_axis: types.Sequence[types.Union[opts.LineItem, dict]],
            #  is_selected: bool = True,
            #  is_connect_nones: bool = False,
            #  xaxis_index: types.Optional[types.Numeric] = None,
            #  yaxis_index: types.Optional[types.Numeric] = None,
            #  color: types.Optional[str] = None,
            #  is_symbol_show: bool = True,
            #  symbol: types.Optional[str] = None,
            #  symbol_size: types.Union[types.Numeric, types.Sequence] = 4,
            #  stack: types.Optional[str] = None,
            #  is_smooth: bool = False,
            #  is_clip: bool = True,
            #  is_step: bool = False,
            #  is_hover_animation: bool = True,
            #  z_level: types.Numeric = 0,
            #  z: types.Numeric = 0,
            #  markpoint_opts: types.MarkPoint = None,
            #  markline_opts: types.MarkLine = None,
            #  tooltip_opts: types.Tooltip = None,
            #  itemstyle_opts: types.ItemStyle = None,
            #  label_opts: types.Label = opts.LabelOpts(),
            #  linestyle_opts: types.LineStyle = opts.LineStyleOpts(),
            #  areastyle_opts: types.AreaStyle = opts.AreaStyleOpts(),
        }

        return my_yaxis_options

    @property
    def chart_init_options(self):
        """
        This function will return the chart's init options
        """

        my_init_option = {
            "width": self.__width,
            "height": self.__height,
            "page_title": self.page_title,
            "theme": self.theme,
            "bg_color": self.bg_color,
        }

        return my_init_option

    @property
    def file_name(self):
        """
        This function will return the file name
        """

        return self.__file_name

    @file_name.setter
    def file_name(self, file_name: str):
        """
        This function will set the file name
        """

        if not isinstance(file_name, str):
            type_var = show_type(file_name)
            PLOT_LOG.error('The file_name must be str can not be %s' % type_var)
        if file_suffix(file_name) == 'html':
            self.__file_name = file_name
        else:
            self.__file_name = file_name + '.html'

    @property
    def data(self):
        """
        This function will return the data
        the data is equilavent to the ( x_data,y_data )
        """
        return self.__x_data, self.__y_data

    @data.setter
    def data(self, data: dict):

        """
        This function will return the data
        the data API used to set the data of the chart
        convenient the user to set the x_data and y_data
        chart.data = {"a":1,"b":2} is equilavent to chart.x_data = ["a","b"] and chart.y_data = [1,2]
        """
        if isinstance(data, dict):
            tmp_x, tmp_y = separate(data)  # change the dict to two list
            tmp_y = change_num_list(tmp_y)  # let the y_data be a list of number
            self.__x_data = tmp_x
            self.__y_data = tmp_y
        else:
            PLOT_LOG.error('The data must be type of dict!')

    @property
    def x_data(self):
        """
        This function will return the x_data
        """
        return self.__x_data

    @x_data.setter
    def x_data(self, x_data: list):
        """
        This function will set the x_data
        """
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
        """
        maybe the y_data function have some problem
        because in the y_data function, the y_data must be a list and the value must be a number
        this will be fixed in the future
        and for the format like this: [[],[]] not support or not check
        """

        if not isinstance(y_data, list):
            type_var = show_type(y_data)
            PLOT_LOG.error('The y_data must be list can not be %s' % type_var)
        else:
            # [[],[]]这种情况的检测
            if isinstance(y_data[0], list):
                if len(y_data) == 1:  # 将[[]] 转成 []
                    y_data = change_num_list(y_data[0])
                    if type_check(y_data):
                        self.__y_data = y_data
                    else:
                        PLOT_LOG.error('y_data format error!')
                else:
                    tmp_y_data_list = []
                    for i in y_data:
                        i = change_num_list(i)
                        if type_check(i):
                            tmp_y_data_list.append(i)
                        else:
                            PLOT_LOG.error('y_data format error!')
                            exit(1)
                    self.__y_data = tmp_y_data_list
            else:
                y_data = change_num_list(y_data)
                if type_check(y_data):
                    self.__y_data = y_data
                else:
                    PLOT_LOG.error('y_data format error!')

    @property
    def width(self):
        """
        This function will return the width of the chart
        """
        return self.__width

    @width.setter  # 图表宽度设置
    def width(self, width: Union[str, int, None]):
        """
        This function will set the width of the chart
        """
        if isinstance(width, int):
            width = str(width) + 'px'
            self.__width = width

    @property
    def height(self):
        """
        This function will return the height of the chart
        """
        return self.__height

    @height.setter  # 图表高度设置
    def height(self, height: Union[str, int, None]):
        """
        This function will set the height of the chart
        """
        if isinstance(height, int):
            height = str(height) + 'px'
            self.__height = height

    def get_canvas(self):
        return self.__width, self.__height

    @property
    def chart_global_options(self):
        """
        This function will return the chart's global options
        """
        my_global_options = {
            "title_opts": opts.TitleOpts(title=self.chart_title, subtitle=self.chart_subtitle),
            "toolbox_opts": opts.ToolboxOpts(is_show=self.tool_box, orient="vertical", pos_left="95%"),
            "brush_opts": opts.BrushOpts(),
            # the legend_opts should be empty at first
            #  "legend_opts"  : opts.LegendOpts(type_='scroll', pos_top="top", orient="horizontal")
            "legend_opts": opts.LegendOpts(is_show=self.legend, pos_top="top", orient="horizontal"),
            "visualmap_opts": opts.VisualMapOpts(is_show=self.visual_map, max_=max(self.y_data),
                                                 min_=min(self.y_data), pos_left="left")

        }

        return my_global_options

    def save_file(self, chart_obj):
        """
        This function will use render func to save the chart to the html file
        """

        if self.file_name is None:
            PLOT_LOG.warning("Please enter your file name: ")
            self.file_name = str(input())
        # this function .... <++>  
        chart_obj.render(self.file_name)
        PLOT_LOG.complete(f"Plot the {self.file_name} successfully!")

    def data_handle(self, chart_obj):
        """
        This function will handle the data for different chart
        """

        chart_obj.add_xaxis(self.x_data)
        # <++>
        if isinstance(self.y_data[0], list):
            tmp = 0
            if self.y_column_name is None:
                PLOT_LOG.warning("Your y_axis column name not set!")
                PLOT_LOG.info("The default column name will be use")
                for item in self.y_data:
                    chart_obj.add_yaxis('Data' + str(tmp), item)
                    tmp += 1
            else:
                for item in self.y_data:
                    chart_obj.add_yaxis(self.y_column_name[tmp], item)
                    tmp += 1
        else:
            chart_obj.add_yaxis(self.y_column_name, self.y_data)


class BarChart(Chart):
    """
    This class will be used to plot the bar chart
    """

    def __init__(self):
        super().__init__()
        self.init_opts = None
        self.data_zoom: bool = False
        self.mark_line: bool = True
        self.mark_point: bool = False
        self.reverse: bool = False
        self.chart_title: Union[str, None] = 'bar Chart'
        self.chart_subtitle: Union[str, None] = None
        self.yaxis_name: str = 'y轴'  # y轴的名字
        self.y_column_name: Union[str, None, list] = None  #
        self.xaxis_name: str = 'x轴'  # x轴的名字
        self.__xaxis_slope: int = 0  # 设置x轴每个数据项名称的斜度()度数
        self.yaxis_fomat: str = "{value}"  # y轴数据格式化

    @property
    def slope(self):  # set xaxis_slope
        return self.__xaxis_slope

    @slope.setter
    def slope(self, slope: Union[str, int, None]):
        if isinstance(slope, str) and is_number(slope):  # 如果传过来的为字符串(判断是否为字符串的数字)
            int_slope = int(slope)
        elif isinstance(slope, int):
            int_slope = slope
        else:
            PLOT_LOG.error('Type error')
            int_slope = 0
        if int_slope > 360 or int_slope < -360:
            PLOT_LOG.error('Numerical error')
        else:
            self.__xaxis_slope = int_slope

    def info(self):  # 待开发(获取配置信息的接口)
        def canvas_info():
            printf('Canvas information')

    def init(self):
        self.init_opts = None
        self.data_zoom: bool = False
        self.mark_line: bool = True
        self.mark_point: bool = False
        self.reverse: bool = False
        self.chart_title: Union[str, None] = 'bar Chart'
        self.chart_subtitle: Union[str, None] = None
        self.yaxis_name: str = 'y轴'
        self.xaxis_name: str = 'x轴'
        self.__xaxis_slope: int = 0

    @property
    def bar_global_options(self):
        my_global_options = self.chart_global_options
        if self.data_zoom == True:
            my_global_options.update({"datazoom_opts": opts.DataZoomOpts(is_show=self.data_zoom)})
        return my_global_options

    @property
    def bar_mark_options(self):
        my_mark_options = {
            "label_opts": opts.LabelOpts(is_show=False),  # 设置是否在柱体上显示数据
            "markpoint_opts": opts.MarkPointOpts(
                data=[
                    opts.MarkPointItem(type_="max", name="max"),
                    opts.MarkPointItem(type_="min", name="min"),
                    opts.MarkPointItem(type_="average", name="average"), ]
            ),
        }
        return my_mark_options

    @property
    def bar_line_options(self):
        my_line_options = {
            "label_opts": opts.LabelOpts(is_show=False),
            "markline_opts": opts.MarkLineOpts(
                data=[
                    opts.MarkLineItem(type_="min", name="min"),
                    opts.MarkLineItem(type_="max", name="max"),
                    opts.MarkLineItem(type_="average", name="average"),
                ]
            ),
        }
        return my_line_options

    @property
    def bar_axis_options(self):
        # TODO <++> the LabelOpts have many attribute can be set, we can set a default config

        my_axis_options = {
            "xaxis_opts": opts.AxisOpts(name=self.xaxis_name,
                                        axislabel_opts=opts.LabelOpts(rotate=self.slope)),
            "yaxis_opts": opts.AxisOpts(name=self.yaxis_name,
                                        axislabel_opts=opts.LabelOpts(rotate=self.slope, formatter=self.yaxis_fomat)), }
        return my_axis_options

    def bar_base(self):
        bar = Bar(init_opts=opts.InitOpts(**self.chart_init_options))
        bar.set_global_opts(**self.bar_global_options, **self.bar_axis_options)

        # 可以在global_opts里添加xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),

        # 可以通过以下方式来格式化y轴数据
        # yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value} /月")),

        self.data_handle(bar)

        if self.reverse:
            self.mark_point = False
            bar.reversal_axis()
            bar.set_series_opts(label_opts=opts.LabelOpts(position="right"))

        if self.mark_point:
            bar.set_series_opts(**self.bar_mark_options)  # 设置柱状图的point标记
        if self.mark_line is True:
            bar.set_series_opts(**self.bar_line_options)  # 设置柱状图的line标记

        self.save_file(bar)

        #  TODO <++> 添加柱状图的折线图


class PieChart(Chart):
    def __init__(self):
        super().__init__()
        self.name: str = 'item'
        self.series_name: str = '数据'  # series_name
        self.sort: bool = False

        self.visual_map = False
        self.tool_box = False
        self.data_zoom = False

        self.rose: bool = True
        self.rosetype = 'area'  # radius area
        self.data_pair = []
        self.position: list = ['50%', '50%']  # the position of the center of the pie chart

        self.radius: list = ["30%", "75%"]

    @property
    def pie_global_options(self):
        my_global_options = self.chart_global_options
        return my_global_options

    @property
    def pie_series_options(self):
        my_series_options = {
            "tooltip_opts": opts.TooltipOpts(trigger=self.name, formatter="{a} <br/>{b}: {c} ({d}%)"),
            "label_opts": opts.LabelOpts(formatter="{b}")
        }
        return my_series_options

    def pie_base(self, series_name=None):
        self.data_pair = [list(z) for z in zip(self.x_data, self.y_data)]
        if self.sort is True:
            self.data_pair.sort(key=lambda x: x[1])
        if series_name is not None:
            self.series_name = series_name
        else:
            pass
        pie = Pie(init_opts=opts.InitOpts(**self.chart_init_options))

        # data_pair = [list(z) for z in zip(key_data, value_data)]
        # data_pair.sort(key=lambda x: x[1])  # 开启饼图排序

        pie.add(series_name=self.series_name, data_pair=self.data_pair)
        pie.set_global_opts(**self.pie_global_options)
        pie.set_series_opts(**self.pie_series_options)
        self.save_file(pie)

    def pie_rose(self, series_name=None):

        self.data_pair = [list(z) for z in zip(self.x_data, self.y_data)]

        if self.sort is True:
            self.data_pair.sort(key=lambda x: x[1])
        if series_name is not None:
            self.series_name = series_name
        else:
            pass
        pie = Pie(init_opts=opts.InitOpts(**self.chart_init_options))

        # data_pair = [list(z) for z in zip(key_data, value_data)]
        # data_pair.sort(key=lambda x: x[1])  # 开启饼图排序

        pie.add(series_name=self.series_name, data_pair=self.data_pair, radius=self.radius,
                center=self.position, rosetype="area")

        pie.set_global_opts(**self.pie_global_options)
        pie.set_series_opts(**self.pie_series_options)
        self.save_file(pie)

    def pie_doughnut(self, series_name=None):
        self.data_pair = [list(z) for z in zip(self.x_data, self.y_data)]
        if self.sort is True:
            self.data_pair.sort(key=lambda x: x[1])
        if series_name is not None:
            self.series_name = series_name
        else:
            pass
        pie = Pie(init_opts=opts.InitOpts(**self.chart_init_options))
        # data_pair = [list(z) for z in zip(key_data, value_data)]
        # data_pair.sort(key=lambda x: x[1])  # 开启饼图排序
        pie.set_global_opts(**self.pie_global_options)

        pie.add(
            series_name=self.series_name,
            data_pair=[list(z) for z in zip(self.x_data, self.y_data)],
            radius=["50%", "70%"],
            label_opts=opts.LabelOpts(is_show=False, position="center"),
        )

        pie.set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            # label_opts=opts.LabelOpts(formatter="{b}: {c}")
        )
        self.save_file(pie)


class LineChart(Chart):
    def __init__(self):
        super().__init__()
        self.data_zoom = False

    @property
    def line_y_xaxis_options(self):
        my_line_y_xaxis_options = {

            "series_name": "",
            "y_axis": self.y_data,
            "symbol": "emptyCircle",
            "is_symbol_show": True,
            "label_opts": opts.LabelOpts(is_show=False),

        }

        return my_line_y_xaxis_options

    @property
    def line_global_options(self):
        my_line_global_options = self.chart_global_options
        if self.data_zoom == True:
            my_line_global_options.update({"datazoom_opts": opts.DataZoomOpts(is_show=self.data_zoom)})

        return my_line_global_options

    def data_handle(self):
        pass

    def line_base(self):
        line = Line(init_opts=opts.InitOpts(**self.line_global_options))
        line.set_global_opts(**self.chart_global_options)
        self.data_handle(line)
        self.save_file(line)
        pass

    @property
    def line_axis_options(self):
        # TODO <++> the LabelOpts have many attribute can be set, we can set a default config

        #          my_line_axis_options = {
        #  "xaxis_opts": opts.AxisOpts(name=self.xaxis_name,
        #                              type_="category", boundary_gap=False
        #                              axislabel_opts=opts.LabelOpts(rotate=self.slope)),
        #                              "yaxis_opts": opts.AxisOpts(type_="value",name=self.yaxis_name,axistick_opts=opts.AxisTickOpts(is_show=True),
        #                              splitline_opts=opts.SplitLineOpts(is_show=True),
        #                              axislabel_opts=opts.LabelOpts(rotate=self.slope,formatter=self.yaxis_fomat)), }
        #
        #  return my_line_axis_options
        pass

    @staticmethod
    def line_beautiful(self):

        pass

    def line_area(self):
        line = Line(init_opts=opts.InitOpts(**self.line_global_options))
        line.set_global_opts(**self.chart_global_options)
        line.add_xaxis(xaxis_data=self.x_data)
        my_line_y_xaxis_options = self.line_y_xaxis_options
        my_line_y_xaxis_options.update({"areastyle_opts": opts.AreaStyleOpts(opacity=1, color="#C67570"), })
        line.add_yaxis(**self.line_y_xaxis_options)
        self.save_file(line)

    def line_smooth(self):
        line = Line(init_opts=opts.InitOpts(**self.chart_init_options))
        line.set_global_opts(**self.line_global_options)
        line.add_xaxis(self.x_data)
        line_y_xaxis_options = self.line_y_xaxis_options
        line_y_xaxis_options.update({"is_smooth": True})
        line.add_yaxis(**line_y_xaxis_options)
        self.save_file(line)


class ScatterChart(Chart):
    def __init__(self):
        super().__init__()
        pass

    def scatter_base(self):
        scatter = Scatter(init_opts=opts.InitOpts(**self.chart_init_options))
        scatter.set_global_opts(**self.chart_global_options)
        self.data_handle(scatter)
        self.save_file(scatter)

    def scatter_size(self):
        scatter = Scatter(init_opts=opts.InitOpts(**self.chart_init_options))
        my_global_options = self.chart_global_options
        my_global_options.update()

        #  "visualmap_opts": opts.VisualMapOpts(type_="size", max_=max(self.y_data), min_=min(self.y_data))
        self.data_handle(scatter)
        scatter.set_global_opts(
            title_opts=opts.TitleOpts(title=self.chart_title, subtitle=self.chart_subtitle),
            visualmap_opts=opts.VisualMapOpts(type_="size", max_=max_y, min_=min_y),
        )
        scatter.render("scatter_size.html")



if __name__ == '__main__':
    pass

