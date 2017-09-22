#! /usr/bin/env python
# coding=utf-8
import baidutieba_spider
import jingdonggoods_spider
import jingdongcomments_spider
from BigSpider_app.DataBase import mysql_options,mongodb_options

# id:站点id
def spider_server(site_data,id):
    if site_data[3] =='baidutieba':#爬取百度贴吧
        baidutieba_spider.startGrab(site_data[1],id)
    elif site_data[3] =='jingdongpinglun':#爬取京东商品评论
        print "jingdonggoods_spider"
        #1、爬取商品列表
        jingdonggoods_spider.startGrab(site_data[2],id)
        #2、根据商品列表爬取商品的评论
        #2.1、获取商品id
        mongodb_conn = mongodb_options.mongodb_init_uestc()
        print "biubiu"
        jingdong_goods_id_list = mongodb_options.jingdonggoods_find_all(mongodb_conn,id)
        print "00000000000000000000000000000000"
        print len(jingdong_goods_id_list)
        for jingdong_goods_iid in jingdong_goods_id_list:
            goods_iid = jingdong_goods_iid['goods_id']
            print goods_iid
        print "1111111111111111111111111111111"
        for jingdong_goods_id in jingdong_goods_id_list:
            goods_id = jingdong_goods_id['goods_id']
            jingdongcomments_spider.startGrab(goods_id,id)

    return;




