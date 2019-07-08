import boto3
import logging
import os
import json
import datetime
from time import mktime


LOGLEVEL = os.environ.get('LOGLEVEL', logging.INFO)

 
def getLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


def get_instances():
    ec2 = boto3.client('ec2')
    res = ec2.describe_instances(
        Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
    instances = [i["InstanceId"]
                 for r in res["Reservations"] for i in r["Instances"]]
    return instances


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)

def dumps(data):
    return json.dumps(data, cls=JSONEncoder)


def sanitize(data):
    return json.loads(dumps(data))
    
