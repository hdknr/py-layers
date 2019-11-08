import click
import boto3
import json
from .utils import setup, J, my_ipaddress
from layerslib.ec2 import get_instances, all_secgroups, authorize_port, revoke_port


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def ec2(ctx, profile_name):
    setup(ctx, profile_name)


@ec2.command()
@click.pass_context
def instance_list(ctx):
    '''ec2: get Instance'''
    instances = get_instances()
    click.echo(J(instances))


@ec2.command()
@click.option('--name', '-n', default=None)
@click.pass_context
def vpc_detail(ctx, name):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs 
    response = vpcs(name=name)
    click.echo(J(response))


@ec2.command()
@click.option('--group', '-g', default=None, help="Group Name")
@click.pass_context
def port_list(ctx, group):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_security_groups
    response = all_secgroups(name=group)
    for g in response:
        for p in g.get('IpPermissions', []):
            for r in p.get('IpRanges', []):
                description = r.get('Description', '')
                click.echo(
                    f"{g['VpcId']} {p['IpProtocol']}/{p['FromPort']} {r['CidrIp']} {description}"
                )

@ec2.command()
@click.argument('vpc')
@click.pass_context
def vpc_instance_list(ctx, vpc):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Vpc.instances
    vpcobj = get_vpc(vpc)
    # <class 'boto3.resources.collection.ec2.Vpc.instancesCollection'>
    instances = vpcobj.instances.all()  # ec2.Vpc.instancesCollection
    for instance in instances:
        # boto3.resources.factory.ec2.Instance
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Instance
        click.echo(J(instance.tags))



@ec2.command()
@click.argument('port')
@click.argument('description')
@click.option('--group', '-g', default=None, help="Security Group Name(Name, tag:Name,)")
@click.option('--proto', '-p', default='tcp', help="Protocol(tcp|udp|...)")
@click.pass_context
def myip_allow(ctx, port, description, group, proto):
    ''' Allow *PORT* number for current computer network '''
    response = all_secgroups(name=group)
    group_ids = [i['GroupId'] for i in response]
    myip = my_ipaddress() 
    for gid in group_ids:
        click.echo(f"allowing {gid}: {proto}/{port} for {myip}")
        res = authorize_port(gid, description,  f"{myip}/32", int(port), proto)
        click.echo(J(res))


@ec2.command()
@click.argument('port')
@click.option('--group', '-g', default=None, help="Security Group Name(Name, tag:Name,)")
@click.option('--proto', '-p', default='tcp', help="Protocol(tcp|udp|...)")
@click.pass_context
def myip_reject(ctx, port, group, proto):
    response = all_secgroups(name=group)
    group_ids = [i['GroupId'] for i in response]
    myip = my_ipaddress() 
    for gid in group_ids:
        click.echo(f"rejecting {gid}: {proto}/{port} for {myip}")
        res = revoke_port(gid, f"{myip}/33", int(port), proto)
        click.echo(Jl(res))
