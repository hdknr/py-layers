#!/usr/bin/env python
import click
import boto3
import json

from .utils import setup, J

SERVICE = {
    'ec2': "ec2.amazonaws.com",
    'lambda': "lambda.amazonaws.com",
}

def service_policy(service):
    return json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": service,
                },
                "Action": "sts:AssumeRole"
            }
        ]
    })

@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def iam(ctx, profile_name):
    setup(ctx, profile_name)


def client():
    return boto3.client('iam')


def resource():
    return boto3.resource('iam')

@iam.command()
@click.pass_context
def role_list(ctx):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_roles
    res = client().list_roles()
    click.echo(J(res))


@iam.command()
@click.argument('name')
@click.pass_context
def role_detail(ctx, name):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.get_role
    res = client().get_role(RoleName=name)
    click.echo(J(res))


@iam.command()
@click.argument('name')
@click.argument('service')
@click.pass_context
def role_create(ctx, name, service):
    '''Create Role (for ec2, lambda) '''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.create_role
    service_code = SERVICE.get(service, None)
    if service_code:
        res = client().create_role(
            RoleName=name,
            AssumeRolePolicyDocument=service_policy(service_code),
        )
        click.echo(J(res))


@iam.command()
@click.option('--allpolicy', '-a', is_flag=True)
@click.pass_context
def policy_list(ctx, allpolicy):
    ''' List Policy(Attached) '''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_policies
    attached = not allpolicy 
    res = client().list_policies(OnlyAttached=attached)
    click.echo(J(res))


@iam.command()
@click.argument('role')
@click.argument('policy')
@click.pass_context
def role_policy_create(ctx, role, policy):
    '''Attache a Policy to a Role'''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.attach_role_policy
    res = client().attach_role_policy(
        RoleName=role,
        PolicyArn=policy,
    )
    click.echo(J(res))


@iam.command()
@click.argument('name')
@click.pass_context
def role_policy_list(ctx, name):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_role_policies
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iam.html#IAM.Client.list_attached_role_policies

    p = client().list_role_policies(RoleName=name)
    ap = client().list_attached_role_policies(RoleName=name)
    data = {
        'PolicyNames':  p['PolicyNames'], 
        'AttachedPolicies': ap['AttachedPolicies'],
    }
    click.echo(J(data))
