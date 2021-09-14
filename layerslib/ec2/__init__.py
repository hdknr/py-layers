import json

from .base import client, resource
from .instance import Instance  # NOQA


def F(key, value):
    value = isinstance(value, list) and value or [value]
    return dict(Name=key, Values=value)


def TK(name):
    return F("tag-key", name)


def TV(value):
    return F("tag-value", value)


def TKV(name, value):
    return [TK(name), TV(value)]


def FS(*attr, tag=()):
    fset = [F(*a) for a in attr] + (TKV(*tag) if tag else [])
    return fset


ATTR_IS_RUNNNING = ("instance-state-name", "running")


def vpcs(name=None):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_vpcs
    args = name and dict(
        Filters=[{"Name": "tag:Name", "Values": [name]}]) or {}
    res = client().describe_vpcs(**args)
    return res.get("Vpcs", [])


def get_vpc(name):
    res = vpcs(name)
    if len(res) == 1:
        # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#vpc
        return resource().Vpc(res[0]["VpcId"])


def all_secgroups(name=None):
    vpc_ids = [i["VpcId"] for i in vpcs()]
    Filters = [dict(Name="vpc-id", Values=vpc_ids)]
    response = client().describe_security_groups(Filters=Filters)
    if name:
        return [i for i in response.get("SecurityGroups", []) if json.dumps(i).find(name) >= 0]

    return response.get("SecurityGroups", [])


def authorize_port(group_id, description, port, cidrs=None, cidrs_v6=None, proto="tcp"):
    cidrs = cidrs or []
    cidrs_v6 = cidrs_v6 or []
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.authorize_security_group_ingress
    ips = [dict(CidrIp=i, Description=description) for i in cidrs]
    ips_v6 = [dict(CidrIpv6=i, Description=description) for i in cidrs_v6]

    perms = dict(IpProtocol=proto, FromPort=port,
                 ToPort=port, IpRanges=ips, Ipv6Ranges=ips_v6)

    return client().authorize_security_group_ingress(GroupId=group_id, IpPermissions=[perms])


def revoke_port(group_id, cidr, port, proto="tcp"):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.SecurityGroup.revoke_ingress
    sg = resource().SecurityGroup(group_id)
    return sg.revoke_ingress(
        CidrIp=cidr,
        IpProtocol=proto,
        FromPort=port,
        ToPort=port,
    )


def list_security_groups():
    res = client().describe_security_groups()
    return res["SecurityGroups"]


def get_security_group(id):
    res = resource().SecurityGroup(id)
    return res


def find_cidrs(rule, ip, word):
    return list(
        map(lambda i: i[f"Cidr{ip}"], filter(lambda i: i.get(
            "Description", "").find(word) >= 0, rule[f"{ip}Ranges"]))
    )
