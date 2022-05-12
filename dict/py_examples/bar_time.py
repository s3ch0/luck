from analyse import File
from draw2 import *

file1 = File('./spider.xlsx')
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

