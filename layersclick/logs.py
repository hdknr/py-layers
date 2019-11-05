import click
import boto3
from .utils import setup, J
from layerslib.logs import filter_events


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def logs(ctx, profile_name):
    setup(ctx, profile_name)


@logs.command()
@click.argument('group_name')
@click.argument('pattern')
@click.pass_context
def filter(ctx, group_name, pattern):
    res = filter_events(group_name, pattern)
    print(J(res))
