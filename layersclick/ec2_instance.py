import click

from layerslib.ec2 import instance

from .utils import J, setup


@click.group()
@click.option("--profile_name", "-p", default=None)
@click.pass_context
def ec2_instance(ctx, profile_name):
    setup(ctx, profile_name)


@ec2_instance.command()
@click.pass_context
def instance_list(ctx):
    """ec2: get Instance

    layers ec2 -p yourog instance-list \
        | jq -r ".[] | [
            .InstanceId,
            .Tags[0].Value,
            .SecurityGroups[0].GroupName,
            .SecurityGroups[0].GroupId] | @csv" \
        | csvtomd
    """
    instance_set = instance.get_instances()
    click.echo(J(instance_set))


@ec2_instance.command()
@click.argument("instance_id")
@click.pass_context
def create_ami(ctx, instance_id):
    """ec2: create AMI for instance_id """
    obj = instance.Instance.factory(instance_id)
    obj.create_image()
