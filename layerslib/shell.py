import boto3
import os

LOG = os.environ.get('LOG', '/aws/lambda/shell')

def run_command(instances, commands, timeout="3600"):
    ssm = boto3.client('ssm')
    return ssm.send_command(
        InstanceIds=instances,
        DocumentName="AWS-RunShellScript",
        Parameters={
            "commands": commands,
            "executionTimeout": [timeout]
        },
        CloudWatchOutputConfig={
            'CloudWatchLogGroupName': LOG,
            'CloudWatchOutputEnabled': True
        }
    )


def main(event, context, commands, instances):
    return run_command(instances, commands)
