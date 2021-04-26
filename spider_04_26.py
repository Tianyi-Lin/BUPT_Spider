import requests
import http.cookiejar as cookielib
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import os
import datetime

today = datetime.date.today().isoformat()  # 日期格式 2021-05-07
# 在桌面建立一个文件夹用于储存文件
folder_path = r'C:\Users\15966\Desktop\BUPTspider' + today + "/"
if not os.path.exists(folder_path):
    os.makedirs(folder_path)


# ---------------------------------------------------------
def getLt(str):
    lt = bs(str, 'html.parser')
    dic = {}
    for inp in lt.form.find_all('input'):
        if (inp.get('name')) != None:
            dic[inp.get('name')] = inp.get('value')
    print(dic)
    return dic
# ----------------------------------------------------------


# 模拟一个浏览器头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'
}

# setting cookie
s = requests.Session()
s.cookies = cookielib.CookieJar()
r = s.get('http://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694',
          headers=header)
dic = getLt(r.text)

postdata = {
    'username': '2019210101',  # 此处为你的学号
    'password': 'ty123456',  # 你的密码
    'lt': dic['lt'],
    'execution': dic['execution'],
    '_eventId': 'submit',
    'rmShown': '1'
}

# 携带登陆数据，以post方式登录，
response = s.post('http://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694',
                  data=postdata, headers=header)

# 用get方式访问“校内通知”的页面
header_get = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'JSESSIONID=4E3E6FF3FFFA796241DC1543107F1FA3',
    'Host': 'my.bupt.edu.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1524',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
}
res = s.get('http://my.bupt.edu.cn/list.jsp?urltype=tree.TreeTempUrl&wbtreeid=1154', headers=header_get)
# 用beautifulsoup解析html
soup = bs(res.text, 'html.parser')
# print(soup)

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



