import pymongo
import matplotlib.pyplot as plt
import matplotlib
import re

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.kongjian
collection = db.ss
matplotlib.rcParams['font.sans-serif'] = ['SimHei']


# 使用正则获取年份数据
def get_year_dict(year):
    condition = str(year) + '.*'
    results = collection.find({'time': {'$regex': condition}})
    return results, results.count()


# 使用正则获取月份数据
def get_month_dict(results):
    months = [0] * 13
    for result in results:
        time = result.get('time')
        month = re.match('.*?年(\d+).*', time).group(1)
        months[int(month)] = months[int(month)] + 1
    months = months[1:]
    return months


# 年份条形图
def year_histogram(year_data):
    keys = sorted(year_data.keys())
    values = []
    for key in keys:
        values.append(year_data.get(key))

    rects = plt.bar(x=keys, height=values, align='center')
    # 在每个条形图中显示数据值
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height + 3, str(height), ha='center', va='bottom')
    plt.title('每年说说分布')
    plt.xlabel('年份')
    plt.ylabel('数量')
    plt.show()


# 月份条形图
def month_histogram(month_data, year):
    keys = ['1月', '2月', '3月', '4月', '5月', '6月',
            '7月', '8月', '9月', '10月', '11月', '12月', ]
    values = month_data

    rects = plt.bar(x=keys, height=values, align='center')
    # 在每个条形图中显示数据值
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x() + rect.get_width() / 2, height, str(height), ha='center', va='bottom')
    plt.title(year + '说说分布')
    plt.xlabel('月份')
    plt.ylabel('数量')
    plt.show()


# 年份折线图
def year_line_chart(year_data):
    keys = list(map(int, sorted(year_data.keys())))
    values = []
    for key in keys:
        values.append(year_data.get(str(key)))
    plt.plot(keys, values)
    plt.xticks(keys)
    plt.title('每年说说分布')
    plt.xlabel('年份')
    plt.ylabel('数量')
    plt.show()


# 月份折线图
def month_line_chart(month_data, year):
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    keys = ['1月', '2月', '3月', '4月', '5月', '6月',
            '7月', '8月', '9月', '10月', '11月', '12月']
    values = month_data
    plt.plot(month, values)
    plt.xticks(month, keys)
    plt.title(year + '说说分布')
    plt.xlabel('月份')
    plt.ylabel('数量')
    plt.show()


# 汇总折线图
def all_line_char(year_month_data):
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    keys = ['1月', '2月', '3月', '4月', '5月', '6月',
            '7月', '8月', '9月', '10月', '11月', '12月']
    index = 0
    label = 2012
    for key in sorted(year_month_data.keys()):
        value = year_month_data.get(key)
        plt.plot(month, value, label=label)
        index += 1
        label += 1
    plt.grid()
    plt.ylim(0, 350)
    plt.xticks(month, keys)
    plt.xlabel('月份')
    plt.ylabel('年份')
    plt.title('各年说说分布折线')
    plt.legend(loc='best')
    plt.show()


if __name__ == '__main__':
    year_data = {}
    month_data = {}
    month_data_many = {}
    for i in range(2000, 2020):
        results, num = get_year_dict(i)
        if num:
            year_data[str(i)] = num
            month_data[str(i)] = get_month_dict(results)
            if num >= 200:
                month_data_many[str(i)] = month_data[str(i)]
    year_histogram(year_data)
    for year in sorted(month_data.keys()):
        month_histogram(month_data[year], year=year)
    year_line_chart(year_data)
    for year in sorted(month_data.keys()):
        month_line_chart(month_data[year], year=year)
    all_line_char(month_data_many)