# affiliation

![aff1](img/aff1.jpg)

## 简介

> <font color=red>affiliation 项目是基于很多主流的 Python 第三方库开发的</font>

<font color=red>主要封装了日常生活中可能会经常使用的函数,如控制键盘,终端美化,Excel 读取写入,简单数据分析,可视化分析,图片处理(视觉处理)等等</font>

`affiliation API` 它能为你在以下场景提供相对的便利:

1. 终端的美化

2. **<font color=green>Excel 表格的快速读写</font>**

3. 键盘的控制

4. **<font color=green>制作可视化图表</font>**

5. 数据分析

6. 视觉处理 (待完善)

7. 深度学习 (待开发)

## 安装

1. 去`Github`/`Gitee` 下载应的源码包
2. 安装相关`Python`依赖项

```shell
# 打开cmd进入到源码包目录后执行以下命令
pip install -r requirements.txt
# 如果网速较慢,可以试着使用以下方法(使用阿里源)
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

3. 将源码放入`python` 的默认第三方库的目录下

```python
# 默认为:
C:\Users\86178\AppData\Local\Programs\Python\Python36\Lib\site-packages
# 86178 对应你主机的用户名
# Python36 对应你使用的python解释器的版本
```

## 快速使用

### 终端美化

> <font size=4 color=red>!</font> <font color=red>终端美化,主要使用了 rich 库,但 rich 库不支持对 Console 美化,所以有一些函数不支持在 Console 下使用\_如以下函数:</font>

- `form_list`
- `form_dict`
- 等一些特殊颜色的输出

#### 美化列表

![aff2](img/aff2.png)

使用场景:

- 一般爬虫爬取的数据可以存放在一个列表里,而列表里一般都是字典(键值对),这时就可以使用 _`form_list`_ 这个函数对其进行美化输出,简单分析爬虫数据.

示例:

```python
from affiliation import embellish

dict1 = {'name':'Busy To Live','gender':'boy','grade':0,'birthday':'2002-09-08','mood':'blue','fans':0,'teacher':'myself','stuid':32}
embel ish.form_dict(dict1)

```

#### 美化字典

![aff3](img/aff3.png)

#### Console 彩色输出

对于别的第三方库一般都是

> 默认使用`embelish`模块里面的`printf函数`进行终端/控制台颜色输出,你也可以通过重构 print 函数来实现

![aff4](img/aff4.png)

### 可视化图表

#### 柱状图

如果需要更自由的可视化图表设计,可以去参考 pyecharts 官网: [pyecharts 的官方网站](https://pyecharts.org/#/)

> <font size=4 color=red>!</font> 此模块几乎完全使用 pyecharts 开发的.

**示例代码:** [演示网页](dicts\bar_time.html)

```python
from analyse import File
from cv import *

if __name__ == '__main__':


    file1 = File('./dicts/data_site/spider.xlsx')
    data1 = file1.select_col('原价')
    data2 = file1.select_col('目前价格')
    price_percentage = [round(b / a, 2) for a, b in zip(data1, data2)]
    res_x = [i for i in set(price_percentage)]
    res_x.sort()
    res_y = [price_percentage.count(i) for i in set(price_percentage)]
    chart1 = BarChart()
    chart1.tool_box = True
    chart1.slope = 25
    chart1.chart_subtitle = '打折图'
    chart1.visual_map = True
    chart1.mark_point = False
    chart1.x_data = res_x
    chart1.y_data = res_y
    chart1.bar_time('number')

```

<img src="img/aff6.png" alt="aff6" style="zoom:33%;" />

> 当有多列数据时,只要在设置 y 轴数据时将其转换成一个嵌套列表即可

示例代码: [演示网站](dicts\bar_time_2.html)

```python
from cv import BarChart
from pyecharts.globals import ThemeType

if __name__ == '__main__':
    y = [65, 46, 5, 55, 88, 10, 20, 25, 45, 78, 24, 88]
    y2 = [20, 32, 120, 33, 33, 47, 30, 35, 123, 28, 44, 100]
    x = ['橘子', '石榴', '柠檬', '火龙果', '樱桃', '苹果', '梨', '桃子', '山竹', '西瓜', '草莓', '葡萄']
    bar = BarChart()
    bar.chart_title = '水果销量'
    bar.theme = ThemeType.VINTAGE
    bar.x_data = x
    bar.xaxis_name = '水果种类'
    bar.y_data = [y, y2] # 将两列数据合并成列表
    bar.yaxis_name = '销量'
    bar.tool_box = True  # 设置右边的工具栏
    bar.mark_point = True  # 设置标记点
    bar.mark_line = False
    bar.bar_time()

```

<img src="img/aff13.png" alt="aff13"/>

![aff12](img/aff12.png)

**| 结合 `analyse`模块制作可视化图表**

示例代码

```python
from analyse import File
from cv import BarChart

if __name__ == '__main__':
    # 使用File类创建文件对象
    file1 = File('./dicts/data_site/spider.xlsx')
    dict_data = file1.count('出版社')
    bar = BarChart()
    bar.data = dict_data  # 设置数据
    bar.slope = 10  # 设置x轴数据的斜度(默认为顺时针方向)
    bar.tool_box = True  # 设置右边的工具栏
    bar.mark_point = True  # 设置标记点
    bar.mark_line = True  # 设置标记线
    bar.bar_time()
```

![aff6](img/aff7.png)

#### 饼图

**示例代码**

```python
from cv import PieChart
if __name__ == '__main__':
    y = [10, 20, 25, 45, 78, 24]
    x = ['苹果', '梨', '桃子', '山竹', '西瓜', '草莓']
    pie = PieChart()
    pie.x_data = x
    pie.y_data = y
    # 也可以使用 pie.data =  (zip(x,y))
    pie.visual_map = True
    pie.pie_rose('日销售量')

```

![aff6](img/aff9.png)

示例代码:

```python
from cv import PieChart
from pyecharts.globals import ThemeType
if __name__ == '__main__':
    y = [10, 20, 25, 45, 78, 24]
    x = ['苹果', '梨', '桃子', '山竹', '西瓜', '草莓']
    pie = PieChart()
    pie.theme= ThemeType.DARK # 使用黑色主题
    # (对应的主题可以去pyecharts官网查看)
    pie.x_data = x
    pie.y_data = y
    pie.pie_doughnut("日销售量")

```

### 操作 Excel

你只要使用以下代码就能实现用 python 对`excel`,`csv` 格式的数据进行简单的分析和操作了

示例代码:

```python
from affiliation.analyse import File
# 使用File类创建file对象
excel_file = File("./dicts/data_site/tencent.xlsx")
# csv文件要指定分隔符,若未指定(会提示你输入分隔符)
csv_file = File("./dicts/data_site/hotel_bookings.csv",',')
```

这时你就可以使用这两个文件对象,进行一些数据操作了.

如获取`excel`表的所有行,所有列,某一行,某一列. 等一系列操作

当然如果你能熟练使用 python 的 `pandas` 库进行数据操作的话,只需要调用

```pythhon
excel_file.df # 数据类型为pandas的dataframe
```

### 日志记录

使用日志模块

示例代码:

```python
from affiliation.log import Log # 引入Log类
log1 = Log()  # 单例模式创建对象
log1.error()
log1.process()


#  对于log级别强的如(error,admonition,等会有报错行号)
log1.error("Your input data is error!")
log1.info("请等待一段时间,数据正在导入..") # 可以在里面接 str类型的数据,用户指定输出

```

![aff5](img/aff5.png)

### 图像处理

> <font color=red size=5>!</font> <font face=楷体 color=red>这个模块还未完全完善,但对图像处理(opencv)的大部分操作进行了封装和简化 (后续也会进行完善)</font>

```python
from affiliation.picop import Picture

if __name__ == '__main__':

    pic1 = Picture(r'.\img\test.png') # 实例化对象
    pic1.gray() # 灰度化
    pic2.show() # 显示图片(默认为matplotlib方式显示)
    # pic2.show('cv') # 以cv2的方式显示图片



```

**得到灰度图**

![raw_img](README.assets/raw_img.png)

```python
pic1.binarization() # 对图像进行二值化
pic1.show()
```

我们只需要调用`binarization`这个函数就能获得二值化图像,但得到的图像有很多噪声

我们可以试着使用腐蚀和膨胀操作进行过滤这些噪声

![binarization](README.assets/binarization.png)

```python
pic1.dilate()
pic2.erosion()
```

腐蚀操作

![dilate](README.assets/dilate.png)

膨胀操作

![result](README.assets/result.png)

## API

### ==analyse.py==

#### File 类

```python
from affiliation.analyse import File
# 使用File类创建file对象
excel_file = File("./dicts/data_site/tencent.xlsx")
```

##### head

返回值类型: `list`

作用: 返回 Excel 文件的列名,csv 文件的第一行

```python
result = excel_file.head
```

##### all_row

返回值类型: `numpy.ndarray`

```python
result = excel_file.all_row # 返回所有行
```

##### average()

返回值类型: `int`

```
result = excel_file.average('可计算的列名')
```

##### col_number

返回值类型: `int`

作用: 返回文件的列数

##### row_number

返回值类型: `int`

作用: 返回文件的行数

##### select_col

返回值类型 numpy.ndarray`

作用:选择某一行的数据

```python
# 函数原型

```

### ==excel.py==

> excel.py 里封装了许多对 excel 表格的基本操作

### ==log.py==

> log.py 里封装了一些日志输出函数

#### Log 类

##### complete

##### debug

##### error

##### process

##### warning

### ==embellish.py==

> 封装了一些 console 和终端的美化函数

### base.py

> 封装了一些库内经常使用的基础函数

### kbdc.py

> 封装了对键盘进行控制的基本操作

### ==Picop.py==

#### Picture

> Picture 类内置多种图像操作的方法

##### trace_log

查看图像进行了哪些操作

##### trace_back

还原图像操作

##### gray

```python
# 原型
def gray(self, trace_back_save=True):
    pass
```

类型: 方法

用法:

```python
# 获得图像的灰度图
# "Object"必须为Picture类创建的对象
"Object".gray() # 无返回值
```

##### hsv

对图像进行 HSV 变换

##### binarization

<font color=red>对图像进行二值化处理</font>

##### thresh

设置卷积核的大小

##### erosion

腐蚀操作

##### dilate

膨胀操作

##### black_hat

黑帽操作

##### top_hat

顶帽操作

##### canny_detection

`canny`检测

##### edge_detection

边缘检测

##### open_operation

开操作

##### close_operation

闭操作

##### mean_filter

均值滤波

##### gaussian_filter

高斯滤波

##### median_filter

中值滤波

##### show_all_filter

查看全部滤波对这张图片的操作(一般用来对比)

##### pyrUP

金字塔操作

##### pyrDown

##### show

图片展示

##### sobel_operator

`sobel` 算子

##### scharr_operator

`scharr` 算子

##### laplacian_operator

拉普拉斯算子

##### operator_show

查看所有算子对图像的操作

##### contours

轮廓绘制

##### find_contours

##### draw_specific_contour

绘制特定轮廓

##### draw_all_contour

画出所有轮廓

##### approx_contour

##### contour_area

算出轮廓面积

##### contour_length

算出轮廓周长

##### save

保存操作后的图片

#### Operator

> Operator 类用来记录用户图像操作的历史

```python
# 类型: numpy.ndarray
```

#### 类外方法

### ==cv.py==

> ​

### sv.py

> ​

---

### <font color=purple>myutils.py</font>

>
