import json
import logging
import os

import boto3
import requests

LOGGER = logging.getLogger('notifier')

#########
# AWS
#########

config = boto3.client('config')

def get_compliance_status_report():
    non_compliant_report = get_non_compliant_report()
    

def get_non_compliant_report():
    # TODO: write terraform to save that query instead of manually doing it...
    exp = config.get_stored_query(QueryName='Count-Non-compliant')['StoredQuery']['Expression']
    results = list(map(lambda result: json.loads(result), config.select_resource_config(Expression=exp)['Results']))
    LOGGER.info(f"queries: {results}")
    return results




