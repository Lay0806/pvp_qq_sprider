import redis


def redis_init():
    db = redis.Redis(host='localhost', port=6379, db=0)
    return db


def crawling_queue(db):
    crawling_queue = db.zcard('uestc:request')
    return crawling_queue
