__version__ = '0.0.1'
import click
import sys
from .logs import logs
from .ec2 import ec2
from .mails import mails
from .utils import setup
from .builder import builder


COMMANDS = {
    'ec2': ec2, 'mails': mails, 'logs': logs,
    'builder': builder,
}


def dispatch():
    if len(sys.argv) >= 2:
        command = COMMANDS.get(sys.argv[1], None)
        if command:
            del sys.argv[1]
            command(obj={})

    click.echo("specify commad group:\n")
    click.echo(",".join(COMMANDS.keys()))
