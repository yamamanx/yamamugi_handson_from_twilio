# coding:utf-8

import logging
import traceback
import boto3
import os
import json


log_level = os.environ.get('LOG_LEVEL', 'INFO')

logger = logging.getLogger()

if log_level == 'ERROR':
    logger.setLevel(logging.ERROR)
elif log_level == 'DEBUG':
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        logger.debug(event)
        if event['param']['Digits'] != '1':
            return {'say': '1番以外が押されましたので申込を中止します'}

        phone_number = event['param']['From'].replace('+81', '0').replace('-', '')
        logger.debug(phone_number)

        response_event = {
            'phone_number': phone_number
        }
        logger.debug(response_event)

        client = boto3.client('stepfunctions')
        client.start_execution(
            stateMachineArn=os.environ['STATE_MACHINE_ARN'],
            input=json.dumps(response_event)
        )

        return {'say': 'お申込みありがとうございます。受け付け完了いたしました。'}

    except Exception as e:
        logger.error(traceback.format_exc())
        raise (traceback.format_exc())
