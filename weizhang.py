# -*- coding: utf-8 -*-
'''
Send a message to the specific phone using Aliyun SMS.
Shane Wang
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
import urllib2, json, urllib

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
# get weizhangstatus
def query(lsnum,engineno):
    data = {}
    appkey = "0d492f59f05a97ab"
    data["carorg"] = "shanxi"  # 交管局代号
    data["lsprefix"] = "晋"  # 车牌前缀 utf8
    data["lsnum"] = lsnum  # 车牌
    data["lstype"] = "02"  # 车辆类型
    data["engineno"] = engineno # 发动机号
    # data["lsnum"] = "E8C916"  # 车牌
    # data["lstype"] = "02"  # 车辆类型
    # data["engineno"] = "D3031129"  # 发动机号
    data["frameno"] = ""  # 车架号
    url_values = urllib.urlencode(data)
    url = "http://api.jisuapi.com/illegal/query?appkey=" + appkey
    request = urllib2.Request(url, url_values)
    result = urllib2.urlopen(request)
    jsonarr = json.loads(result.read())

    if jsonarr["status"] != u"0":
        print jsonarr["msg"]
        return jsonarr["msg"]
        exit()
    result = jsonarr["result"]
    print result
    if isinstance(result, list):
        for val in result["list"]:
            print val["time"], val["address"], val["content"], val["legalnum"], val["price"], val["score"]
    else:
        print "恭喜您，没有违章！"
        return "恭喜您，没有违章！"

# Main
__name__ = 'send'
if __name__ == 'send':
    __business_id = uuid.uuid1()
    parameters1 = 'key=5a8e875a4ad44e54a934e92088108dc3&location=榆次'
    parameters2 = 'key=5a8e875a4ad44e54a934e92088108dc3&location=呼和浩特'
    status = query('ESS888','606268972')
    params = "{\"name\":\"%s\",\"status\":\"%s\"}" % (
        "王先生", status)
    print send_sms(__business_id, '13835650229', "异地小助手", "SMS_125116761", params)

    status = query('EMY180', '144259')
    params = "{\"name\":\"%s\",\"status\":\"%s\"}" % (
        "马先生", status)
    print send_sms(__business_id, '13934322840', "异地小助手", "SMS_125116761", params)
