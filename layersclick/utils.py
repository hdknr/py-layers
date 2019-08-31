import boto3
import json
import os


def J(data, indent=2, **kwargs):
    return json.dumps(data, indent=indent, **kwargs)

def setup(ctx, profile_name):

    if profile_name:
        session = boto3.Session(profile_name=profile_name)
        credentials = session.get_credentials()
        ctx.obj['session'] = session
        ctx.obj['credentials'] = credentials
    
        os.environ['AWS_DEFAULT_REGION'] = session.region_name
        os.environ['AWS_ACCESS_KEY_ID'] = credentials.access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = credentials.secret_key
