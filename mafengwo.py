import requests
from bs4 import BeautifulSoup
import json
import xlsxwriter
# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook('TEST.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write_row(0,0,['URL','제목','공유날짜','정보','내용'])
row = 1
col = 0
f = open('test.txt','w')
def GetUrl():
    f = open('mafengwoList.txt', 'w')
    idx = 1
    for pageIdx in range(1, 301):
        datas = {
            'mddid': 10184,
            'pageid': 'mdd_index',
            'sort': 1,
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
        for div in divs:
            href = div.find('a')['href']
            print(idx, " : ", basicUrl + href)
            idx += 1
            f.write(basicUrl + href + '\n')

    f.close()
if __name__ =="__main__":
    url = 'http://www.mafengwo.cn/i/9412201.html'
    html = requests.get(url)
    bs4 = BeautifulSoup(html.text,'lxml')
    title = bs4.find('h1',class_='headtext lh80').get_text().strip()

    #___시간부분
    iid =  bs4.find('div',class_='view_title clearfix').find('div')['data-params'].split(':')[1][1:-2]
    # print(timeHtml.text.split('(',maxsplit=1)[1][:-2])
    timeApiUrl = 'http://pagelet.mafengwo.cn/note/pagelet/headOperateApi?callback=jQuery1810058602936847424125_1531032027345&params=%7B%22iid%22%3A%22{}%22%7D&_=1531032027452'.format(iid)
    timeHtml = requests.get(timeApiUrl)
    jsonStr = json.loads(timeHtml.text.split('(',maxsplit=1)[1][:-2])
    timeBs4 = BeautifulSoup(jsonStr['data']['html'], 'lxml')
    datetime = timeBs4.find('span',class_='time').get_text().strip()
    #___시간부분 끝
    #___옵션부분
    optionLis = bs4.find('div',class_='tarvel_dir_list clearfix').find_all('li')
    optionStr =""
    for li in optionLis:
        optionStr += li.get_text().strip()+'\n'
    #___옵션부분 끝
    #___내용부분
    div = bs4.find('div',class_='_j_content_box')
    textJson = json.loads(bs4.find('script').get_text().split(' = ')[1][:-2])
    new_iid = textJson['new_iid']  ##끝

    text = " ".join(div.get_text().split()) + '\n'
    lastDiv = div.find_all('div')[-1]
    laseSeq = lastDiv['data-seq'] ##마지막
    print(laseSeq)
    while True:
        ajaxUrl = 'http://www.mafengwo.cn/note/ajax.php?act=getNoteDetailContentChunk&id={}&iid={}&seq={}&back=0'.format(iid,new_iid,laseSeq)
        html = requests.get(ajaxUrl)
        jsonStr = json.loads((html.text))
        has_more = jsonStr['data']['has_more']
        bs4 = BeautifulSoup(jsonStr['data']['html'], 'lxml')
        text += " ".join(bs4.get_text().split()) + '\n'
        print(" ".join(bs4.get_text().split()))
        print("___"*10)
        lastDiv = bs4.find_all('div')[-1]
        laseSeq = lastDiv['data-seq']  ##마지막
        #print(laseSeq)
        #print(has_more)
        if has_more:
            pass
        else:
            break
    #___내용부분 끝
    #___출력
    print(iid,title,datetime)
    print(optionStr)
    print(text)
    worksheet.write_row(row, col, [url,title, datetime,optionStr])
    worksheet.write_string(row, 5, text)
    f.write(text)
    row += 1
workbook.close()

