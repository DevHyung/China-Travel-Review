import requests
from bs4 import BeautifulSoup
import json
import time
def GetUrl():
    f = open('mafengwo_New_List.txt', 'w')
    idx = 1
    for pageIdx in range(1, 706):
        datas = {
            'mddid': 10184,
            'pageid': 'mdd_index',
            'sort': 2,
            'cost': 0,
            'days': 0,
            'month': 0,
            'tagid': 0,
            'page': pageIdx
        }
        basicUrl = 'http://www.mafengwo.cn'
        url = 'http://www.mafengwo.cn/gonglve/ajax.php?act=get_travellist'
        html = requests.post(url, data=datas)
        jsonStr = json.loads(html.text)
        bs4 = BeautifulSoup(jsonStr['list'], 'lxml')
        divs = bs4.find_all('div', class_='tn-image')
        print(pageIdx, ' 페이지 ', len(divs), '개 수집중')
        for div in divs:
            href = div.find('a')['href']

            idx += 1
            f.write(basicUrl + href + '\n')

    f.close()
if __name__ =="__main__":
