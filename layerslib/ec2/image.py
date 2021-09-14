from .base import client


def create_image(instance_id, ami_name, description):
    return client().create_image(Description=description, NoReboot=True, InstanceId=instance_id, Name=ami_name)


def delete_image(image_id):
    """
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.deregister_image
    """
    return client().deregister_image(ImageId=image_id)


def get_images(owners=None, filters=None):
    """
    - https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_images
    - https://docs.aws.amazon.com/ja_jp/AWSEC2/latest/APIReference/API_DescribeImages.html
    """
    owners = owners or ["self"]
    filters = filters or []

    q = filters and dict(Filters=filters) or {}
    images = client().describe_images(Owners=owners, **q)["Images"]
    return images


def get_image_ids(*args, **kwargs):
    return [i["ImageId"] for i in get_images(*args, **kwargs)]
