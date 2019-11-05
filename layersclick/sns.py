#!/usr/bin/env python
import click
import boto3
from .utils import setup, J
from layerslib.sns import publish_by_name


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def sns(ctx, profile_name):
    setup(ctx, profile_name)


@sns.command()
@click.pass_context
def list_topics(ctx):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Client.list_topics
    res = all_topics()
    click.echo(J(res))


@sns.command()
@click.argument('topic')
@click.argument('message')
@click.option('--subject', '-s', default=None)
@click.pass_context
def publish(ctx, topic, message, subject):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Client.publish
    res = publish_by_name(topic, message, subject=subject)
    click.echo(J(res))
