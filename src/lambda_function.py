import logging
import os
import json
import urllib.request
from datetime import datetime, timedelta


WEBHOOK_URL = os.environ['WEBHOOK_URL']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_slack(account, event_name, event_time, user_name, source_ip, sg_id):
    
    headers = {'Content-Type': 'application/json'}
    
    slack_payload = {
        'username': 'Security Group 변경 알림',
        'icon_emoji': ':aws:',
        'attachments': [
            {
                'color': '#FFBE33',
                'blocks': [
                    {
                        'type': 'header',
                        'text': {
                            'type': 'plain_text',
                            'text': 'Security Group 변경이 감지되었습니다.',
                            'emoji': True
                        }
                    },
                    {
                        'type': 'section',
                        'fields': [
                            {
                                'type': 'mrkdwn',
                                'text': f"*Account*\n {account}"
                            },
                            {
                                'type': 'mrkdwn',
                                'text': f'*Event Name*\n {event_name}'
                            }
                        ]
                    },
                    {
                        'type': 'section',
                        'fields': [
                            {
                                'type': 'mrkdwn',
                                'text': f"*Event Time*\n {event_time}"
                            },
                            {
                                'type': 'mrkdwn',
                                'text': f"*User*\n {user_name}"
                            }
                        ]
                    },
                    {
                        'type': 'section',
                        'fields': [
                            {
                                'type': 'mrkdwn',
                                'text': f'*Source IP*\n {source_ip}'
                            },
                            {
                                'type': 'mrkdwn',
                                'text': f'*Security Group ID*\n {sg_id}'
                            }
                        ]
                    }
                ]
            }
        ]
    }
    
    data = json.dumps(slack_payload).encode('utf-8')
    
    req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
    
    response = urllib.request.urlopen(req)
    
    response_status = response.getcode()
    
    if response_status == 200:
        logger.info('Message posted successfully')
    else:
        logger.error(f'Failed to post message, status code: {response_status}')

def convert_timezone(event_time_utc):
    
    logger.info(f'Event Time (UTC): {event_time_utc}')
    
    time_format = '%Y-%m-%dT%H:%M:%SZ'
    utc_time = datetime.strptime(event_time_utc, time_format)
    kst_time = utc_time + timedelta(hours=9)
    event_time_kst = kst_time.strftime(time_format)

    return event_time_kst

def lambda_handler(event, context):
    
    logger.info(f'Event: {event}')
    logger.info(f'Lambda function ARN: {context.invoked_function_arn}')
    logger.info(f'Lambda Request ID:, {context.aws_request_id}')
    
    payload = event.get('detail')
    
    account = payload.get('userIdentity').get('accountId')
    user_name = payload.get('userIdentity').get('userName')
    source_ip = payload.get('sourceIPAddress')
    event_name = payload.get('eventName')
    event_time_utc = payload.get('eventTime')
    event_time_kst = convert_timezone(event_time_utc)
    
    if event_name == 'CreateSecurityGroup':
        sg_id = payload.get('responseElements').get('groupId')
    else:
        sg_id = payload.get('requestParameters').get('groupId')
    
    
    send_slack(account, event_name, event_time_kst, user_name, source_ip, sg_id)
    