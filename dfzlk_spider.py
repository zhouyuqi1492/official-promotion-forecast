import requests
from bs4 import BeautifulSoup
from bs4.element import NavigableString
import json
import os
from pypinyin import pinyin, Style,lazy_pinyin
import re


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743/116 Safari/537.36'
}
# 全局计数,后作为文件名
count_people = 0
#为了更方便的访问个人简历
url_for_people = 'http://ldzl.people.com.cn/dfzlk/front/'


def gain_province_url(url):
    # 用于保存省一级资料页面的后缀数组
    array = []
    url_complete = url + '/dfzlk/front/personProvince1.htm'
    html = requests.get(url = url_complete, headers = headers)
    html_bytes = html.content
    html_strings = html_bytes.decode('gbk')
    #print(html_strings)
    soup = BeautifulSoup(html_strings, 'lxml')
    sidebar = soup.find(class_ = 'p4_con').find(class_ = 'fl').find('ul')
    tr = sidebar.children
    for i, child in enumerate(tr):
        if isinstance(child,NavigableString):
            continue
        province_name = child.find('a').get_text()
        province_code = child.find('a').get('href')
        array.append((province_name, province_code))
    # 去除港澳台
    array.pop()
    array.pop()
    array.pop()
    #print('省份领导班子网页:', array)
    #print('数组长度', len(array))
    
    return array



# 从各省主页爬到个人的主页面
def spider_province(url, province):
    print(province,'官员的简历爬取')
    filename = lazy_pinyin(province, style = Style.NORMAL)[0] + lazy_pinyin(province, style = Style.NORMAL)[1]
    # 创建保存文件的文件夹
    if os.path.exists('data/' + filename):
        pass
    else:
        os.mkdir('data/' + filename)
    
    html = requests.get(url = url, headers = headers)
    html_bytes = html.content
    html_strings = html_bytes.decode('gbk')
    soup = BeautifulSoup(html_strings, 'lxml')

    # 为避免重复任职的官员多次存储
    people = []

    # 党委班子信息
    dwbz = soup.find_all( class_ = 'box02')[0]
    pattern = "<a href=\"(.*)?\">(.*)?<\/a>"    # 正则表达式对<class 'bs4.element.Tag'>中的文本信息进行配对
    dwbz_str = str(dwbz)
    res = re.findall(pattern, dwbz_str)
    for (url_path, name) in res:
        if name not in people:
            people.append((name, url_path))
        else:
            pass

    # 政府副职信息
    zffz = soup.find_all( class_ = 'box02')[1]
    pattern = "<a href=\"(.*)?\">(.*)?<\/a>"    # 正则表达式对<class 'bs4.element.Tag'>中的文本信息进行配对
    zffz_str = str(zffz)
    res = re.findall(pattern, zffz_str)
    for (url_path, name) in res:
        if name not in people:
            people.append((name, url_path))
        else:
            pass

    # 市区县政领导
    sqxz = soup.find(class_ = 'p1_l_b_right')
    sqxz_str = str(sqxz)
    pattern = "<a href=\"(.*)?\">(.*)?<\/a>" 
    res = re.findall(pattern, sqxz_str)
    for (url_path, name) in res:
        if name == '空缺':
            continue
        if name not in people:
            people.append((name, url_path))
        else:
            pass

    # 对people数组中的所有官员进行个人简历的获取
    for item in people:
        spider_person_and_save(item[1], item[0], filename)
    


def spider_person_and_save(url_path, name, province):
    url = url_for_people + url_path
    #print(url)
    html = requests.get(url=url, headers= headers)
    html_bytes = html.content
    html_strings = html_bytes.decode('gbk')
    soup = BeautifulSoup(html_strings, 'lxml')
    infoBlock = soup.find(class_ = 'box01')
    infoBlock_str =  infoBlock.get_text()

    # 处理字符串空白部分
    infoStr_clear = infoBlock_str.replace('\t', '')
    infoStr_clear = infoStr_clear.replace('\r', '')
    infoStr_clear = infoStr_clear.replace('\u3000', '')
    #infoStr_clear = infoStr_clear.replace('\n', ' ')
    infoStr_clear = infoStr_clear.strip()
    # print(infoStr_clear.split('。', 1))
    #print(infoStr_clear)
    
    # 用户
    info = {}
    for i in range(len(infoStr_clear)):
        if infoStr_clear[i] == '。':
            mark = i 
            break
    info['introduction'] = infoStr_clear[:i+1]
    temp = infoStr_clear[i+1:].replace('\n', ' ')
    regex = re.compile('  ')
    info['experience'] = regex.split(temp)

    for i in range(len(info['experience'])):
        if '人民网' in info['experience'][i] :
            info['experience'].pop()
            break
    for i in range(len(info['experience']))[::-1]:
        if info['experience'][i] == '' or info['experience'][i] == ' ':
            info['experience'].remove(info['experience'][i])

    print(info)
    global count_people
    count_people += 1

    # 写入文件
    filename = ('data/%s/%05d_%s.txt')%(province, count_people, name)
    if os.path.exists(filename):
        print('已经写入')
        pass 
    else:
        with open(filename,'w') as f:
            json.dump(info,f, indent=2, ensure_ascii = False)
        print('写入成功')


def main():
    url = 'http://ldzl.people.com.cn'
    province_array = gain_province_url(url)
    for province, pronvince_url in province_array:
        spider_province(url + pronvince_url, province)



if __name__ == '__main__':
    main()