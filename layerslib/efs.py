import boto3


def client():
    return boto3.client("efs")


def get_filesystem(filters=None):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/efs.html#EFS.Client.describe_file_systems
    q = filters and dict(Filters=filters) or {}
    return client().describe_file_systems(**q)
