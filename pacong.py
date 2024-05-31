import requests
import parsel
import pandas as pd

# 0 设置文件路径
file_path = r"D:\aaa.xlsx"

# 1 请求与响应
url = 'http://category.dangdang.com/pg7-cp01.25.01.00.00.00.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
} #应替换
html_data = requests.get(url=url, headers=headers).text
# print(html_data) #打印响应结果，该网页的文本信息

# 2 解析数据
selector = parsel.Selector(html_data)
lis = selector.css('ul.bigimg li')  # class名为bigimg的ul下的所有li

# 初始化一个空列表来存储 DataFrame
df_list = []
print(len(lis))


for li in lis:

    current_price = ''
    decide_price = ''
    count_price = ''
    author = ''
    publish_time = ''
    publish_house = ''

    title = li.css('.name a::text').get()  #该li下，class名为name的元素下面的a标签文字
    print(title)
    prices = li.css('.price span')
    try: # 有的书没有三个span标签!
        current_price = prices[0].css(' ::text').get()
        decide_price = prices[1].css(' ::text').get()
        count_price = prices[2].css(' ::text').get()
    except IndexError:
        print('IndexError')

    # 出版信息
    spans = li.css('.search_book_author span')
    try:
        author = spans[0].css('::text').get()
        publish_time = spans[1].css('::text').get()
        publish_house = spans[2].css('a::text').get()
    except IndexError:
        print('IndexError')

    data ={
        '标题': title,
        '现价': current_price,
        '定价': decide_price,
        '折扣': count_price,
        '作者': author,
        '发版日期': publish_time,
        '发版社': publish_house
    }
    df_list.append(data)


df = pd.DataFrame(df_list)
df.to_excel(file_path, index=False)
print(f"数据已保存到文件: {file_path}")  # 打印保存数据的文件路径