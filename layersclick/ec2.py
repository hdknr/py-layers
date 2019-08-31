import click
import boto3
from .utils import setup, J
from layerslib.ec2 import get_instances


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def ec2(ctx, profile_name):
    setup(ctx, profile_name)


@ec2.command()
@click.pass_context
def list_instance(ctx):
    '''ec2: get Instance'''
    instances = get_instances()
    click.echo(instances)
