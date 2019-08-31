import click
import json
import boto3
from .utils import setup


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def mails(ctx, profile_name):
    setup(ctx, profile_name)


@mails.command()
@click.argument('bucket')
@click.argument('message_id')
@click.option('--prefix', '-p', default='')
@click.option('--settings', '-s', default='')
@click.pass_context
def forward_mail(ctx, bucket, message_id, prefix, settings):
    '''mails: Forward email message stored in S3'''
    from layerslib.mails import (
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


@mails.command()
@click.argument('address')
@click.argument('region')
@click.pass_context
def verify_email_address(ctx, address, region):
    '''mails: Verify Email Address'''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/ses-verify.html
    ses = ctx.obj['session'].client('ses', region_name=region)
    res = ses.verify_email_identity(EmailAddress=address)
    click.echo(res)