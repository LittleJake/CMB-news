import datetime
import redis
import requests

REDIS_HOST = "{{REDIS_HOST}}"
REDIS_PORT = "{{REDIS_PORT}}"
REDIS_PASSWORD = "{{REDIS_PASSWORD}}"
SERVERCHAN_TOKEN = "{{SERVERCHAN_TOKEN}}"
WXPUSHER_TOKEN = "{{WXPUSHER_TOKEN}}"

pool = redis.ConnectionPool(host=REDIS_HOST,
                            port=REDIS_PORT,
                            password=REDIS_PASSWORD)


def get_time(origin_date_str):
    local_date = datetime.datetime.strptime(origin_date_str, "%Y-%m-%dT%H:%M:%S.%fZ") \
                 + datetime.timedelta(hours=8)
    return datetime.datetime.strftime(local_date, '%Y-%m-%d %H:%M:%S')


def set_id(id):
    re = redis.StrictRedis(connection_pool=pool,decode_responses=True)
    return re.set('CMB_ID', id)


def get_id():
    re = redis.StrictRedis(connection_pool=pool,decode_responses=True)
    re.setnx('CMB_ID', 0)
    return int(re.get('CMB_ID'))


def set_json(data):
    re = redis.StrictRedis(connection_pool=pool,decode_responses=True)
    return re.set('CMB_JSON', data)



def send_msg_wxpusher(msg):
    if msg == "":
        return

    body = requests.get(url="http://wxpusher.zjiecode.com/api/fun/wxuser"
                            "?appToken="+WXPUSHER_TOKEN+"&page=1&pageSize=50")

    data = {
        "appToken": WXPUSHER_TOKEN,
        "content": msg,
        "contentType": 3,
        "uids": []
    }

    for user in body.json()['data']['records']:
        data["uids"].append(user['uid'])

    body = requests.post(url="http://wxpusher.zjiecode.com/api/send/message",
                         json=data)
    return body.json()


def send_msg_serverchan(title, msg):
    if title == "" or msg == "":
        return
    requests.post(url="https://sc.ftqq.com/"+SERVERCHAN_TOKEN+".send",
                  data={"text": title, "desp": msg})
    return


def fetch():
    headers = {
        'Host': 'cmbgold-api-gateway.paas.cmbchina.com',
        'encryptData': 'a80c35dd80944c723880a6b17178b0cb',
        'User-Agent': 'CMBGold/38 CFNetwork/1125.2 Darwin/19.4.0',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Accept-Language': 'zh-tw',
        'timeStamp': '1583344609',
        'Cache-Control': 'no-cache',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    body = requests.get(url='https://cmbgold-api-gateway.paas.cmbchina.com/api/news/short'
                        , headers=headers)

    return body.json()


json = fetch()
id = get_id()
msg = ""
title = ""

for data in json["data"]:
    if get_id() < int(data['id']):
        set_id(int(data['id']))
        title = "招银汇金推送，id：" + data['id']

    if id < int(data['id']):
        msg += (get_time(data["time"]) + " " + data["content"] + '\n\n')


if WXPUSHER_TOKEN != "":
    send_msg_wxpusher(msg)

if SERVERCHAN_TOKEN != "":
    send_msg_serverchan(title, msg)

set_json(json)