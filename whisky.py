import requests,bs4
import pandas as pd
import time
name = []
number = []
date = []
price = []
item_href = []
content = []
other_info = []
page2 = 91
head = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
proxy_id = { "http": "http://61.135.155.82:443"}
cookie = {'session-id':'459-4568418-5692641','ubid-acbcn':'459-5049899-3055220','x-wl-uid':'1AK7YMFc9IzusayDn2fT6Topjz3iAOpR3EeA2UQSqco8fo5PbK2aCpyBA/fdPMfKFqZRHc4IeyuU=','session-token':'OH1wPvfOj6Tylq2nnJcdn5wyxycR/lqyGsGU3+lUtU4mbC0ZD9s8/4Oihd1BlskUQG8zRbLVs9vfWXuiJmnRlDT4x35ircp2uLxOLNYQ4j5pzdFJIqqoZUnhHSJUq2yK80P3LqH8An7faXRCPW9BIqX1wu0WmHlSS9vYAPKA/2SGdV9b//EljYjIVCBjOuR/dKRiYEeGK3li0RJOVz7+vMWg7Rnzbx89QxlbCp0WyquZyVxG6f2mNw=="','session-id-time':'2082787201l'}
####函数
def collectdata(page2):
    url = "https://www.whiskyhammer.com/auction/past/?page=" + str(page2) +"&ps=500"
    r = requests.get(url,headers=head,proxies=proxy_id,cookies=cookie)
    r.encoding = r.apparent_encoding
    soup = bs4.BeautifulSoup(r.text,'html.parser')
    div_1 = soup.find_all('div',class_ = 'innerInfo') #某年份月份的网页
    temp=[]
    for i in div_1:
        name.append(i.h3.a.text)
        number.append(i.span.text)
        date.append(i.div.span.text)
        price.append(i.div.span.next_sibling.next_sibling.span.span.text)
        item_href.append(i.h3.a.get('href'))
        temp.append(i.h3.a.get('href'))
    for url_next in temp:
        r_next = requests.get(url_next,headers=head,proxies=proxy_id,cookies=cookie)
        r_next.encoding = r_next.apparent_encoding
        soup_next = bs4.BeautifulSoup(r_next.text,'html.parser')
        div = soup_next.find_all('div',class_ = 'productDetailsWrap')
        div_other = soup_next.find_all('div',itemprop="description")
        other_info.append(div_other[0].text.replace('\xa0',' '))
        content.append(str(div[0].div.ul.li).replace('<strong>','').replace('</strong>','').replace('</li>','').replace('<li>','#'))
    return name,content,price,date,number,other_info

######循环 需要自己编写循环
while(page2<=94):
    collectdata(page2)
    page2+=1
    
#########
#######路径
dic = {"name":name,"number":number,"date":date,"price":price,"url":item_href,"other_info":other_info,"content":content}
df = pd.DataFrame(dic)
outputpath=r'C:\Users\spy\Desktop\whiskydata\91-94.csv' ###spy自己的路径
df.to_csv(outputpath,sep=',',index=True,header=True,encoding= 'utf_8_sig')
########