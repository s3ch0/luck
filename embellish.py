from typing import Union,List
from rich.table import Table
from rich.console import Console



class Color:
        # 定义颜色类型
        colors = {  # Format: (ansi, pygments)
            # foreground
            "white": ("", "#white"),
            "text": ("", "#text"),
            "success": ("\033[32m\033[1m", "#success"),
            "black": ("\033[30m", "#ansiblack"),
            "red": ("\033[31m", "#ansired"),
            "error": ("\033[31m", "#error"),
            "danger": ("\033[31m\033[1m", "#danger"),
            "green": ("\033[32m", "#ansigreen"),
            "complete": ("\033[32m", "#ansigreen"),
            "yellow": ("\033[33m", "#ansiyellow"),
            "orange": ("\033[33m", "#ansiyellow"),
            "admonition": ("\033[33m", "#admonition"),
            "blue": ("\033[34m", "#ansiblue"),
            "default": ("\033[34m", "#ansiblue"),
            "purple": ("\033[35m", "#ansipurple"),
            "warning": ("\033[35m", "#ansipurple"),
            "cyan": ("\033[36m", "#ansicyan"),
            "info": ("\033[36m", "#ansicyan"),
            "grey": ("\033[37m", "#asiwhite"),
            "reset": ("\033[39m", "noinherit"), }
        background = {
            "bg_black": ("\033[40m", "bg:#ansiblack"),
            "bg_red": ("\033[41m", "bg:#ansired"),
            "bg_green": ("\033[42m", "bg:#ansigreen"),
            "bg_yellow": ("\033[43m", "bg:#ansiyellow"),
            "bg_blue": ("\033[44m", "bg:#ansiblue"),
            "bg_purple": ("\033[45m", "bg:#ansipurple"),
            "bg_cyan": ("\033[46m", "bg:#ansicyan"),
            "bg_grey": ("\033[47m", "bg:#ansiwhite"),
            "bg_reset": ("\033[49m", "noinherit"), }
        specials = {
            "normal": ("\033[0m", "noinherit"),  # color & brightness
            "bold": ("\033[1m", "bold"),
            "underline": ("\033[4m", "underline"),
            "blink": ("\033[5m", ""),
            "invert": ("\033[7m", ""),
        }

        def __init__(self):
            self.__color_list:list = list(self.colors.keys()) 
            self.__background_list:list = list(self.background.keys())
            self.__specials_list:list = list(self.specials.keys())
            self.all_list:list = self.color_list + self.background_list + self.specials_list
            self.__cash:list = []

        @property
        def color_list(self)->list:
            return self.__color_list

        @property
        def background_list(self)->list:
            return self.__background_list

        @property
        def specials_list(self)->list:
            return self.__specials_list

        def __repr__(self):
            return "<Color>"

        def __getattr__(self, attr):
            return self.colors.get(attr, [""])[0]

        def __str__(self):
            return 'colors:' + str(self.color_list) + '\n' + ' background:' + str(
                self.background_list) + '\n' + ' specials:' + str(self.specials_list)

        def ansi_to_pygments(self, x):  # Transform ansi encoded text to Pygments text  # noqa: E501
            inv_map = {v[0]: v[1] for k, v in self.colors.items()}
            for k, v in inv_map.items():
                x = x.replace(k, " " + v)
            return x.strip()
  
        # 获取相应的颜色码函数
        def get(self, theme: Union[list, str]):
            # 待开发(或许可以将可迭代对象都加入到 get 函数里如 tuple)
            # if the the theme is just a single style (the parameter is the style of str)
            if isinstance(theme, str) and theme in self.all_list:
                if theme.startswith('bg_'):
                    return self.background.get(theme, [""])[0]
                elif theme in self.colors:
                    return self.colors.get(theme, [""])[0]
                else:
                    return self.specials.get(theme, [""])[0]
            elif isinstance(theme, list):
                if len(theme) == 1 and theme[0] in self.all_list:
                    return self.colors.get(theme[0], [""])[0]
                elif len(theme) > 1:
                    for i in theme:
                        if i in self.all_list:
                            self.__cash.append(i)
                        else:
                            pass
                    tmp_set = set(self.__cash)  # 去重(这边还是颜色名字)
                    tmp_list = []  # 存储颜色码
                    result_str = ''  # 将其转换为字符串型
                    for i in tmp_set:
                        if i in self.color_list:
                            tmp_list.append(self.colors.get(i)[0])
                        elif i in self.background_list:
                            tmp_list.append(self.background.get(i)[0])
                        elif i in self.specials_list:
                            tmp_list.append(self.specials.get(i)[0])
                    for i in tmp_list:
                        result_str = result_str + i
                    return result_str

                else:

                    pass
            else:
                print("\033[31m\033[1m" + 'Some error in getting the colors style!')
                print("\033[31m\033[1m" + 'Or maybe there is no such color style!')
                return 1

        def init(self):
            # 初始化颜色
            print(self.get(['reset', 'bg_reset', 'normal']),end='')

    
__MY_COLOR = Color()

def printf(*args,color:Union[str,List[str]]='default',**argv)->None:
    temp_list = []
    for i in range(len(args)):
        if i == 0:
            temp_list.append(str(__MY_COLOR.get(color))+str(args[i]))
        else:
            temp_list.append(args[i])
    print(*tuple(temp_list),**argv)
    __MY_COLOR.init()
    return None



console = Console()
def form_list(args, color: Union[str, list] = "default"):  # 创建表格的函数
    global table
    if isinstance(args, list):  # 如果传过来的参数为列表
        table = Table(show_header=True, header_style="bold magenta", show_lines=True)  # 创建表头
        tmp_column = args[0]  # 去第一个列表元素
        # !表格颜色渲染
        if isinstance(color, str):
            for column in enumerate(tmp_column.keys()):
                table.add_column(str(column[1]), style=color)  # 取第一个列表元素字典中的所有key值作为表头
        elif isinstance(color, list):
            if len(color) == 1:
                for column in enumerate(tmp_column.keys()):
                    table.add_column(str(column[1]), style=str(color))  # 取第一个列表元素字典中的所有key值作为表头
            if len(color) > 1:
                for column in enumerate(tmp_column.keys()):
                    if len(color) == 0:  # 判断列表是否为空
                        table.add_column(str(column[1]), style='default')  # 取第一个列表元素字典中的所有key值作为表头
                    else:
                        tmp_color = color.pop(0)
                        table.add_column(str(column[1]), style=str(tmp_color))  # 取第一个列表元素字典中的所有key值作为表头
            else:
                for column in enumerate(tmp_column.keys()):
                    table.add_column(str(column[1]), style='default')  # 取第一个列表元素字典中的所有key值作为表头
        # 增加行数
        for column2 in args:  # 遍历列表
            str_dict = str(column2.values())
            right_index = str_dict.rfind(']')
            left_index = str_dict.find('[')
            result = str_dict[left_index + 1:right_index]  # 截取字典中的值
            result_list = result.split(',')  # 获取所有字典中所有value值,并以列表存储.
            result_tuple = tuple(result_list)
            table.add_row(*result_tuple)  # 根据列数添加结果(拆包)
    pass

    console.print(table, justify="center")  # 设置表格在显示屏居中,并打印


# 可优化
def form_dict(args):  # 字典类型建表
    global table
    if isinstance(args, dict):  # 判断类型
        table = Table(show_header=True, header_style="bold magenta")

        column_one = input("Please enter the first column name:")
        column_two = input("Please enter the second column name:")
        table.add_column(column_one, style="info", width=20)
        table.add_column(column_two, style="red", width=20)
        for key, value in args.items():
            table.add_row(str(key), str(value))

        console.print(table, justify="center")  # 设置表格在显示屏居中,并打印





