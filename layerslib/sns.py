import boto3


def client():
    return boto3.client("sns")


def all_topics():
    return client().list_topics()


def find_topic(topic_name):
    res = all_topics()
    for t in res["Topics"]:
        arn = t.get("TopicArn", "")
        if arn.find(topic_name) >= 0:
            return t


def publish(topic_arn, message, subject=None):
    body = {"Message": message}
    if subject:
        body["Subject"] = subject

    return client().publish(TopicArn=topic_arn, **body)


def publish_by_name(topic_name, message, subject=None):
    topic = find_topic(topic_name)
    return topic and publish(topic["TopicArn"], message, subject=subject)


def get_sns_message_from_event(event):
    prefix = "Records"
    node = "Sns"
    if prefix in event and len(event[prefix]) > 0:
        if node in event[prefix][0]:
            return event[prefix][0][node]
