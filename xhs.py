#!/usr/bin/python3
import csv
import math
import hashlib
import json
import os

from urllib import parse
import requests
from bs4 import BeautifulSoup
from lxml import html
from tqdm import tqdm

import tools.logger as logger
import tools.utils as utils



def get_x_sign(api):
    x_sign = "X"
    m = hashlib.md5()
    m.update((api + "WSUDD").encode())
    x_sign = x_sign + m.hexdigest()
    return x_sign


def spider(keyword, authorization, d_page, sort_by='general'):
    host = 'https://www.xiaohongshu.com'
    url = '/fe_api/burdock/weixin/v2/search/notes?keyword={}&sortBy={}' \
          '&page={}&pageSize=20&prependNoteIds=&needGifCover=true'.format(parse.quote(keyword),
                                                                          sort_by,
                                                                          d_page + 1)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat',
        'Referer': 'https://servicewechat.com',
        'Authorization': authorization,  # 过期时间暂时未知
        'X-Sign': get_x_sign(url)
    }

    resp = requests.get(url=host + url, headers=headers, timeout=5)
    if resp.status_code == 200:
        res = json.loads(resp.text)
        return res['data']['notes'], res['data']['totalCount']
    else:
        logger.error('{}'.format(resp.text))


def getlistByName(keyword, authorization_, pageNum=1, sorted_way="general"):
    notes = []
    with logger.status(f"开始检索关键词【{keyword}】相关内容...") as status:
      for i in range(0, pageNum):
          tmp = spider(keyword, authorization_, d_page=i, sort_by=sorted_way)
          if (len(tmp[0]) <= 0):
              break
          else:
              notes.extend(tmp[0])
    ids = []
    for note in notes:
        ids.append(note['id'])
    logger.success(f"检索关键词【{keyword}】相关内容完毕！共检索到" + len(ids).__str__() + "篇内容")
    return ids

def getInfo(ids,keyword):
    logger.info(f"开始爬取【{keyword}】相关内容")
    infolist = []
    for id in tqdm(ids):
        url = "https://www.xiaohongshu.com/explore/" + id
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Connection": "keep-alive",
            "Host": "www.xiaohongshu.com",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1"
        }
        resp = requests.get(url, headers=headers)
        resp.encoding =  "utf-8"
        html = resp.text

        soup = BeautifulSoup(html, 'lxml')

        json_str = soup.find(attrs={'type': 'application/ld+json'}).text

        json_str = json_str.replace('\n', '').replace('\r\n', '')
        info_dic = json.loads(json_str, strict=False)
        info_dic['link'] = url
        
        if info_dic['name'] != '':
            infolist.append(info_dic)
    logger.success(f"爬取【{keyword}】相关笔记完成 共" + len(infolist).__str__() + "篇")
    return infolist


def saveCsvFile(data, keyName):
    logger.info("开始将数据写入到"+keyName+'.csv文件')
    csv_file = '{}_xhs.csv'.format(keyName)
    if os.path.exists(csv_file):
        os.remove(csv_file)
        logger.warn('文件存在，已删除: {}'.format(csv_file))
    f = open(csv_file, 'w', newline='', encoding="utf-8")
    csv_write = csv.writer(f)
    with logger.status("[bold green]开始将数据写入到本地文件...") as status:
      for i in range(len(data)):
          csv_write.writerow(data[i])
      f.close()
    logger.success("数据已成功写入到本地文件"+keyName+'.csv')


def toCsv(infolist, keyname):
    listlist = [['小红书地址', '标题', '内容', '作者昵称','作者首页地址']]
    for info in infolist:
        name = info['name']
        link = info['link']
        description = info['description']
        author = info['author']['name']
        authorLink=info['author']['url']
        listinfo = [link, name, description,author,authorLink]
        listlist.append(listinfo)
    saveCsvFile(listlist, keyname)


def start(keyName,pageSize):
    logger.start("开始小红书数据爬取任务...")
    authorization = utils.getEnv("XHS_AUTHORIZATION")
    sortedWay = "hot_desc"
    idList = getlistByName(keyName, authorization, math.ceil(int(pageSize)/20),sortedWay)
    toCsv(getInfo(idList,keyName), keyName.replace(" ", "_"))
    logger.success("小红书数据爬取完成")



 
    
