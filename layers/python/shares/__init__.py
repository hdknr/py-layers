import boto3
import logging
import os
import json
import datetime
from time import mktime
import urllib.request 


LOGLEVEL = os.environ.get('LOGLEVEL', logging.INFO)


def request(url):
    req = urllib.request.Request(url)                                                                                       
    return urllib.request.urlopen(req)
 
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


def ec2_address():
    url = 'http://169.254.169.254/latest/meta-data/public-ipv4'                                                             
    with request(url) as res:
        return res.read().decode('utf8')


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return int(mktime(obj.timetuple()))
        return json.JSONEncoder.default(self, obj)

def dumps(data):
    return json.dumps(data, cls=JSONEncoder)


def sanitize(data):
    return json.loads(dumps(data))
    

class Aws(object):
    _client_name = ''
    _session = None
     
    def __init__(self, session=None, profile_name=None):
        self._session = session or boto3.Session(profile_name=profile_name)
        self._current_client = None

    @property
    def session(self):
        return self._session

    @property
    def credentials(self):
        return self.sessin.get_credentials()
 
    def get_client(self, client_name=None, region_name=None):
        kwargs = {}
        if not client_name:
            client_name = self._client_name
        if region_name:
            kwargs['region_name'] = region_name

        return self.session.client(client_name, **kwargs)

    def set_current_client(self, client=None, client_name=None, region_name=None):
        self._current_client = client or self.get_client(
            client_name=client_name, region_name=region_name)

    @property
    def client_name(self):
        return self._client_name

    @property
    def client(self):
        return self._current_client
