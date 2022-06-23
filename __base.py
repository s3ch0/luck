import sys
from typing import Union
from luck.__log import Log
import re

__BASE_LOG = Log()

# 待开发 (对numpy里面的数据类型进行判断,然后进行转换成Python里面的内置数据类型)


# 判断是否为字符串型数字
def is_number(strings):
    try:
        float(strings)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(strings)
        return True
    except (TypeError, ValueError):
        pass

    return False


# 按顺序去重
def de_duplication(item: list):
    # if not isinstance(item[0], str or int):
    new_list = []
    for i in item:
        if i not in new_list:
            new_list.append(i)
    return new_list


# 将字典类型分成两个列表
def separate(item: dict):
    if isinstance(item, dict):
        key_list = [key for key in item.keys()]
        value_list = [
            change_num(value) if is_number(value) else value
            for value in item.values()
        ]
        return key_list, value_list


# 将其他类型的数字转换为对应的类型
def change_num(item: Union[str, int, float]):
    if is_number(item) and isinstance(item, str):
        if type(eval(item)) == int:
            result = int(item)
        elif type(eval(item)) == float:
            result = float(item)
        else:
            result = item
    elif isinstance(item, int):
        result = int(item)
    elif isinstance(item, float):
        result = float(item)
    elif is_number(item):
        result = int(item)
    else:
        result = item
    return result


# 将字符串类型的数字列表转换成对应的类型列表
# 只是单纯地将其中为'数字'的转换 不是数字的保持不变
def change_num_list(item: list):
    result_list = []
    check_out = 0
    for i in item:
        if is_number(i) and isinstance(i, str):
            if type(eval(i)) == int:
                result_list.append(int(i))
            elif type(eval(i)) == float:
                result_list.append(float(i))
            else:
                result_list.append(i)
        elif isinstance(i, float):
            result_list.append(i)
        elif isinstance(i, int):
            result_list.append(i)
        elif is_number(i):
            result_list.append(int(i)) # 这边还有点缺陷(比如别的数据类型但也是数字,不能转换成相应的类型)
        else:
            check_out += 1
            result_list.append(i)
    if check_out != 0:
        __BASE_LOG.warning('The list you passed is not all numbers!')

    return result_list


# 检测元素内是否含有字符串或别的类型 有返回->False ,没有返回->True
def type_check(item: list):
    for i in item:
        if not isinstance(i, int) and not isinstance(i, float):
            return False
    else:
        return True


# 返回字符串的变量类型
def show_type(item):
    type_str = str(type(item)).split('\'')[1]
    return type_str


def merge(item):
    pass


def gain_list_max_index(item: list):
    if isinstance(item, list):
        res = [i for i, v in enumerate(item) if v == max(item)]
        return res
    else:
        __BASE_LOG.error('Type error')
        sys.exit(1)


# 判断文件类型
def file_suffix(item: str):
    if isinstance(item, str):
        if re.search("\.", item) is not None:
            tmp_list = item.split('.')
            return tmp_list[-1]
        else:
            pass
            __BASE_LOG.warning('What you passed is not a complete file name!')
        pass
    else:
        __BASE_LOG.error('Type error')
        sys.exit(1)


def gain_file_name(path: str):
    shard_path = path.split("/")
    return shard_path[-1]


def split_list_str(item: list, condition='end', strings='px'):
    index_list = []
    result_res = []
    for k, v in enumerate(item):
        if condition == 'end':
            if is_number(v):
                result_res.append(v)
            elif v.endswith(strings):
                index_list.append(k)
                tmp_list = v.split(strings)
                result_res.append(tmp_list[0])

        elif condition == 'start':
            if is_number(v):
                result_res.append(v)
            elif v.startswith(strings):
                index_list.append(k)
                tmp_list = v.split(strings)
                result_res.append(tmp_list[-1])

    return [index_list, result_res]


if __name__ == '__main__':
    __BASE_LOG.warning()
