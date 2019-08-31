import boto3


def F(key, value):
    value = isinstance(value, list) and value or [value]
    return  dict(Name=key, Values=value)


def TK(name):
    return F('tag-key', name)


def TV(value):
    return F('tag-value', value)


def TKV(name, value):
    return [TK(name), TV(value)]


def FS(*attr, tag=()):
    fset = [F(*a) for a in attr] + (TKV(*tag) if tag else [])
    return fset


ATTR_IS_RUNNNING = ('instance-state-name', 'running')


def get_instances(filters=[]):
    '''
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_instances
    - https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/APIReference/API_DescribeInstances.html
    '''
    ec2 = boto3.client('ec2')
    q = filters and dict(Filters=filters) or {}
    res = ec2.describe_instances(**q)
    instances = [i for r in res["Reservations"] for i in r["Instances"]]
    return instances


def get_instance_ids(*args, **kwargs):
    return [i['InstanceId'] for i in get_instances(*args, **kwargs)]


def create_image(instance_id, ami_name, description):
    ec2 = boto3.client('ec2')
    return ec2.create_image(
        Description=description,
        NoReboot=True,
        InstanceId=instance_id,
        Name=ami_name
    )


def delete_image(image_id):
    '''
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.deregister_image
    '''
    ec2 = boto3.client('ec2')
    return ec2.deregister_image(ImageId=image_id)


def get_images(owners=['self'], filters=[]):
    '''
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images
    - https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/APIReference/API_DescribeImages.html
    '''
    ec2 = boto3.client('ec2')
    q = filters and dict(Filters=filters) or {}
    images = ec2.describe_images(Owners=owners, **q)['Images']
    return images


def get_image_ids(*args, **kwargs):
    return [i['ImageId'] for i in get_images(*args, **kwargs)]
