import click
import boto3
import layerslib
from .utils import setup
import os
import zipfile


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def builder(ctx, profile_name):
    setup(ctx, profile_name)


@builder.command()
@click.argument('path')
@click.pass_context
def build(ctx, path):
    '''builder: build aws layers zipfile'''
    base = os.path.dirname(layerslib.__file__)
    ommit = os.path.dirname(base)

    zf = zipfile.ZipFile(path, "w")
    for dirname, subdirs, files in os.walk(base):
        if '__pycache__' in dirname:
            continue

        zf.write(dirname, arcname=dirname.replace(ommit, 'python'))
        for filename in files:
            if filename.endswith('.pyc'):
                continue
            name = os.path.join(dirname, filename)
            zf.write(name, arcname=name.replace(ommit, 'python'))

    zf.close()

