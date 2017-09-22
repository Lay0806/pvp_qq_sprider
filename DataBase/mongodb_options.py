#! /usr/bin/env python
# coding=utf-8

from pymongo import *
import bson
import uuid

client = MongoClient('10.0.12.233', 27020)


# 连接网页系统数据库
def mongodb_init_spider_ms():

    db = client.spider_ms

    if not client:
        print '[INFO]: MongoDB can not be connected, please check !'
    else:
        print '[INFO]: MongoDB is connected !'
    return db


# 连接爬虫系统数据库
def mongodb_init_uestc():

    client=MongoClient('10.0.12.233', 27020)
    uestc = client.pvp_qq

    if not client:
        print '[INFO]: MongoDB can not be connected, please check !'
    else:
        print '[INFO]: MongoDB is connected !'
    return uestc

# 系统运行数据
def insert_user(db, userid, username, password, email, phone_num):
    db.users.insert({'userid': userid, 'username': username, 'password': password, 'email': email, 'phone_num': phone_num, 'remark':''})


def find_user_by_username(db, username):
    user = db.users.find_one({'username': username})    
    return user


def find_user_by_username_password(db, username, password):
    user = db.users.find_one({'username': username, 'password': password})   
    return user


# 管理员账户在mongodb中手动添加find_admin_by_name_psd
def find_admin_by_name_psd(db, admin_name, admin_psd):
    admin = db.admin.find_one({'admin_name': admin_name, 'admin_psd': admin_psd})
    return admin


def admin_find_all_users(db):
    users = db.users.find()
    return users


def admin_delete_user(db, userid):
    db.users.remove({'userid': userid})


def admin_update_user(db, userid, username, email, phone_num, remark):
    db.users.update({'userid': userid},{
        '$set':{'username': username,'email': email,'phone_num': phone_num,'remark':  remark}})


# db.commoditys.update({'c_id': uid}, {
#     '$set': {'c_name': c_name, 'c_price': c_price, 'c_description': c_description, 'c_postage': c_postage,
#              'c_num': c_num, 'class_name': class_name, 'c_brand': c_brand, 'class_style': class_style,
#              'hotpoint': hotpoint, 'albums': albums, 'specs': specs}})


def admin_find_one_user_byuserid(db, userid):
    user = db.users.find_one({'userid': userid})
    return user


def admin_find_all(db):
    admin_list = db.admin.find()
    return admin_list


# 爬虫数据
# 通过id获得成功抓取数
def crawling_succeed_num_by_id(uestc,id):
    crawling_succeed_num = uestc.crawlinginfo.find({'site_id':id}).count()
    return crawling_succeed_num

# 通过id获得成功京东抓取数
def crawling_jingdong_comments_succeed_num_by_id(uestc,id):
    crawling_succeed_num = uestc.jingdong_comments.find({'site_id':id}).count()
    return crawling_succeed_num

# 获得成功抓取数
def crawling_succeed_num(uestc):
    crawling_succeed_num = uestc.crawlinginfo.find().count()
    return crawling_succeed_num

# 通过id获得爬取的网页信息
def crawling_web_info_by_id(uestc,id):
    crawling_web_info = uestc.crawlinginfo.find({'site_id':id})
    return crawling_web_info

# 通过id获得爬取的京东页面信息
def crawling_jingdong_comments_web_info_by_id(uestc,id):
    crawling_web_info = uestc.jingdong_comments.find({'site_id':id})
    return crawling_web_info

crawling_jingdong_comments_web_info_by_id

# 爬取的网页信息
def crawling_web_info(uestc):
    crawling_web_info = uestc.crawlinginfo.find()
    return crawling_web_info

# 爬取的网页信息
def insert_crawlinginfo(db, title,context,url,auther,create_time,site_id):
    db.crawlinginfo.insert({'title': title, 'context': context, 'url': url, 'auther': auther, 'create_time': create_time, 'site_id':site_id})


#爬取京东商品
def insert_goods_id(db, goods_id,site_id):
    db.jingdong_goods.insert({'goods_id': goods_id,'site_id':site_id})

#获取商品ID
def jingdonggoods_find_all(db,id):
    jingdong_goods_id_list = db.jingdong_goods.find({'site_id':id})
    return jingdong_goods_id_list

#爬取pvp官网英雄
def insert_pvp_hero(db,hero_id,hero_name):
    db.herolist.insert({'hero_id': hero_id,'hero_name':hero_name})

def insert_pvp_heroart(db,insertdata):
    db.hero_article_list.insert(insertdata)

def get_hero_list(db):
    hero_list = db.herolist.find()
    return hero_list