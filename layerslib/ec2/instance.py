import datetime

from .base import resource


class Instance:
    def __init__(self, instance):
        # ec2.instance resource
        self.instance = instance

    @property
    def name(self):
        """Instance Name"""
        return next(filter(lambda i: i["Key"] == "Name", self.instance.tags))["Value"]

    def create_image(self, name=None, description=None, no_reboot=True):
        """
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html?highlight=instance#EC2.Instance.create_image
        """
        name = name or f"{self.name}-{datetime.date.today()}"
        description = description or f"{name}"

        image = self.instance.create_image(
            Name=name,
            InstanceId=self.instance.id,
            Description=description,
            NoReboot=no_reboot,
        )
        return image  # ec2.image resource

    @classmethod
    def factory(cls, instance_id):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html?highlight=instance#instance
        return cls(next(iter(resource().instances.filter(InstanceIds=[instance_id]))))
