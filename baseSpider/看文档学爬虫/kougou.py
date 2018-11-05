import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client=MongoClient()
songs=client.kugon_db.songs

headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3964.2 Safari/537.36"
}

def get_info(url):
    wb_data=requests.get(url,headers=headers)
    soup=BeautifulSoup(wb_data.text,"lxml")
    ranks=soup.select(".pc_temp_num")
    print(ranks)
    titles=soup.select(".pc_temp_songlist > ul > li > a")
    songs_times=soup.select(".pc_temp_time")
    for rank,title,song_time in zip(ranks,titles,songs_times):
        data={
            'rank':rank.get_text().strip(),
            'singer':title.get_text().split('-')[0].strip(),
            'song':title.get_text().split('-')[1].strip(),
            'time':song_time.get_text().strip()
        }
        print(data)
        song_id=songs.insert(data)
        print(song_id)
        print('-------------------------------------------------------')

if __name__ == "__main__":
    urls =['http://www.kugou.com/yy/rank/home/{}-8888.html?from=rank'.format(str(i)) for i in range(1,2)]
    for url in urls:
        get_info(url)
        time.sleep(2)