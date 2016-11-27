import json
from boto import sqs, ses
from pymongo import MongoClient
from datetime import datetime


class MessageReader():
    """AWS SQS client"""

    def __init__(self, access_key, secret_key, region, queue_name):
        conn = sqs.connect_to_region(region,
                                     aws_access_key_id=access_key,
                                     aws_secret_access_key=secret_key)
        self.queue = conn.get_queue(queue_name)

    def get(self):
        """Get messages from SQS queue"""
        return self.queue.get_messages(visibility_timeout=60, num_messages=10)

    def remove(self, messages):
        """Remove messages from SQS queue"""
        self.queue.delete_message_batch(messages)

    @staticmethod
    def to_messages(raw):
        return [json.loads(json.loads(m.get_body())['Message']) for m in raw]


class MessageStorage():
    """MongoDB client"""

    PIPELINE = [
        {
            "$group": {
                "_id": {
                    "name": "$name",
                    "email": "$email"
                },
                "messages": {
                    "$addToSet": {
                        "msg": "$message",
                        "timestamp": "$timestamp"
                    }
                },
                "ids": {
                    "$addToSet": "$_id"
                }
            }
        }
    ]

    def __init__(self, url, collection_name):
        db = MongoClient(host=url, connect=False).get_default_database()
        self.collection = db.get_collection(collection_name)

    def store(self, messages):
        """Store given message"""
        self.collection.insert_many(messages)

    def group(self):
        """Group messages by name & email"""
        return list(self.collection.aggregate(self.PIPELINE))

    def remove(self, ids):
        """Remove messages with given ids"""
        self.collection.delete_many({"_id": {"$in": ids}})


class MessageSender():
    """AWS SES client"""

    def __init__(self, access_key, secret_key, region, sender, dry_run):
        self.sender = sender
        self.dry_run = dry_run
        self.conn = ses.connect_to_region(region,
                                          aws_access_key_id=access_key,
                                          aws_secret_access_key=secret_key)

    def send(self, receiver, messages):
        """Send notifications digest to user"""
        title = 'Hi {}, your friends are active!'.format(receiver['name'])
        body = '{0}\n\n{1}'.format(title, messages_to_string(messages))
        receiver = self.sender if self.dry_run else receiver['email']
        self.conn.send_email(self.sender, title, body, [receiver])


def messages_to_string(messages):
    """All user messages to string"""
    with_datetime = [extend_with_datetime(m) for m in messages]
    sorted_by_datetime = sorted(with_datetime, key=lambda x: x['datetime'])
    return '\n'.join([message_to_string(m) for m in sorted_by_datetime])


def string_to_datetime(string):
    """Get datetime from given timestamp string"""
    return datetime.strptime(string, '%Y-%m-%dT%H:%M:%S')


def extend_with_datetime(msg):
    """Extend message object with datetime"""
    msg['datetime'] = string_to_datetime(msg['timestamp'])
    return msg


def message_to_string(msg):
    """Single message to string"""
    return '{0},\t\t{1}:{2}\t\t\t{3}'.format(msg['datetime'].strftime("%A"),
                                             msg['datetime'].strftime("%H"),
                                             msg['datetime'].strftime("%M"),
                                             msg['msg'])