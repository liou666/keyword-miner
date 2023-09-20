import os 
import re 
import math

import pandas as pd
from jsonpath import jsonpath
import requests 
from tqdm import tqdm

import tools.logger as logger
import tools.utils as utils

def jsonModel(jsonData):
        # 微博创建时间
        time_list = jsonpath(jsonData, "$..mblog.created_at")
        time_list = [utils.formet_time(i) for i in time_list]
        # 微博作者
        author_list = jsonpath(jsonData, '$..mblog.user.screen_name')
        # 微博ID
        id_list = jsonpath(jsonData, '$..mblog.id')
        # 微博b_id
        bid_list = jsonpath(jsonData, '$..mblog.bid')
        # 转发数
        reposts_count_list = jsonpath(jsonData, '$..mblog.reposts_count')
        # 评论数
        comment_count_list = jsonpath(jsonData, '$..mblog.comments_count')
        # 点赞数
        attitudes_count_list = jsonpath(jsonData, '$..mblog.attitudes_count')
        # 微博链接
        link_list = list(map(lambda x: "https://m.weibo.cn/detail/"+x, id_list))
        
        return time_list, author_list, id_list, bid_list, reposts_count_list, comment_count_list, attitudes_count_list, link_list

def getInfo(keyword, pageNum, csv_file_name):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.54',
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br",
    }

    for page in range(1, pageNum+1):
        url = 'https://m.weibo.cn/api/container/getIndex'
        detailUrl = 'https://m.weibo.cn/statuses/extend'
        params = {
            "containerid": "100103type=1&q={}".format(keyword),
            "page_type": "searchall",
            "page": page,
        }

        r = requests.get(url, headers=headers, params=params)
        cards = r.json()["data"]["cards"]

        text_list = [] # 微博简介集合
        text_list = jsonpath(cards, '$..mblog.text')
        content_list=[] #微博内容集合

        dr = re.compile(r'<[^>]+>', re.S)
        if not text_list:  continue

        time_list, author_list, id_list, bid_list, reposts_count_list, comment_count_list, attitudes_count_list, link_list = jsonModel(cards)

        for id in tqdm(id_list):
            r1 = requests.get(detailUrl+"?id="+id, headers=headers)
            r2 = r1.json()["data"]["longTextContent"]
            content = dr.sub('', r2) 
            content_list.append(content)

        dataFrame = pd.DataFrame(
            {
                '微博链接': link_list,
                '微博内容': content_list,
                '微博作者': author_list,
                '发布时间': time_list,
                '转发数': reposts_count_list,
                '评论数': comment_count_list,
                '点赞数': attitudes_count_list,
                '微博BID': bid_list
            }
        )

        if os.path.exists(csv_file_name): header = None
        else: header = ['微博链接','微博内容', '微博作者','发布时间','转发数','评论数','点赞数', '微博BID']


        # 保存到csv文件
        dataFrame.to_csv(csv_file_name, mode='a+', index=False, header=header)
        logger.success(f'爬取第{page}页微博数据成功')

def start(keyWord,pageSize):
    logger.start("开始微博数据爬取任务...")
    
    csv_file_name = '{}_wb.csv'.format(keyWord.replace(" ", "_"))

    if os.path.exists(csv_file_name):
        os.remove(csv_file_name)
        logger.warn('文件存在，已删除: {}'.format(csv_file_name))
    getInfo(keyWord, math.ceil(int(pageSize)/12),csv_file_name)
    dataFrame = pd.read_csv(csv_file_name)
    dataFrame.drop_duplicates(subset=['微博BID'], inplace = True, keep = 'first')
    dataFrame.to_csv(csv_file_name, index = False, encoding = 'utf_8_sig')
    logger.success("微博数据爬取完成")


