# -*- coding: utf8 -*-
import urllib
import requests
import re
import json
from DataBase import mongodb_options
import HTMLParser
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

globalSet = set()

class QQPVP(object):
    summaryHeaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Accept-Encoding": "text",
        'Accept-Language':u'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        "Host":"apps.game.qq.com",
    }
    summaryReferer = u'http://pvp.qq.com/web201605/searchResult.shtml?G_biz=18&sKeyword={keyword}'

    articleHeaders = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36",
        "Accept-Encoding": "text",
        'Accept-Language':u'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
        "Host":"apps.game.qq.com",
    }
    articleReferer = u'http://pvp.qq.com/web201605/newsDetail.shtml?G_Biz=18&tid={index}'



    def __init__(self,name):
        self.summarySession = requests.Session()
        self.summarySession.headers = QQPVP.summaryHeaders
        ##Request URL:http://apps.game.qq.com/wmp/v3.1/?p0=18&p1=searchIso&p2=%B0%D7%C6%F0&p3=NEWS&page=3&pagesize=15&order=sIdxTime&r1=searchObj&openId=&agent=&channel=&area=&&_=1504767130553
        #url = u'http://pvp.qq.com/web201605/searchResult.shtml?G_biz=18&sKeyword=%25E7%2599%25BD%25E8%25B5%25B7'
        self.articleSession = requests.Session()
        self.articleSession.headers = QQPVP.articleHeaders
        self.name = name
        self.page = 0
        self.number = 0
        self.articleList = []
        self.heroArticleList = []

    # 保存到数据库
    def saveToSqlite(self,spider_info):
      
        mongodb_conn = mongodb_options.mongodb_init_uestc()
        mongodb_options.insert_pvp_heroart(mongodb_conn,spider_info)

    def startDownload(self):
        self.downloadSummary()
        self.downloadArticle()

    def downloadSummary(self):
        url = u'http://apps.game.qq.com/wmp/v3.1/?p0=18&p1=searchIso&p2={word}&p3=NEWS&page={page}&pagesize=15&order=sIdxTime&r1=searchObj&openId=&agent=&channel=&area=&&_=1504773915672'
        for page in range(1000):
            self.summarySession.headers['Referer'] = QQPVP.summaryReferer.format(keyword=urllib.quote(urllib.quote(self.name)))
            try:
                html = self.summarySession.get(url.format(word=urllib.quote(self.name.decode('utf-8').encode(encoding='gb2312',errors='ignore')),page=page), timeout=15)
                re_status = re.compile(r'"status":"(.*?)"') 
                response_code = re_status.findall(html.content.decode())[0]
                if response_code == '-1' :
                    self.page = page-1
                    break
                re_content = re.compile(r'"sTitle":"(.*?)".*?"sAuthor":"(.*?)".*?"iNewsId":"(.*?)"')
                datas = re_content.findall(html.content.decode('unicode_escape'))
                for data in datas:
                    self.articleList.append({"art_id":data[2],"title":data[0],"author":data[1],"heroName":self.name})
                    self.number += 1
            except Exception as e:
                print("Error with %s ,page = %d , error = %s" % (self.name,self.page,str(e)))

        return;

    def downloadArticle(self):

        url = u'http://apps.game.qq.com/wmp/v3.1/public/searchNews.php?source=web_news_go&p0=18&id={index}&openId=&&agent=&&channel=&&area=&'
        for globa in self.articleList:
            print "=========================article_"+globa['art_id']+"============================="
            if globa['art_id'] in globalSet:
                print("index = %s has writed" % (globa['art_id']))
                continue
            self.articleSession.headers['Referer'] = QQPVP.articleReferer.format(index=globa['art_id'])
            try:
                html = self.articleSession.get(url.format(index=globa['art_id']),timeout=15)
                re_content = re.compile(r'"sContent":"(.+?)",')
                datas_content = re_content.findall(html.content.decode('utf-8'))
                html_parser = HTMLParser.HTMLParser()
                unescaped = html_parser.unescape(datas_content[0].decode('unicode_escape')).replace("\\/","/")
                if len(datas_content)>0:
                    data_content = datas_content[0]
                else:
                    data_content = ''
                re_time = re.compile(r'"sIdxTime":"(.+?)",')
                datas_time = re_time.findall(html.content.decode('utf-8'))
                if len(datas_time)>0:
                    data_time = datas_time[0]
                else:
                    data_time = ''
                globalSet.add(globa['art_id'])
                self.heroArticleList.append({"title":globa['title'],"author":globa['author'],"createtime": data_time,"content":unescaped})
            except Exception as e:
                print("article Error with %s ,error = %s" % (self.name,str(e)))
        heroArticleInfo = {"heroName":globa['heroName'],"article":self.heroArticleList}
        print "======================================save MonogoDB========================"
        self.saveToSqlite(heroArticleInfo)
        return

    def filter_tags(self,htmlstr):
        # 先过滤CDATA
        re_backslash=re.compile(r'\\')
        re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
        re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
        re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
        re_br = re.compile('<br\s*?/?>')  # 处理换行
        re_h = re.compile('</?\w+[^>]*>')  # HTML标签
        re_comment = re.compile('<!--[^>]*-->')  # HTML注释
        s = re_backslash.sub('',htmlstr);
        s = re_cdata.sub('', s)  # 去掉CDATA
        s = re_script.sub('', s)  # 去掉SCRIPT
        s = re_style.sub('', s)  # 去掉style
        s = re_br.sub('\n', s)  # 将br转换为换行
        s = re_h.sub('', s)  # 去掉HTML 标签
        s = re_comment.sub('', s)  # 去掉HTML注释
        # 去掉多余的空行
        blank_line = re.compile('[ \n\t\f\v]+')
        s = blank_line.sub('\n', s)
        s = blank_line.sub('\n', s)
        s = self.replaceCharEntity(s)  # 替换实体
        return s

    def replaceCharEntity(self,htmlstr):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }

        re_charEntity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_charEntity.search(htmlstr)
        while sz:
            entity = sz.group()  # entity全称，如&gt;
            key = sz.group('name')  # 去除&;后entity,如&gt;为gt
            try:
                htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
            except KeyError:
                # 以空串代替
                htmlstr = re_charEntity.sub('', htmlstr, 1)
                sz = re_charEntity.search(htmlstr)
        return htmlstr

def get_hero_name_list():
        mongodb_conn = mongodb_options.mongodb_init_uestc()
        heroList = mongodb_options.get_hero_list(mongodb_conn)
        return heroList

if __name__ == '__main__':
    heroList = []
    heros = get_hero_name_list()
    for hero in heros:
        heroList.append(hero["hero_name"])
    print "=========================Start Spider==========================="
    for hero in heroList:
        print "=================Start "+hero+"=================="
        pvp = QQPVP(hero.encode())
        pvp.startDownload()
        print("name = %s , page = %d , number = %d" % (hero,pvp.page,pvp.number))
        print "=================End "+hero+"=================="
    print "==========================End Spider============================="


