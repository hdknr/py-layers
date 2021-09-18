import click

from layerslib import efs as EFS

from .utils import J, setup


@click.group()
@click.option("--profile_name", "-p", default=None)
@click.pass_context
def efs(ctx, profile_name):
    setup(ctx, profile_name)


@efs.command()
@click.pass_context
def efs_list(ctx):
    data = EFS.get_filesystem()
    click.echo(J(data))
