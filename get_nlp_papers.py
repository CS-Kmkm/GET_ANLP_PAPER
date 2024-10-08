import requests
from bs4 import BeautifulSoup

# proceedingsのURL
URL = "https://www.anlp.jp/proceedings/annual_meeting/{}/{}"
PROGRAM = "html/program.html"
BODY = "html/body.html"

def get_soup(year:int, html:str=""):
    response = requests.get(URL.format(year, html))
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

"""
html: urlのhtmlの部分
author_num: authorのtrまでの距離
title_tag : titleのtag
pid_class : プログラムのidを指定するために利用されているクラス名
2014~2024(2022以外)：html = "", author_num = 1, title_tag='span', pid_class = 'pid'
(get_paper_2015.py)
2022：html = "", author_num = 2, title_tag='span', pid_class = 'pid'
(get_paper_2022.py)(一部筆者が取れてない場合がある。)
2014：html = "", author_num = 1, title_tag='a', pid_class = 'pid'
2006~2013：html = PROGRAM, author_num = 1, title_tag='span', pid_class = 'pid'
(get_paper_2006.py)
2005: html=BODY, author_num=1, title_tag='a'
(get_nlp_papaer_2005.py)
1995~2004：html = "", author_num = 1, title_tag='span', pid_class = 'paper_id'
(get_paper_1995.py)

"""

def get_nlp_papers(word: str, year: int, html:str, author_num:int, title_tag:str='span', pid_class:str = 'pid'):
    soup = get_soup(year, html)
    papers = []

    rows = soup.find_all('tr')
    for i in range(len(rows)):
        is_pid = rows[i].find('td', class_=pid_class)
        if is_pid:
            pid_id = is_pid.text
            title_candidate = rows[i].find(title_tag, class_='title')
            if title_candidate:
                title = "".join(title_candidate.text.split())
                if word in title:
                    td = rows[i+author_num]
                    authors = ''.join(td.text.split())
                    
                    papers.append({
                        'title': title,
                        'authors': authors,
                        'pdf_tag': pid_id
                    })
        else:
            continue

    print(f"### NLP{year}")
    for paper in papers:
        if not paper['title']:
            continue
        paper_url = URL.format(year, f"pdf_dir/{paper['pdf_tag']}")
        print(f"[{paper['title']}]({paper_url})")
        print(f"\t {paper['authors']}")

# ANLPのhtmlの形式に合わせた辞書の指定
args = [
        {"year": 1995, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'paper_id'},
        {"year": 1996, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'paper_id'},
        {"year": 1997, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'paper_id'},
        {"year": 1998, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'paper_id'},
        {"year": 1999, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'paper_id'},
        {"year": 2000, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'paper_id'},
        {"year": 2001, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'paper_id'},
        {"year": 2002, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'paper_id'},
        {"year": 2003, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'paper_id'},
        {"year": 2004, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'paper_id'},
        {"year": 2005, "html":BODY, "author_num": 1, "title_tag":'a', "pid_class": 'pid'},
        {"year": 2006, "html":PROGRAM, "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2007, "html":PROGRAM, "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2008, "html":PROGRAM, "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2009, "html":PROGRAM, "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2010, "html":PROGRAM, "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2011, "html":PROGRAM, "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2012, "html":PROGRAM, "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2013, "html":PROGRAM, "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2014, "html" : "", "author_num": 1, "title_tag":'a', "pid_class": 'pid'},
        {"year": 2015, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2016, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2017, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2018, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2019, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2020, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2021, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2022, "html" : "", "author_num": 2, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2023, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'pid'},
        {"year": 2024, "html" : "", "author_num": 1, "title_tag":'span', "pid_class": 'pid'}
        ]

for arg in args[::-1]:
    get_nlp_papers('攻撃性', **arg)
