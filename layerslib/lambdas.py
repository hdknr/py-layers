import boto3


def client():
    return boto3.client("lambda")
