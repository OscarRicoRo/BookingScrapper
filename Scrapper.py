import urllib.request
import pandas as pd
from bs4 import BeautifulSoup
import re


# PROXYS: 'http://169.57.1.85:8123', 'http://92.205.22.114:38080', 'http://49.0.2.242:8090', 'http://85.60.193.39:55443', 'http://133.242.171.216:3128'

def get_nombre(url):
    nombre = re.findall(r'(?<=hotel/es/)(.*)(?=\?)', url)
    return nombre[0]


def get_aid(url):
    aid = re.findall(r'(aid=\d+)', url)
    return aid[0]


def get_sid(url):
    sid = re.findall(r'(?<=aid=)(.*)(?=&ucfs)', url)
    return sid[0]


def scrapper(url, filename):
    page = 1
    df = pd.DataFrame(
        columns=['author', 'date', 'country', 'titulo', 'calificacion', 'pos review', 'neg review']
    )
    name = get_nombre(url)
    aid = get_aid(url)
    sid = get_sid(url)
    reviews = [0]
    while reviews:
        scrap_url = f'https://www.booking.com/reviews/es/hotel/{name}?aid={aid}&sid={sid}&customer_type=total&hp_nav=0&old_page=0&order=featuredreviews&page={page}&r_lang=es&rows=25&srpvid=bbed5277667202b3&'.format(
            name=name, aid=aid, sid=sid, page=page)
        proxy_handler = urllib.request.ProxyHandler({'http': 'http://169.57.1.85:8123'})
        opener = urllib.request.build_opener(proxy_handler)
        req = urllib.request.Request(
            scrap_url,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36',
            }
        )

        f = opener.open(req)
        soup = BeautifulSoup(f.read().decode('utf-8'), 'html.parser')
        reviews = soup.findAll("li", {"class": "review_item"})

        for review in reviews:
            date = review.find("p", {"class": "review_item_date"}).text
            author = review.find("div", {"itemprop": "author"}).find("span", {"itemprop": "name"}).text
            if review.find("span", {"itemprop": "nationality"}):
                country = review.find("span", {"itemprop": "nationality"}).find("span", {"itemprop": "name"}).text
            else:
                country = ""
            calificacion = review.find("span", {"class": "review-score-badge"}).text
            if review.find("div", {"class": "review_item_header_content"}).find("span", {"itemprop": "name"}):
                titulo = review.find("div", {"class": "review_item_header_content"}).find("span",
                                                                                          {"itemprop": "name"}).text
            else:
                break
            if review.find("p", {"class": "review_pos"}):
                review_pos = review.find("p", {"class": "review_pos"}).find("span", {"itemprop": "reviewBody"}).text
            else:
                review_pos = ""
            if review.find("p", {"class": "review_neg"}):
                review_neg = review.find("p", {"class": "review_neg"}).find("span", {"itemprop": "reviewBody"}).text
            else:
                review_neg = ""
            temp = pd.DataFrame([[author.strip(), date.strip(), country.strip(), titulo.strip(), calificacion.strip(),
                                  review_pos.strip(), review_neg.strip()]],
                                columns=['author', 'date', 'country', 'titulo', 'calificacion',
                                         'pos review', 'neg review'])
            df = pd.concat([df, temp], ignore_index=True)
        page += 1
    df.to_csv(filename + '.csv', encoding='utf-8')
