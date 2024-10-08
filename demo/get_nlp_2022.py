import requests
from bs4 import BeautifulSoup

# 指定されたURL
url = "https://www.anlp.jp/proceedings/annual_meeting/{}/"

# 2022年の論文を取得するための関数
def get_nlp_papers_a(year:int= 2022):
    s = 0
    response = requests.get(url.format(year))
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'html.parser')
    papers = []

    rows = soup.find_all('tr')
    for i in range(len(rows)):
        is_pid = rows[i].find('td', class_='pid')
        if is_pid:
            pid_id = is_pid.text
            title_candidate = rows[i].find('span', class_='title')
            if title_candidate:
                title = "".join(rows[i].find('span', class_='title').text.split())
                if '構文' in title:
                    td = rows[i+2]
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
        paper_url = f"https://www.anlp.jp/proceedings/annual_meeting/{year}/pdf_dir/{paper['pdf_tag']}"
        print(f"[{paper['title']}]({paper_url})")
        print(f"\t {paper['authors']}")

# 2022は対応
# for i in range(2024, 1994, -1):
get_nlp_papers_a(2022)
