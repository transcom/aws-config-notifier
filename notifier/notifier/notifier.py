import json
import logging
import os

import boto3

LOGGER = logging.getLogger('notifier')

#########
# AWS
#########

CONFIG = boto3.client('config')
SNS = boto3.client('sns')

def get_non_compliant_report():
    # TODO: write terraform to save that query instead of manually doing it...
    exp = CONFIG.get_stored_query(QueryName='Count-Non-compliant')['StoredQuery']['Expression']
    # the lambda below does the following:
    # the response object is described here: 
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/config.html#ConfigService.Client.select_resource_config
    # the result block, the part we care about, is actually a list of strings described below: 
    # `['{"COUNT(*)":14,"configuration":{"targetResourceType":"AWS::Logs::LogGroup"}}', '{"COUNT(*)":2,"configuration":{"targetResourceType":"AWS::S3::Bucket"}}']`
    # the lambda takes the results block, and loads each string into json, which we will pase into something easier to work with
    # this can be done in one line, but I have opted to split it up for clarity
    # if this formatted string ever changes, we will have to update this parsing. 
    results = [json.loads(result) for result in CONFIG.select_resource_config(Expression=exp)['Results']]
    results = [{"count": result["COUNT(*)"], "resource_type": result["configuration"]["targetResourceType"]} for result in results]
    LOGGER.info(f"queries: {results}")
    return results

def prepare_sns_message(title="", report=None, additional_text=""):
    """Prepares the message for sending to SNS (plain text)
    Parameters:
    title (str): title of the message
    report (list(dict)): the noncompliant resource type, and the count of that specific resource. 
    additional_text (str): ???? figure out what i wanna do there
    Returns:
    send_to_sns (bool): whether to send the string or not
    message (str): the formatted string
    """
    message = f"{title}\n```"
    if len(report) > 0: 
        message += "\n".join([f"{result['resource_type']}: {result['count']}" for result in report])
        LOGGER.info(f"message: {message}")
        message += f"```\n{additional_text}"
    
    send_to_sns = False
    if len(message) > 0:
        send_to_sns = True
    
    return send_to_sns, message

def send_sns_message(topic_arn="", payload=""):
    """
    # Sents the SNS message
    """
    payload = json.dumps(payload)

    resp = SNS.publish(
        TopicArn = topic_arn,
        Message = payload,
        Subject = "AWS Config Notifier Bot"
    )
    if 'MessageId' in resp:
        LOGGER.info('Message sent successfully sent to SNS {}, msg ID'.format(topic_arn, resp['MessageId']))
    else:
        LOGGER.error('Message could NOT be sent {}'.format(topic_arn))

def compliance_notify():
    topic_arn = os.environ.get('SNS_TOPIC', None)
    environment = os.environ.get('ENVIRONMENT', "transcom-gov-milmove-demo")
    title = f"{os.environ.get('NOTIFICATION_TITLE', 'Non-Compliant Resource Report')} for {environment}:"
    additional_text = os.environ.get('ADDITIONAL_TEXT', 
        'Please continue to: https://console.amazonaws-us-gov.com/config/home?region=us-gov-west-1#/dashboard to learn more')

    send_to_sns, messages = prepare_sns_message(title=title, report=get_non_compliant_report(), additional_text=additional_text)
    messages = "this is a test\n" + messages
    if send_to_sns and topic_arn is not None:
        send_sns_message(topic_arn=topic_arn, payload=messages)

