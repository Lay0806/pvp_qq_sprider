# pvp_qq_sprider
爬取王者荣耀官网英雄攻略
## 01 需求

本次爬虫主要是爬取王者荣耀官网中所有英雄的英雄攻略。并将数据存入到mongoDB数据库中。

#### 使用的技术

* Python2中的urllib模块、request模块
* 正则表达式
* Mongo数据库

#### 遇到的问题

* Python2中的转码问题
* 正则表达式的匹配
* html语言转码
* 爬取页面的url

## 02 过程
#### 获取hero列表
由于官网上的hero数据是通过动态加载的，返回的事json文件，所以我们只需要获取到json文件，读取出来就可以了。
* 获取json文件
```Python
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
    ...

```
*获取每个hero对象
```Python
hero_list = json.loads(heroList.text)
    for hero in hero_list:
        hero_id = hero["ename"]
        hero_name = hero["cname"]
        heroInfo = {"hero_id":hero_id,"hero_name":hero_name}
```
*将数据保存到Mongo数据库中
```Python
# 获取spider_info字典中的信息
    hero_id = spider_info["hero_id"]
    hero_name = spider_info["hero_name"]
    # 连接数据库并插入相应数据
    mongodb_conn = mongodb_options.mongodb_init_uestc()
    print "-------------->"
    print id
    mongodb_options.insert_pvp_hero(mongodb_conn,hero_id,hero_name)
```
#### 获取英雄攻略
* 首先，我们需要遍历每一个hero，获取每一个英雄的攻略
```Python
heroList = []
    heros = get_hero_name_list()
    for hero in heros:
        heroList.append(hero["hero_name"])
    print "=========================Start Spider==========================="
    for hero in heroList:
        print "=================Start "+hero+"=================="
        pvp = QQPVP(hero.encode())
        pvp.startDownload()
```
* 由于获取英雄攻略时的request存在有一个依赖关系，所以我们先找出其以来的url，找到每一个hero的攻略列表
```Python
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
```
* 最后，遍历每一个英雄的攻略列表，爬取每一篇对应的内容
```Python
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
```




## 03 总结
本项目实现了爬取王者荣耀英雄攻略的功能，并且具有可用性、可靠性的保证。但是还是有以下的不足：
* 应该使用分布式爬虫技术，增加爬取效率
* 应该加入Rides缓存机制，防止进程阻塞
* 应该加入反爬虫技术（虽然爬取的目标站点没有反爬技术）

