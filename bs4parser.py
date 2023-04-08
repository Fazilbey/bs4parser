import requests
from bs4 import BeautifulSoup
from Article import Article
import datetime
from db import DB
baseurl='"https://nur.kz/'
url="https://nur.kz/latest/"
article_objects=[]


response=requests.get(url)
name = 'NUR.KZ'
titul=''
top_tag='<a class="article-preview-category__content" >'
bottom_tag='<h2 class="article-preview-category__subhead"></h2>'
title_cut='<h2 class="article-preview-category__subhead"></h2>'
date_cut='<div class="article-preview-category__date"></div>'


soup=BeautifulSoup(response.text , 'html.parser')
titul+=soup.find('title').text

article=soup.find_all('article')

for all in article :
    title=(all.h2.text or all.h3.text or all.h4.text).strip()
    time=(all.time[ 'datetime' ]).strip()
    link=(all.a[ 'href' ]).strip()
    if (title or time or link) is not None :
        obj=Article(title, time , link, "")
        article_objects.append(obj)

    else :
        raise Exception("Sorry, check data again")

for i in range(len(article_objects)):
    new_url = article_objects[i].link

    new_response = requests.get(new_url)


    bs4 = BeautifulSoup(new_response.text, 'html.parser')
    p_tags=bs4.find_all('p' , class_='align-left formatted-body__paragraph')
    texts = ''
    for p in p_tags :
        texts += p.text
    new_article = Article(article_objects[i].title, article_objects[i].date, article_objects[i].link, texts.strip())
    article_objects[i] = new_article

for i in range(len(article_objects)):
    print(article_objects[ i ].title)
    print(article_objects[i].content)
    print(article_objects[i].date)
    print(article_objects[i].link)


db = DB()
db.insert_to_resource(titul, baseurl, top_tag,bottom_tag,title_cut, date_cut)

for i in range(len(article_objects)):
    dt=datetime.datetime.fromisoformat(f"{article_objects[i].date}")
    unix_time=int(dt.timestamp())

    now_unix=int(datetime.datetime.now().timestamp())

    data=datetime.datetime.fromisoformat(f'{article_objects[i].date}')

    # Convert to year-month-day format
    ymd_str=data.strftime('%Y-%m-%d')
    

    db.insert_into_items(1, article_objects[i].link, article_objects[i].title, article_objects[i].content, unix_time, now_unix, ymd_str)
