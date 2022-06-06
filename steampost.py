import requests
from bs4 import BeautifulSoup
import time
from lxml import  etree
import threading
class Steam:


    url = 'https://steamcommunity.com/app/730/tradingforum/'
    r = requests.get(url)
    store_post = []
    remove_duplicate = []

    def __init__(self, url, request):
        self.url = url
        self.request = request

    def scrape_data(self):
        soup = BeautifulSoup( Steam.r.text, 'lxml')
        for steam_post in soup.find_all('a',{'class': 'forum_topic_overlay'}):
            Steam.store_post.append(steam_post['href'])


    def checking_post(self):


        for steam_post_validate in Steam.store_post[3:]:
            url = steam_post_validate
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            dom = etree.HTML(str(soup))
            for validate in dom.xpath('//div[@class="popup_block_new forum_author_menu"]//a[2]'):
                if validate.get('href') not in Steam.remove_duplicate:
                    Steam.remove_duplicate.append(validate.get('href'))
        #task check the duplicate next

        time.sleep(5)

    def finalize_data(self):
        for extract in Steam.remove_duplicate:
            r = requests.get(extract)
            soup = BeautifulSoup(r.text, 'lxml')
            count_post = soup.find_all('a', {'class': 'searchresult_forum_link'})
            if len(count_post) <= 4:
                print(extract)
            else:
                print("Nothing found")


if __name__ == '__main__':

    steam = Steam(Steam.url,Steam.r)
    while True:
        t1 = threading.Thread(target=steam.scrape_data(), )
        t2 = threading.Thread(target=steam.checking_post(),)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        steam.finalize_data()

