#!/usr/bin/env python
import sys
import click
import json
import os
import boto3

BASE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.dirname(BASE)
ROOT = os.path.dirname(BIN)
LAYERS = os.path.join(BASE, 'layers/python')

sys.path.append(LAYERS)


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def fn(ctx, profile_name):

    if profile_name:
        session = boto3.Session(profile_name=profile_name)
        credentials = session.get_credentials()
        ctx.obj['session'] = session
        ctx.obj['credentials'] = credentials
    
        os.environ['AWS_DEFAULT_REGION'] = session.region_name
        os.environ['AWS_ACCESS_KEY_ID'] = credentials.access_key
        os.environ['AWS_SECRET_ACCESS_KEY'] = credentials.secret_key


@fn.command()
@click.pass_context
def instance(ctx):
    ''' get Instance'''
    from shares import get_instances
    instances = get_instances()
    click.echo(instances)


@fn.command()
@click.pass_context
def debug_info(ctx):
    '''Debug Info '''
    from shares import debug, sanitize
    click.echo(sanitize(debug.info()))


@fn.command()
@click.argument('bucket')
@click.argument('message_id')
@click.option('--prefix', '-p', default='')
@click.option('--settings', '-s', default='')
@click.pass_context
def forward_mail(ctx, bucket, message_id, prefix, settings):
    '''Forward email message stored in S3'''
    from shares.mails import (
        getMessageObjectFromFile, forwardMessage, forwardSes)

    if bucket == 'local':
        obj = getMessageObjectFromFile(message_id)
        settings = json.load(open(settings))
        forwardMessage(obj, settings)
    else:
        if prefix and not prefix.endswith('/'):
            prefix = prefix + '/'
        
        # Fake Event
        receipt = dict(recipients=[])
        mail = dict(messageId=message_id)
        ses = dict(receipt=receipt, mail=mail)
        record = dict(ses=ses)
        event = dict(Records=[record])

        forwardSes(event, ctx, bucket, prefix)


@fn.command()
@click.argument('address')
@click.argument('region')
@click.pass_context
def verify_email_address(ctx, address, region):
    '''Verify Email Address'''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ses-verify.html
    ses = ctx.obj['session'].client('ses', region_name=region)
    res = ses.verify_email_identity(EmailAddress=address)
    click.echo(res)


if __name__ == '__main__':
    fn(obj={})
