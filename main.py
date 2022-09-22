import datetime as dt
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
from zhdate import ZhDate
import requests
import os
import random

start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]

def get_token():
  url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid="+ app_id +"&secret=" + app_secret
  res = requests.get(url).json()
  access_token = res['access_token']
  return access_token

def get_userId():
  token = get_token()
  url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token="+ token +"&next_openid="
  res = requests.get(url).json()
  openidArr = res['data']['openid']
  return openidArr

def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_count():
#   delta = today - datetime(start_date, "%Y-%m-%d")
#   return delta.days
    return 11

def get_birthday():
    return 123
#   next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
#   if next < datetime.now():
#     next = next.replace(year=next.year + 1)
#   return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  return words.json()['data']['text']

def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]

def time_parse(today):
   distance_year = (dt.datetime.strptime(str(today.year) + "-01-01", "%Y-%m-%d") - today).days
   if distance_year < 0 :
   		distance_year = (dt.datetime.strptime(str(today.year + 1) + "-01-01", "%Y-%m-%d") - today).days

   distance_big_year = (ZhDate(today.year, 1, 1).to_datetime() - today).days
   if distance_big_year < 0 :
        (ZhDate((today.year + 1), 1, 1).to_datetime() - today).days

   distance_4_5 = (dt.datetime.strptime(str(today.year) + "-04-05", "%Y-%m-%d") - today).days
   if distance_4_5 < 0 :
        (dt.datetime.strptime(str(today.year + 1) + "-04-05", "%Y-%m-%d") - today).days

   distance_5_1 = (dt.datetime.strptime(str(today.year) + "-05-01", "%Y-%m-%d") - today).days
   if distance_5_1 < 0 :
        (dt.datetime.strptime(str(today.year + 1) + "-05-01", "%Y-%m-%d") - today).days

   distance_5_5 = (ZhDate(today.year, 5, 5).to_datetime() - today).days
   if distance_5_5 < 0 :
        (ZhDate(today.year + 1, 5, 5).to_datetime() - today).days

   distance_8_15 = (ZhDate(today.year, 8, 15).to_datetime() - today).days
   if distance_8_15 < 0 :
        (ZhDate(today.year + 1, 8, 15).to_datetime() - today).days

   distance_10_1 = (dt.datetime.strptime(str(today.year) + "-10-01", "%Y-%m-%d") - today).days
   if distance_10_1 < 0 :
        (dt.datetime.strptime(str(today.year + 1) + "-10-01", "%Y-%m-%d") - today).days

    # print("距离周末: ", 5 - today.weekday())
    # print("距离元旦: ", distance_year)
    # print("距离大年: ", distance_big_year)
    # print("距离清明: ", distance_4_5)
    # print("距离劳动: ", distance_5_1)
    # print("距离端午: ", distance_5_5)
    # print("距离中秋: ", distance_8_15)
    # print("距离国庆: ", distance_10_1)

   time_ = [
	{"v_": 5 - 1 - today.weekday(), "title": "周末"}, # 距离周末
        {"v_": distance_year, "title": "元旦"}, # 距离元旦
        {"v_": distance_big_year, "title": "过年"}, # 距离过年
        {"v_": distance_4_5, "title": "清明节"}, # 距离清明
        {"v_": distance_5_1, "title": "劳动节"}, # 距离劳动
        {"v_": distance_5_5, "title": "端午节"}, # 距离端午
        {"v_": distance_8_15, "title": "中秋节"}, # 距离中秋
        {"v_": distance_10_1, "title": "国庆节"}, # 距离国庆
   ]


   time_ = sorted(time_, key = lambda x: x['v_'], reverse = False)

   return time_

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

def get_du():
  du = requests.get("https://api.shadiao.pro/du")
  if du.status_code != 200:
    return get_du()
  return du.json()['data']['text']

def get_pyq():
  pyq = requests.get("https://api.shadiao.pro/pyq")
  if pyq.status_code != 200:
    return get_pyq()
  return pyq.json()['data']['text']

holiday = ''
today = dt.datetime.today()
time_ = time_parse(today)
for t_ in time_:
   if t_.get("v_") >= 0:
      holiday += '\n 距离{}还有:{}天'.format(t_.get("title"), t_.get("v_"))


date_new = '{}年{}月{}日 {}'.format(today.year, today.month, today.day, get_week_day(today))


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {
	"weather":{"value":wea},"temperature":{"value":temperature},
	"love_days":{"value":get_count()}, "color":{get_random_color()},
	"date_new":{"value":date_new},"holiday":{"value":holiday},
	"soup":{"value":"2342"}, "writing":{"value":"53535"}
}


openidArr = get_userId()
for index in range(len(openidArr)):
   res = wm.send_template(openidArr[index], template_id, data)
   print(res)
