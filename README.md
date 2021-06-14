# CMB-news
![Crond job for Redis CMB](https://github.com/LittleJake/CMB-news/workflows/Crond%20job%20for%20Redis%20CMB/badge.svg)
![Crond job for non redis CMB](https://github.com/LittleJake/CMB-news/workflows/Crond%20job%20for%20non%20redis%20CMB/badge.svg)

爬取招商银行-招银汇金财经新闻，调用github workflow定时抓取

## 介绍
爬取思路：URL重放，服务器不校验时间戳，导致相同时间校验头可无限重放获取最新数据。

## 说明
### Redis版
通过redis保存已推送过的id来节省流量，并且保存Json至Redis内供外部调用。


| 键      | 说明              |
| ------- | ---------------- |
| CMB_ID  | 推送过的最新消息ID  |
| CMB_JSON| 获取的消息Json字符串|


### 非Redis版
自动调用Server酱或Wxpusher的API推送至微信。


### 其他
脚本自动运行为5分钟一次，可修改workflow文件达到自己想要的效果。


## 使用方法
1. fork本项目
2. 申请server酱token，[Server酱官网](http://sc.ftqq.com/)
3. 申请Wxpusher的appToken，[wxpusher官网](https://wxpusher.zjiecode.com/docs/#/)
4. 打开项目`Settings`→`Secrets`页面，添加如下
    
    |  名称              | 说明               | 值实例      |
    |  ---------------  | ----------------  | ---------- |
    | REDIS_HOST        | Redis主机/IP       | 127.0.0.1 |
    | REDIS_PORT        | Redis端口          | 6379      |
    | REDIS_PASSWORD    | Redis密码          | 123456    |
    | SERVERCHAN_TOKEN  | Server酱token     | -         |
    | WXPUSHER_TOKEN    | Wxpusher appToken | -         |
    
5. 打开`Action`页面，激活workflow，点击`Enable`
6. 在自己的项目点个Star即可运行Workflow

## 运行截图

![1](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210614143821.jpg)

![2](https://cdn.jsdelivr.net/gh/LittleJake/blog-static-files@imgs/imgs/20210614143822.jpg)

## 鸣谢
[Server酱](http://sc.ftqq.com/)

[wxpusher](https://wxpusher.zjiecode.com/docs/#/)

## 开源许可证
Apache 2.0
