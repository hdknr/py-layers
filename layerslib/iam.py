import itertools

import boto3


def client():
    return boto3.client("iam")


def resource():
    return boto3.resource("iam")


def _M(data, key="ResponseMetadata"):
    data.pop(key)
    return data


def groups_for_user(user_name):
    return client().list_groups_for_user(UserName=user_name).get("Groups", [])


def group_policies_for_group(group_name):
    return client().list_group_policies(GroupName=group_name).get("PolicyNames", [])


def policies_for_group(group_name):
    return [
        _M(client().get_group_policy(GroupName=group_name, PolicyName=p)) for p in group_policies_for_group(group_name)
    ]


def user_policies_for_user(user_name):
    return [
        _M(client().get_user_policy(UserName=user_name, PolicyName=p))
        for p in client().list_user_policies(UserName=user_name).get("PolicyNames", [])
    ]


def group_policies_for_user(user_name, groups=None):
    groups = groups or groups_for_user(user_name) or []
    return list(itertools.chain(*[policies_for_group(g["GroupName"]) for g in groups]))


def policies_for_user(user_name, groups=None):
    groups = groups or groups_for_user(user_name) or []
    return dict(
        Groups=groups,
        UserPolicies=user_policies_for_user(user_name),
        GroupPolicies=group_policies_for_user(user_name, groups=groups),
    )


def describe_user(user_name):
    user = _M(client().get_user(UserName=user_name))
    policies = policies_for_user(user_name)
    user.update(policies)
    return user
