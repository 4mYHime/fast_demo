# coding=utf-8
import json
import logging

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from celery import Celery

from setting import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ali_cloud = settings.ALiCloud()

app = Celery('tasks',
             broker=settings.CELERY_REDIS_URL,
             backend=settings.CELERY_REDIS_URL)


@app.task
def send_sms(phone, sign_name, template_code, template_params=None):
    client = AcsClient(ali_cloud.ACCESS_KEY_ID, ali_cloud.ACCESS_KEY_SECRET, ali_cloud.REGION)
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', sign_name)
    request.add_query_param('TemplateCode', template_code)
    request.add_query_param('TemplateParam', template_params)
    response = client.do_action_with_exception(request)
    # TODO response未理想返回告警
    return json.loads(response)
