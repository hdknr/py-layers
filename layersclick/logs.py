import click

from layerslib.logs import all_groups, filter_events

from .utils import J, setup


@click.group()
@click.option("--profile_name", "-p", default=None)
@click.pass_context
def logs(ctx, profile_name):
    setup(ctx, profile_name)


@logs.command()
@click.argument("group_name")
@click.argument("pattern")
@click.option("--seconds", "-s", default=None)
@click.pass_context
def filter(ctx, group_name, pattern, seconds):
    res = filter_events(group_name, pattern, seconds=seconds)
    click.echo(J(res))


@logs.command()
@click.pass_context
def list_groups(ctx):
    res = all_groups()
    click.echo(J(res))
