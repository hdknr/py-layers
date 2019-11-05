import click
import boto3
from .utils import setup, J
from layerslib.logs import filter_events, all_groups


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def logs(ctx, profile_name):
    setup(ctx, profile_name)


@logs.command()
@click.argument('group_name')
@click.argument('pattern')
@click.option('--seconds', '-s', default=None)
@click.pass_context
def filter(ctx, group_name, pattern, seconds):
    try:
        res = filter_events(group_name, pattern, seconds=seconds)
        print(J(res))
    except:
        import traceback
        print(traceback.format_exc())


@logs.command()
@click.pass_context
def list_groups(ctx):
    res = all_groups()
    click.echo(J(res))
