import click
import boto3
import json
import requests
from itertools import chain
from .utils import setup, J, my_ipaddress
from layerslib import ec2 as EC2 , cloudfront as CF


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def ec2(ctx, profile_name):
    setup(ctx, profile_name)


@ec2.command()
@click.pass_context
def instance_list(ctx):
    '''ec2: get Instance
    
    layers ec2 -p yourog instance-list | jq -r ".[] | [.InstanceId, .Tags[0].Value, .SecurityGroups[0].GroupName, .SecurityGroups[0].GroupId] | @csv" | csvtomd
    '''
    instances = EC2.get_instances()
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
    response = EC2.all_secgroups(name=group)
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
    response = EC2.all_secgroups(name=group)
    group_ids = [i['GroupId'] for i in response]
    myip = my_ipaddress() 
    for gid in group_ids:
        click.echo(f"allowing {gid}: {proto}/{port} for {myip}")
        res = EC2.authorize_port(gid, description, int(port), cidrs=[f"{myip}/32"], proto=proto)
        click.echo(J(res))


@ec2.command()
@click.argument('port')
@click.option('--group', '-g', default=None, help="Security Group Name(Name, tag:Name,)")
@click.option('--proto', '-p', default='tcp', help="Protocol(tcp|udp|...)")
@click.pass_context
def myip_reject(ctx, port, group, proto):
    response = EC2.all_secgroups(name=group)
    group_ids = [i['GroupId'] for i in response]
    myip = my_ipaddress() 
    for gid in group_ids:
        click.echo(f"rejecting {gid}: {proto}/{port} for {myip}")
        res = EC2.revoke_port(gid, f"{myip}/33", int(port), proto)
        click.echo(J(res))


@ec2.command()
@click.argument('group_id')
@click.pass_context
def sg_rule_list(ctx, group_id):
    ''' IP Permissions for Security Group'''
    # jq '.[] | select(.ToPort=1433) | .IpRanges[] | [.CidrIp, .Descri^Cion] | @tsv'
    sg = EC2.get_security_group(group_id)
    res = sg.ip_permissions
    click.echo(J(res))


@ec2.command()
@click.argument('group_id')
@click.option('--word', '-w', default='CloudFront', help="CloudFront")
@click.option('--port', '-p', default=80, help="Service Port")
@click.option('--dry', '-d', default=False, is_flag=True, help="CloudFront")
@click.pass_context
def allow_cloudfront_ip(ctx, group_id, word, port, dry):
    '''Allow CloudFront Edge Servers to access this Security Group'''
    # https://console.aws.amazon.com/support/home#/case/create?issueType=service-limit-increase&limitType=vpc

    sg = EC2.get_security_group(group_id)

    rules = list(filter(
        lambda i: all([i['IpProtocol'] == 'tcp', i['FromPort'] == port, i['ToPort'] == port, ]),
        sg.ip_permissions,
    ))

    sg_cidrs_ip = list(chain(*(EC2.find_cidrs(rule, 'Ip', word) for rule in rules)))
    sg_cidrs_ipv6 = list(chain(*(EC2.find_cidrs(rule, 'Ipv6', word) for rule in rules)))

    cidrs_ip, cidrs_ipv6 = CF.edge_server_cidrs()

    new_cidrs_ip = list(filter(lambda i: i not in sg_cidrs_ip, cidrs_ip))
    new_cidrs_ipv6 = list(filter(lambda i: i not in sg_cidrs_ipv6, cidrs_ipv6))

    if dry:
        click.echo(new_cidrs_ip) 
        click.echo(new_cidrs_ipv6) 
    elif len(new_cidrs_ip) > 0 or len(new_cidrs_ipv6) > 0:
        EC2.authorize_port(group_id, word, port, new_cidrs_ip, new_cidrs_ipv6)


@ec2.command()
@click.pass_context
def sg_list(ctx):
    '''Security Group: List
    layers ec2 -p youorg sg-list | jq -r ".[] | [.GroupId, .Tags[0].Value, .Description] | @csv" | csvtomd
    '''
    res = EC2.list_security_groups()
    click.echo(J(res))
