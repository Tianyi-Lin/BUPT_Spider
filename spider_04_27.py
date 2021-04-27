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

res_news = session.get('http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1154')
# 用beautifulsoup解析html
soup = bs(res_news.text, 'html.parser')
print(soup)

news = []
author = []
date = []

for raw_news in soup.find_all(href=re.compile("xntz_content")):
    news.append(raw_news['title'])

for raw_author in soup.find_all(class_='author'):
    author.append(raw_author.string)

for raw_time in soup.find_all(class_='time'):
    date.append(raw_time.string)

print(news)
print(author)
print(date)
