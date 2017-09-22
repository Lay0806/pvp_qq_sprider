# -*- coding:utf-8 -*-
import MySQLdb


def mysql_init():
    conn = MySQLdb.connect(host='127.0.0.1', user='root', passwd='wang19910806', db='spider', charset='utf8')
    if conn:
        return conn
        print '[INFO] mysql is connected !!'
    else:
        print '[INFO] mysql failed to be connected !!!'


# 获取已添加站点信息
def get_site_info(conn):
    cur = conn.cursor()
    sql = 'select * from rules'
    result = cur.execute(sql)
    data = cur.fetchmany(result)
    return data


# 通过ID删除站点
def delete_site_by_id(conn, ids):
    cur = conn.cursor()
    for id0 in ids:
        id0 = int(id0)
        sql = "delete from rules where id=%s"
        result = cur.execute(sql, id0)
    conn.commit()
    return result


# 通过ID修改站点信息
def update_site_info(conn,id,name,url,rule):
    cur = conn.cursor()
    id0 = int(id)
    sql = "update rules set name='%s', start_urls='%s',extract_from='%s' where id=%d" % (name, url, rule, id0)
    result = cur.execute(sql)
    conn.commit()
    return result


# 添加站点
def add_site(conn,name,url,rule,firstsit):
    cur = conn.cursor()
    sql = "insert into rules (name,start_urls,extract_from,firstsit) values('%s','%s','%s','%s')" % (name,url,rule,firstsit)
    result = cur.execute(sql)
    conn.commit()
    return result

#根据id查询一个站点
def get_site_info_by_id(conn,id):
    cur = conn.cursor()
    id = int(id)
    sql = "select name,start_urls,extract_from,firstsit from rules where id=%s"
    result = cur.execute(sql, id)
    data = cur.fetchmany(result)
    print "3############"
    print data[0]
    return data[0]





# 添加爬取结果
def add_spiderinfo(conn,name,keyword,time,crawling_num,site_id):
    cur = conn.cursor()
    sql = "insert into spiderinfo (name,keyword,time,crawling_num,site_id) values('%s','%s','%s','%s','%s')" % (name,keyword,time,crawling_num,site_id)
    result = cur.execute(sql)
    conn.commit()
    return result

# 获取爬取结果
def get_spiderinfo_info(conn):
    cur = conn.cursor()
    sql = 'select * from spiderinfo'
    result = cur.execute(sql)
    data = cur.fetchmany(result)
    return data
