import os
from datetime import timedelta
from celery import Celery
import boto.sqs
import json
from pymongo import MongoClient

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

conn = boto.sqs.connect_to_region("eu-west-1",
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

QUEUE = conn.get_queue('komot3')

db = MongoClient(connect=False).get_database('komot')
collection = db.get_collection('messages')
from aggregator import Aggregator
aggregator = Aggregator(collection)

app = Celery('notifications')
app.conf.update(
    BROKER_URL='redis://localhost',
    CELERY_TASK_SERIALIZER='pickle',
    CELERY_ACCEPT_CONTENT=['pickle'],
    CELERYBEAT_SCHEDULE={
        'notifications.store': {
            'task': 'notifications.store',
            'schedule': timedelta(seconds=10)
        },
        'notifications.aggregate': {
            'task': 'notifications.aggregate',
            'schedule': timedelta(seconds=10)
        }
    }
)


@app.task(name='notifications.store')
def store():
    raw_messages = QUEUE.get_messages(visibility_timeout=60, num_messages=10)
    messages = [json.loads(json.loads(m.get_body())['Message']) for m in
                raw_messages]

    if len(raw_messages) > 0:
        collection.insert_many(messages)
        QUEUE.delete_message_batch(raw_messages)


@app.task(name='notifications.aggregate')
def aggregate():
    for r in aggregator.collect():
        send.delay(r['_id'], r['messages'], r['to_delete'])


@app.task
def send(receiver, messages, ids):
    print 'To : {0}'.format(receiver)
    print 'What : {0}'.format(messages)
    print 'Ids: {0}'.format(ids)
    collection.delete_many({"_id": {"$in": ids}})

