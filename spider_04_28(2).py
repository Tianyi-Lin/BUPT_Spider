import requests
import re
import http.cookiejar as cookielib
from bs4 import BeautifulSoup as bs


def get_lt(str):
    lt = bs(str, 'html.parser')
    dic = {}                                    # 字典
    for inp in lt.form.find_all('input'):
        if (inp.get('name')) != None:
            dic[inp.get('name')] = inp.get('value')
    print(dic)
    return dic


# ------------------------------------------------------
# 通过Session类新建一个会话
session = requests.Session()
# 往下使用requests的地方，直接使用session即可，session就会保存服务器发送过来的cookie信息

url1 = 'http://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694'
# Q1：为什么url='http://auth.bupt.edu.cn/authserver/login'不可以登录

headers1 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
}
res_get1 = session.get(url=url1, headers=headers1)

# 通过第一次get获取post_data中的lt值等
dic = get_lt(res_get1.text)
post_data1 = {
    'username': '2019210101',  # 此处为你的学号
    'password': 'ty123456',  # 你的密码
    'lt': dic['lt'],
    'execution': dic['execution'],
    '_eventId': dic['_eventId'],
    'rmShown': dic['rmShown']
}

res_post1 = session.post(url=url1, data=post_data1, headers=headers1)
# 上面的session会保存会话，往下发送请求，直接使用session即可

# Q2：如何获得post应答报文header中的Location中的重定位地址
# 答：在res_post1.history[0].headers['Location']中，有两个重定向地址
url_relocated1 = res_post1.history[0].headers['Location']
url_relocated2 = res_post1.history[1].headers['Location']

res_relocated1 = session.get(url=url_relocated1, headers=headers1)
res_relocated2 = session.get(url=url_relocated2, headers=headers1)


JSESSIONID_pre = ''.join(session.cookies.items()[2])
str_list = list(JSESSIONID_pre)
equ = '='
str_list.insert(10, equ)
JSESSIONID = ''.join(str_list)

headers_home = {
    'JSESSIONID': JSESSIONID,
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
}

res_home = session.get(url='http://my.bupt.edu.cn/xs_index.jsp?urltype=tree.TreeTempUrl&wbtreeid=1541')
# 第一次session.get的url是跟随重定向到'http://my.bupt.edu.cn/system/resource/code/auth/clogin.jsp?owner=1664271694'
res_home = session.get(url='http://my.bupt.edu.cn/xs_index.jsp?urltype=tree.TreeTempUrl&wbtreeid=1541')
# 第二次session.get的url才是'http://my.bupt.edu.cn/xs_index.jsp?urltype=tree.TreeTempUrl&wbtreeid=1541'

# # 用beautifulsoup解析html
# soup = bs(res_home.text, 'html.parser')
# print(soup)


# 从resonance中得知新闻页的url一般格式为：'http://my.bupt.edu.cn/list.jsp?totalpage=1047&PAGENUM=1&urltype=tree.TreeTempUrl&wbtreeid=1154'
# 其中PAGENUM=1表示第一页，故构造如下新闻页url列表
res_temp = session.get(url='http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1154')
soup_temp = bs(res_temp.text, 'html.parser')

# class = "p_t"携带总页数
total_page_number = int(soup_temp.select('.p_t')[1].text[1:5])

# 构造新闻页url列表
url_list_of_newspage = []
for n in range(1, total_page_number+1):
    url_list_of_newspage.append('http://my.bupt.edu.cn/list.jsp?totalpage=1047&PAGENUM=' + str(n) + '&urltype=tree.TreeTempUrl&wbtreeid=1154')


# 保存新闻标题，作者，时间的列表
news_title = []
url_news_content = []
# 新闻正文文字
news_content_text = []
# 新闻正文图片
news_content_img = []
author = []
date = []


# 爬取一页新闻页中的所有新闻标题
def spider_onepage_news_title(url_news_page):
    res_news = session.get(url_news_page)
    # 用beautifulsoup解析html
    soup = bs(res_news.text, 'html.parser')
    for raw_news_title in soup.find_all(href=re.compile("xntz_content")):
        # 将新闻标题存到列表news_title
        news_title.append(raw_news_title['title'])
        # 将每条新闻正文对应url存到列表url_news_content
        url_news_content.append('http://my.bupt.edu.cn/' + raw_news_title['href'])
    for raw_author in soup.find_all(class_='author'):
        author.append(raw_author.string)
    for raw_time in soup.find_all(class_='time'):
        date.append(raw_time.string)


def spider_all_news_title(maxpage_to_spider: int):
    # 循环爬取第1页到第the_maxpage_to_spider页的新闻，每一页有20条新闻消息
    for m in range(0, maxpage_to_spider):
        url = url_list_of_newspage[m]
        spider_onepage_news_title(url)


def spider_all_news_content(url_news_content: list):
    # 循环爬取新闻的内页正文
    # url_contnet是每个新闻内页的url地址
    for url_content in url_news_content:
        res_news_content = session.get(url_content)
        # 用beautifulsoup解析html
        soup_content = bs(res_news_content.text, 'html.parser')
        # content是正文的全部内容，包含标题，文字和图片,name = 'articlecontent'
        for content in soup_content.find_all("div", {"name": "articlecontent"}):
            # 从content中筛选出文字存入news_content_text
            news_content_text.append(content.select('.v_news_content')[0].text)
            # 注意class="v_news_content"只有一个，所以list只有一个元素，用[0]选中

            img_url_list_raw = content.select("img", src=re.compile("/__local"))
            # 注意select("img", src=re.compile("/__local"))有多个，所以list有多个元素，需要循环筛选orisrc对应的图片url地址
            if len(img_url_list_raw) != 0:
                for n in range(0, len(img_url_list_raw)):
                    # 从content中筛选出图片url地址存入news_content_img
                    # 图片url的格式：http://my.bupt.edu.cn/__local/B/C9/7D/DE7F3DCC26ECCD12F993FC1E7C7_176624D1_301C2.png
                    news_content_img.append('http://my.bupt.edu.cn' + img_url_list_raw[n]['orisrc'])


def print_news(maxpage_to_print: int):
    for p in range(0, maxpage_to_print):
        print(news_title[p])
        print(author[p])
        print(date[p])
        print('--------------------------------------------------------')


# 爬取10页的消息并打印
spider_all_news_title(1)
# 一页20条新闻
print_news(1*20)


def find_news(key_word: str):
    # 在新闻中检索消息
    matching = [match_str for match_str in news_title if key_word in match_str]
    print(matching)


spider_all_news_content(url_news_content)

find_news("关于")
# find_news("自习")
# find_news("奖学金")
# find_news("假")
# find_news("评优")

print(news_content_text)
print(news_title)

# # 下一版新闻页的网址
# # 例如第4页的url为：’http://my.bupt.edu.cn/list.jsp?totalpage=1047&PAGENUM=4&urltype=tree.TreeTempUrl&wbtreeid=1154‘
# url_next_news = []
# for next_url in soup.find_all(href=re.compile("totalpage")):
#     url_next_news.append('http://my.bupt.edu.cn/list.jsp' + next_url.attrs['href'])
#
# # 获取当前的新闻页所处的页数
# page_now = list(map(int, soup.select('.p_no_d')[0].contents))[0]
# # 通过soup.select('.p_no_d')[0].contents得到页数，map(int,...)转为int型
# page_next = page_now + 1
