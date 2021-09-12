# https://docs.aws.amazon.com/ja_jp/ses/latest/DeveloperGuide/receiving-email-action-lambda.html
import email
import json
import re
from email.utils import getaddresses
from itertools import chain

import boto3
from botocore.exceptions import ClientError

from . import getLogger

S3 = boto3.client("s3")

logger = getLogger()


def getObject(key, s3bucket, s3prefix=""):
    obj = S3.get_object(Bucket=s3bucket, Key=f"{s3prefix}{key}")
    return obj


def getMessage(messageId, s3bucket, s3prefix=""):
    o = getObject(messageId, s3bucket, s3prefix)
    return o["Body"].read()


def getMessageObject(messageId, s3bucket, s3prefix=""):
    return email.message_from_bytes(getMessage(messageId, s3bucket, s3prefix=s3prefix))


def getMessageObjectFromFile(path):
    return email.message_from_file(open(path))


def getSettings(s3bucket, s3prefix=""):
    o = getObject("emails.json", s3bucket, s3prefix)
    return json.loads(o["Body"].read())


def patchHeader(msg, verified_from, prefix=""):
    del msg["DKIM-Signature"]
    del msg["Sender"]
    del msg["Return-Path"]
    del msg["Reply-To"]

    msg["Reply-To"] = msg["From"]
    del msg["From"]
    msg["Return-Path"] = verified_from
    msg["From"] = verified_from

    if prefix and prefix.lower() not in msg.get("Subject").lower():
        new_subj = " ".join([prefix, msg.get("Subject", "")])
        del msg["Subject"]
        msg["Subject"] = new_subj


def getRecipients(record):
    return record["ses"]["receipt"]["recipients"]


def getMessageId(record):
    return record["ses"]["mail"]["messageId"]


def findRecipients(message_obj):
    addrs = getaddresses(
        chain(
            message_obj.get_all("to", []),
            message_obj.get_all("cc", []),
            message_obj.get_all("Received", []),
            message_obj.get_all("bcc", []),
        )
    )
    return list(set(i[1] for i in addrs if re.search(r"^\S+@\S+$", i[1])))


def sendMessage(sender, forwarded, message_text, region_name, original):
    try:
        SES = boto3.client("ses", region_name=region_name)
        SES.send_raw_email(Source=sender, Destinations=[forwarded], RawMessage=dict(Data=message_text))
        logger.info(f"Forwarded email for <{original}> to <{forwarded}>. ")
    except ClientError as e:
        logger.error(f"Client error while forwarding email for <{original}> to <{forwarded}>: {e}")


def forwardMessage(message_obj, settings, recipients=None):
    if not recipients:
        recipients = findRecipients(message_obj)

    patchHeader(message_obj, settings["sender"])
    msg_string = message_obj.as_string()

    for recipient in recipients:
        forwards = settings["forwards"].get(recipient, [])
        for address in forwards:
            sendMessage(settings["sender"], address, msg_string, settings["region_name"], recipient)


def forwardMessageInBucket(messageId, s3bucket, s3prefix, recipients=None):
    recipients = recipients or []
    message_obj = getMessageObject(messageId, s3bucket, s3prefix)
    settings = getSettings(s3bucket, s3prefix)
    forwardMessage(message_obj, settings, recipients)


def forwardSes(event, context, s3bucket, s3prefix):
    record = event["Records"][0]
    messageId = getMessageId(record)
    recipients = getRecipients(record)
    forwardMessageInBucket(messageId, s3bucket, s3prefix, recipients)
