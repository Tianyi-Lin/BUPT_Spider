import requests
from bs4 import BeautifulSoup as bs


def getLt(str):
    lt = bs(str, 'html.parser')
    dic = {}
    for inp in lt.form.find_all('input'):
        if (inp.get('name')) != None:
            dic[inp.get('name')] = inp.get('value')
    print(dic)
    return dic


headers_for_login_get = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Cookie': 'pgv_pvi=6059785216; Hm_lvt_41e71a1bb3180ffdb5c83f253d23d0c0=1598852977; JSESSIONID=00019OOH-S1_FRM8aOKH9kMnxJA:2K7JFRR7T9',
    'Host': 'auth.bupt.edu.cn',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'
}


headers_for_login_post = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Content-Length': '119',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'pgv_pvi=6059785216; Hm_lvt_41e71a1bb3180ffdb5c83f253d23d0c0=1598852977; JSESSIONID=00019OOH-S1_FRM8aOKH9kMnxJA:2K7JFRR7T9',
    'Host': 'auth.bupt.edu.cn',
    'Origin': 'http://auth.bupt.edu.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'
}


headers_for_login_post_again = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Content-Length': '119',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': 'pgv_pvi=6059785216; Hm_lvt_41e71a1bb3180ffdb5c83f253d23d0c0=1598852977; JSESSIONID=00019OOH-S1_FRM8aOKH9kMnxJA:2K7JFRR7T9',
    'Host': 'auth.bupt.edu.cn',
    'Origin': 'http://auth.bupt.edu.cn',
    'Proxy-Connection': 'keep-alive',
    'Referer': 'http://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'
}


get_url = post_url = post_url_again = \
    'http://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fmy.bupt.edu.cn%2Fsystem%2Fresource%2Fcode%2Fauth%2Fclogin.jsp%3Fowner%3D1664271694'
url_redirection = 'http://my.bupt.edu.cn/system/resource/code/auth/clogin.jsp?owner=1664271694&ticket=ST-1513906-oGYIKSLzFye3okyHp3tw-kYhK-cas-1619462693528'

# 通过Session类新建一个会话
session = requests.Session()
# 往下使用requests的地方，直接使用session即可，session就会保存服务器发送过来的cookie信息
res_get = session.get(url=get_url, headers=headers_for_login_get)


dic = getLt(res_get.text)
post_data = {
    'username': '2019210101',  # 此处为你的学号
    'password': 'ty123456',  # 你的密码
    'lt': dic['lt'],
    'execution': dic['execution'],
    '_eventId': dic['_eventId'],
    'rmShown': dic['rmShown']
}


res_post = session.post(url=post_url, data=post_data, headers=headers_for_login_post)
# 上面的session会保存会话，往下发送请求，直接使用session即可

res_post_again = session.post(url=post_url_again, data=post_data, headers=headers_for_login_post)

res_tiaozhuan = session.get(url=url_redirection, data=post_data, headers=headers_for_login_post_again)

print('123')
