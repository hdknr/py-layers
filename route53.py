#!/usr/bin/env python
import click
import sys
import os
import json

BASE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.dirname(BASE)
ROOT = os.path.dirname(BIN)
LAYERS = os.path.join(BASE, 'layers/python')

sys.path.append(LAYERS)

from shares import dns


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def route53(ctx, profile_name):

    if profile_name:
        ctx.obj['aws'] = dns.Route53(profile_name=profile_name)


@route53.command()
@click.pass_context
def zones(ctx):
    res = ctx.obj['aws'].zones
    click.echo(json.dumps(res, indent=2))

@route53.command()
@click.argument('domain')
@click.pass_context
def records(ctx, domain):
    res = ctx.obj['aws'].list_records(domain)
    click.echo(json.dumps(res, indent=2))

if __name__ == '__main__':
    route53(obj={})
