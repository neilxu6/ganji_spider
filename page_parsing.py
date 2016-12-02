from bs4 import BeautifulSoup
import requests
import pymongo
import random


client = pymongo.MongoClient('localhost', 27017)
ganji = client['ganji']
url_list = ganji['url_list']
item_info = ganji['item_info']

headers  = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
    'Connection':'keep-alive'
}

# http://cn-proxy.com/
proxy_list = [
    'http://61.132.241.109:808',
    'http://111.23.4.155:8080',
    'http://120.92.3.165:80',
    ]
proxy_ip = random.choice(proxy_list) # 随机获取代理ip
proxies = {'http': proxy_ip}



# spider 1
def get_links_from(channel, pages, who_sells='o'):
    # http://bj.ganji.com/ershoubijibendiannao/o3/
    # o for personal a for merchant
    list_view = '{}{}{}/'.format(channel, str(who_sells), str(pages))
    wb_data = requests.get(list_view,headers=headers,proxies=proxies)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find('ul', 'pageLink'):
        for link in soup.select('.fenlei dt a'):
            item_link = link.get('href')
            url_list.insert_one({'url': item_link})
            print(item_link)
    else:
        # It's the last page !
        pass

# spider 2
def get_item_info_from(url,data=None):
    wb_data = requests.get(url,headers=headers)
    if wb_data.status_code == 404:
        pass
    else:
        soup = BeautifulSoup(wb_data.text, 'lxml')
        data = {
            'title':soup.title.text.strip(),
            'price':soup.select('.f22.fc-orange.f-type')[0].text.strip(),
            'pub_date':soup.select('.pr-5')[0].text.strip().split(' ')[0],
            'area':list(map(lambda x:x.text,soup.select('ul.det-infor > li:nth-of-type(3) > a'))),
            'cates':list(soup.select('ul.det-infor > li:nth-of-type(1) > span')[0].stripped_strings),
            'url':url
        }
        print(data)
        item_info.insert_one(data)

get_item_info_from('http://bj.ganji.com/ershoubijibendiannao/27447965338166x.htm')
