import click
import json
import base64
from .utils import setup, J
from layerslib.lambdas import client


@click.group()
@click.option('--profile_name', '-p', default=None)
@click.pass_context
def lambdas(ctx, profile_name):
    setup(ctx, profile_name)


@lambdas.command()
@click.pass_context
def list_layer(ctx):
    '''List Layers'''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_layers
    res = client().list_layers() 
    click.echo(J(res))


@lambdas.command()
@click.pass_context
def list_function(ctx):
    '''List Functions'''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.list_functions
    res = client().list_functions() 
    click.echo(J(res))


@lambdas.command()
@click.argument('name')
@click.argument('path')
@click.pass_context
def upload_layer(ctx, name, path):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.publish_layer_version
    runtime = 'python3.7'
    with open(path, 'rb') as zf:
        res = client().publish_layer_version(
            LayerName=name,
            Content={'ZipFile': zf.read()},
            CompatibleRuntimes=[runtime],
        )
        click.echo(J(res))


@lambdas.command()
@click.argument('function_name')
@click.pass_context
def invoke(ctx, function_name):
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.invoke
    # https://docs.aws.amazon.com/ja_jp/lambda/latest/dg/API_Invoke.html
    event_dict = {}
    res = client().invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',   # 'Event'|'RequestResponse'|'DryRun'
        LogType='Tail',
        # Payload=json.dumps(event_dict),
    )
    log_result = res['LogResult']
    payload = res['Payload']

    click.echo(base64.b64decode(log_result))
    click.echo(J(json.load(payload)))


@lambdas.command()
@click.argument('function_name')
@click.argument('role')
@click.pass_context
def set_role(ctx, function_name, role):
    '''Set Role(ARN) to Lambda Function '''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.update_function_configuration
    res = client().update_function_configuration(
        FunctionName=function_name,
        Role=role,
    )
    click.echo(J(res))


@lambdas.command()
@click.argument('function_name')
@click.argument('key')
@click.argument('value')
@click.pass_context
def set_env(ctx, function_name, key, value):
    '''Set Environment Variable to Lambda Function'''
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.get_function_configuration
    info = client().get_function_configuration(FunctionName=function_name)
    defaults = {'Variables': {}}
    envs = info.get('Environment', defaults)
    envs['Variables'][key] = value

    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Client.update_function_configuration
    res = client().update_function_configuration(FunctionName=function_name, Environment=envs)
    click.echo(J(res))
