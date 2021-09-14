import click

from layerslib.ec2 import image, instance

from .utils import J, setup


@click.group()
@click.option("--profile_name", "-p", default=None)
@click.pass_context
def ec2_image(ctx, profile_name):
    setup(ctx, profile_name)


@ec2_image.command()
@click.pass_context
def image_list(ctx):
    """ec2: get AMI Image
    layers ec2_image -p yourprofile image-list | jq -r ".[] | [list] | @csv"
    list:
        .Name, .ImageId, .Tags[0].Value
    """
    image_set = image.get_images()
    click.echo(J(image_set))


@ec2_image.command()
@click.argument("instance_id")
@click.pass_context
def create_ami(ctx, instance_id):
    """ec2: create AMI for instance_id """
    obj = instance.Instance.factory(instance_id)
    obj.create_image()
