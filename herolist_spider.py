#! /usr/bin/env python
# coding=utf-8
import requests
import sqlite3
import datetime
import re
import json
from bs4 import BeautifulSoup
from DataBase import mongodb_options
from throttle import Throttle


# 保存到数据库
def saveToSqlite(spider_info):
    # 获取spider_info字典中的信息
    hero_id = spider_info["hero_id"]
    hero_name = spider_info["hero_name"]
    # 连接数据库并插入相应数据
    mongodb_conn = mongodb_options.mongodb_init_uestc()
    print "-------------->"
    print id
    mongodb_options.insert_pvp_hero(mongodb_conn,hero_id,hero_name)

# 抓取京东商品主函数
def startGrab():

    # 所有页面的BaseURL
    base_url = "http://pvp.qq.com/web201605/js/herolist.json"
    # 当前页码
    headers = {"Content-type": "application/x-www-form-urlencoded"
                        , "Accept": "text/plain"
                        , "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36"}
    try:
        #throttle = Throttle(delay=1000)
        #throttle.wait(url)
        heroList = requests.get(base_url,headers=headers)
    except:
        print "requests error"
    print "============start=========="
    print heroList.text
    hero_list = json.loads(heroList.text)
    for hero in hero_list:
        hero_id = hero["ename"]
        hero_name = hero["cname"]
        heroInfo = {"hero_id":hero_id,"hero_name":hero_name}
        saveToSqlite(heroInfo)
    #comments_info = json.decode(soup)
    print "============end=========="

if __name__ == '__main__':
    startGrab()



