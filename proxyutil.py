#!/usr/bin/env python
# coding:utf-8
import requests
import json
from ProxyPool.config import API_CONFIG

def getProxy():
    port = API_CONFIG['PORT']
    r = requests.get('http://localhost:%s/' % port)
    proxy = json.loads(r.content)
    if proxy:
        proxy = proxy[0]
    return proxy 