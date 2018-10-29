#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Send a message to the specific phone using Aliyun SMS.
wwwglin
20171008
'''

import sys
import datetime
import random
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
import requests

reload(sys)
sys.setdefaultencoding('utf8')

# Do NOT change the REGION
REGION = "cn-hangzhou"
# ACCESS_KEY_ID/ACCESS_KEY_SECRET. Change them based on author info.
ACCESS_KEY_ID = "YOUR ACCESS_KEY_ID"
ACCESS_KEY_SECRET = "YOUR ACCESS_KEY_SECRET"

acs_client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)


def send_sms(business_id, phone_numbers, sign_name, template_code, template_param=None):
    smsRequest = SendSmsRequest.SendSmsRequest()
    # The Template Code is necessary.
    smsRequest.set_TemplateCode(template_code)

    # The Template parameters are necessary.
    if template_param is not None:
        smsRequest.set_TemplateParam(template_param)

    # The request number is necessary.
    smsRequest.set_OutId(business_id)

    # The sign name is necessary.

    smsRequest.set_SignName(sign_name);
    # The destnation phone number is necessary.
    smsRequest.set_PhoneNumbers(phone_numbers)

    # Call the sms sending interface. Return json.
    smsResponse = acs_client.do_action_with_exception(smsRequest)

    # Add the service handling logic here.

    return smsResponse


def query_send_detail(biz_id, phone_number, page_size, current_page, send_date):
    queryRequest = QuerySendDetailsRequest.QuerySendDetailsRequest()
    # The phone number to be checked
    queryRequest.set_PhoneNumber(phone_number)
    # The BizId is selected.
    queryRequest.set_BizId(biz_id)
    # The sending date is necessary. Support to the date in 30 days. eg. yyyyMMdd
    queryRequest.set_SendDate(send_date)
    # The maxinum item number in the current page is necessary.
    queryRequest.set_CurrentPage(current_page)
    # The page size is necessary.
    queryRequest.set_PageSize(page_size)

    # Call the sms record checking interface. Return json.
    queryResponse = acs_client.do_action_with_exception(queryRequest)

    # Add the service handling logic here.

    return queryResponse


# Calc the memorial day
date_now = datetime.datetime.now()
date_start = datetime.datetime(2012, 12, 3)
memorial_day = (date_now - date_start).days
Off_site_day = (date_now - datetime.datetime(2017, 8, 30)).days


# get wheather
def weather(parameters):
    # 中国天气网
    # url1 = 'http://www.weather.com.cn/data/cityinfo/101100402.html'
    url2 = 'https://free-api.heweather.com/s6/weather/forecast?' + parameters

    # 发送请求
    r = requests.get(url2)
    # 设置编码
    r.encoding = "utf-8"
    # 拿到结果
    weather = r.json()
    city = weather['HeWeather6'][0]['basic']['location']
    tmp_max = weather['HeWeather6'][0]['daily_forecast'][0]['tmp_max']
    tmp_min = weather['HeWeather6'][0]['daily_forecast'][0]['tmp_min']

    msg = city + '最高气温' + tmp_max + '℃,最低气温' + tmp_min + '℃.'
    return msg


def course():
    # 课程存储
    courseLinDan = [['下二测试408'], ['上二设计211'], ['自由!!!'], ['上一设计507', '上二云平台315'], ['下二挖掘216']]
    courseLinShuang = [['下二测试408'], ['上二挖掘206', '下二云平台408'], ['自由!!!'], ['上一设计507', '上二云平台315'], ['上一测试415', '下二挖掘216']]
    courseYueDan = [['上午!!!'], ['下午!!!'], ['上午!!!'], ['自由!!!'], ['自由!!!']]
    courseYueShuang = [['上午!!!'], ['下午!!!'], ['上午!!!'], ['自由!!!'], ['自由!!!']]
    # 课程开始时间
    date_now = datetime.datetime.now()
    # date_now = datetime.datetime(2018, 4, 12)
    date_start = datetime.datetime(2018, 4, 2)
    memorial_day = (date_now - date_start).days
    today_num = memorial_day % 7  # today_num 星期几
    isDan = memorial_day / 7  # 单双周
    if isDan % 2 == 1:
        day_course = [courseLinDan[today_num], courseYueDan[today_num]]
    else:
        day_course = [courseLinShuang[today_num], courseYueShuang[today_num]]
    return day_course


# Print the prompt infomation
print "\n%s\n===============================" \
      % date_now.strftime('%Y-%m-%d %H:%M:%S')

# Main
__name__ = 'send'
if __name__ == 'send':
    __business_id = uuid.uuid1()
    print __business_id
    #输入查询参数
    parameters1 = 'key=5a8e875a4ad44e54a934e92088108dc3&location=榆次'
    parameters2 = 'key=5a8e875a4ad44e54a934e92088108dc3&location=呼和浩特'
    weatherYuci = weather(parameters1)
    weatherHushi = weather(parameters2)
    weatherHushi = weatherHushi[0:len(weatherHushi)-1]
    day = str(memorial_day) + '天，' + '异地第' + str(Off_site_day)

    day_course = course()
    day_course = course()
    classLin = ''
    classYue = ''
    for i in day_course[0]:
        classLin = classLin + ',' + i
    classLin = classLin[1:len(classLin)]  # 去除开头的，
    classLin = ':'+classLin + ';'
    for i in day_course[1]:
        classYue = classYue + ',' + i
    classYue = classYue[1:len(classYue)]  # 去除开头的，
    classYue = ':' + classYue
    params = "{\"name\":\"%s\",\"say\":\"%s\",\"wether1\":\"%s\",\"wether2\":\"%s\",\"class1\":\"%s\",\"class2\":\"%s\"}" % (
        "马小妖", day, weatherYuci, weatherHushi, classLin, classYue)
    print send_sms(__business_id, you_phone, "异地小助手", "SMS_130921445", params)

    params = "{\"name\":\"%s\",\"say\":\"%s\",\"wether1\":\"%s\",\"wether2\":\"%s\",\"class1\":\"%s\",\"class2\":\"%s\"}" % (
        "wwwglin", day, weatherYuci, weatherHushi, classLin, classYue)
    print send_sms(__business_id, 'you_phone', "异地小助手", "SMS_130921445", params)
