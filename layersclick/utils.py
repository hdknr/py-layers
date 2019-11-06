import boto3
import json
import os
import importlib.util
from bson import json_util


def J(data, indent=2, **kwargs):
    return json.dumps(data, indent=indent, default=json_util.default, **kwargs)


def import_settings(path):
    spec = importlib.util.spec_from_file_location("local_settings", path)
    settings = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(settings)
    return settings


def create_settings(path):
    if not path:
        return None
    if path.endswith('.json'):
        return type('', (object,), json.load(open(path)))
    elif path.endswith('.py'):
        return import_settings(path)


def create_session(profile_name):
    session = boto3.Session(profile_name=profile_name)
    credentials = session.get_credentials()
    os.environ['AWS_DEFAULT_REGION'] = session.region_name
    os.environ['AWS_ACCESS_KEY_ID'] = credentials.access_key
    os.environ['AWS_SECRET_ACCESS_KEY'] = credentials.secret_key

    return (session, credentials)

def setup(ctx, profile_name, settings=None):
    if settings:
        ctx.obj['settings'] = create_settings(settings)
    if profile_name:
        (ctx.obj['session'] , ctx.obj['credentials']) = create_session(profile_name)
