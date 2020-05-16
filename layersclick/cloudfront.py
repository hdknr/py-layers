import click
import boto3
import json
import requests
from .utils import setup, J, my_ipaddress
from layerslib import cloudfront as CF


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def cloudfront(ctx, profile_name):
    setup(ctx, profile_name)


@cloudfront.command()
@click.pass_context
def distribution_list(ctx):
    '''cloudfront: list distributions'''
    # layers.py cloudfront -p profile distribution-list | jq ".DistributionList.Items[]"
    instances = CF.list_distributions()
    click.echo(J(instances))

@cloudfront.command()
@click.argument('distribution_id')
@click.argument('files', nargs=-1)
@click.pass_context
def invalidate(ctx, distribution_id, files):
    '''cloudfront: clear cache'''
    res = CF.invalidate(distribution_id, *files)
    click.echo(res)
