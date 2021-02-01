import requests,time,random,csv,json,re,traceback
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


fake_ua = UserAgent()
headers = {
    'User-Agent': fake_ua.random,
    'Cookie': 'sim-inst-token="1:3902333280-3902333207-3000202650-3991463349-3000136691-3002642964-3000791242-3000196625:1600362180527:1407c853"; OptanonConsent=isIABGlobal=false&datestamp=Thu+Sep+17+2020+16%3A45%3A11+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=5.6.0&landingPath=https%3A%2F%2Fwww.springer.com%2Fjournal%2F40725'
}




def read_file():
    e_Issn_mode = r'https://.*?/.*?/(\w+)'
    Wiley_url = []
    with open('./wiley_url.csv','r') as fp:
        for line in fp:
            line = line.strip()
            print(line)
            e_Issn = regulize_process(e_Issn_mode,line)
            print(e_Issn)
            url = 'https://onlinelibrary.wiley.com/loi/{}'.format(e_Issn)
            Wiley_url.append(url)
    return Wiley_url


def get_volume_url(url):
    global headers 
    volume_url_list = []
    resp = requests.get(url,headers = headers)
    text = resp.text
    soup = BeautifulSoup(text,'lxml')
    volume_url = ['https://onlinelibrary.wiley.com' + volume_dom.attrs['href'] for volume_dom in soup.find_all('a',class_='visitable')]
    volume_url_list.extend(volume_url)
    return volume_url_list

def get_article_url(volume_url):
    global headers
    resp = requests.get(volume_url,headers = headers,timeout=20)
    text = resp.text
    soup = BeautifulSoup(text,'lxml')
    article_url =  [ 'https://onlinelibrary.wiley.com' + article_dom.attrs['href'] for article_dom in soup.find_all('a',class_="issue-item__title visitable")][1:]
    journal_name = soup.find('img',class_="journal-banner-image").attrs['alt']
    return article_url,journal_name

def article_Process(article_url):
    global headers
    article_info = {

    }
    resp = requests.get(article_url,headers = headers,timeout = 20)
    print('start loading : {}'.format(article_url))
    print('status_code: {}'.format(resp.status_code))
    text = resp.text
    soup = BeautifulSoup(text,'lxml')
    article_title = soup.find('h1',class_="citation__title").string
    author_list = [author_dom.find('span').get_text() for author_dom in soup.find_all('div', class_="accordion-tabbed__tab-mobile")]
    mode = r'https://.*?/.*?/.*?/(.*\.?.*)'
    try:
        article_id = regulize_process(mode,article_url)
    except:
        traceback.print_exc()
    reference_craw(article_id,article_url)
    article_info['title'] = article_title
    article_info['author'] = author_list
    article_info['title_id'] = article_id
    time.sleep(random.randint(3,6))
    print('loading done!')
    print('-'*50)
    return article_info


def regulize_process(mode,article_url):
    pattern = re.compile(mode)
    article_id = pattern.match(article_url).group(1)
    return article_id


def reference_craw(article_id,article_url):
    global headers
    print('laoding reference : {}'.format(article_id))
    resp = requests.get(article_url,headers = headers,timeout = 20)
    text = resp.text
    soup = BeautifulSoup(text,'lxml')
    for dom in soup.find('ul',class_="rlist separator").find_all('li'):
        article_reference = {

        }
        try:
            article_reference['title'] = dom.find('span',class_="articleTitle").get_text()
            article_reference['author'] =  [author.get_text() for author in dom.find_all('span',class_="author")]
        except:
            continue
        with open('./reference/{}.json'.format(article_id),'a') as file:
            json.dump(article_reference,file)


if __name__ == '__main__':
    Wiley_url = read_file()
    for url in Wiley_url:
        volume_url_list = get_volume_url(url)
        for volume_url in volume_url_list:
            print('-'*50)
            article_url,journal_name = get_article_url(volume_url)
            for article_info in article_url:
                try:
                    article_info = article_Process(article_info)
                    with open('./journal/{}.json'.format(journal_name),'a') as fp:
                           json.dump(article_info,fp)
                           fp.close()
                except:
                    continue
            

    