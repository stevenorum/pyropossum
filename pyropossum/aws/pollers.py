#!/usr/bin/env python3

import boto3
from datetime import datetime
import json
# For some reason the following import isn't working on the raspberry pi.
# Probably due to python 3.4 vs 3.6 or something like that.
# from json.decoder import JSONDecodeError
import logging
import threading

logger = logging.getLogger(__name__)

class Request(object):
    '''Wrapper object for a binary on/off request.'''
    def __init__(self, enable, receipt_handle, click_type=None, serial_number=None, timestamp=None, battery_voltage=None, source=None, targets=[], valid=True):
        self.enable = enable
        self.click_type = click_type
        self.receipt_handle = receipt_handle
        self.source = 'BUTTON' if serial_number else source
        self.serial_number = serial_number if serial_number else source
        self.battery_voltage = battery_voltage
        self.timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ') if timestamp else datetime.utcnow()
        self.targets = targets
        self.valid = valid
        pass

    def repr(self):
        return json.dumps(self.dictify())

    def dictify(self):
        return {
            "enable":self.enable,
            "click_type":self.click_type,
            "receipt_handle":self.receipt_handle,
            "source":self.source,
            "serial_number":self.serial_number,
            "battery_voltage":self.battery_voltage,
            "timestamp":self.timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ') if self.timestamp else None,
            "targets":self.targets,
            "valid":self.valid
        }

    @classmethod
    def from_sqs(cls, message):
        try:
            contents = json.loads(message['Body'])
        # See note in imports
        # except JSONDecodeError as e:
        except:
            return cls(enable=False, receipt_handle=message['ReceiptHandle'], valid=False)
        sns_topic = contents.get('TopicArn', None)
        if sns_topic:
            # It's SNS->SQS
            inner_message = json.loads(contents['Message'])
            if 'clickType' in inner_message:
                # It's an IoT button click
                return cls(enable=inner_message['clickType']=='SINGLE',
                           receipt_handle=message['ReceiptHandle'],
                           click_type=inner_message['clickType'],
                           serial_number=inner_message['serialNumber'],
                           battery_voltage=inner_message['batteryVoltage'],
                           timestamp=contents['Timestamp'])
            else:
                # Nothing else written yet.
                return cls(enable=False, receipt_handle=message['ReceiptHandle'], valid=False)
        else:
            # Raw SQS
            if contents.get("source","").lower() in ["cli","alexa"]:
                return cls(enable=contents.get("enable"),
                           receipt_handle=message['ReceiptHandle'],
                           targets=contents.get("targets", [])
                )
            # Nothing else written yet.
            return cls(enable=False, receipt_handle=message['ReceiptHandle'], valid=False)

def exec_actions(actions, *args, **kwargs):
    '''Call each function in actions, with the specified args and kwargs'''
    for action in actions:
        action(*args, **kwargs)
        pass
    pass

class SqsPoller(object):
    '''Object to handle polling an SQS queue for messages.'''
    def __init__(self, queue_url, sqs_client=None, enable_actions=[], disable_actions=[], poll_size=1, poll_length=20, processing_time=15):
        self.queue_url = queue_url
        self.sqs_client = sqs_client if sqs_client else boto3.client('sqs')
        self.poll_size = poll_size
        self.poll_length = poll_length
        self.processing_time = processing_time
        self.enable_actions = enable_actions
        self.disable_actions = disable_actions
        self.polling = False
        self.finished = False
        self.thread = None
        pass

    def _poll(self):
        while self.polling:
            messages = self.sqs_client.receive_message(
                QueueUrl=self.queue_url,
                AttributeNames=['All'],
                MaxNumberOfMessages=self.poll_size,
                VisibilityTimeout=self.processing_time,
                WaitTimeSeconds=self.poll_length
            ).get('Messages',[])
            if not messages:
                continue
            logger.debug("Number of messages: {}".format(len(messages)))
            for message in messages:
                request = Request.from_sqs(message)
                if request:
                    logger.info("Request received: " + request.repr())
                    if request.valid:
                        if request.enable:
                            exec_actions(self.enable_actions, request)
                            pass
                        else:
                            exec_actions(self.disable_actions, request)
                            pass
                        pass
                    self.sqs_client.delete_message(QueueUrl=self.queue_url,ReceiptHandle=request.receipt_handle)

    def start_polling_async(self):
        self.polling = True
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self._poll)
            self.thread.daemon = True
            self.thread.start()
            pass
        pass

    def start_polling(self):
        self.polling = True
        self._poll()

    def stop_polling(self):
        self.polling = False
