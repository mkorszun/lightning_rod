from datetime import timedelta
from celery import Celery
from message import MessageReader, MessageStorage, MessageSender

from config import MONGO_DB_URL, MONGO_DB_COLLECTION, AWS_SQS_NAME, AWS_REGION, \
    AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID, BROKER_URL, SENDER


storage = MessageStorage(MONGO_DB_URL, MONGO_DB_COLLECTION)

reader = MessageReader(AWS_ACCESS_KEY_ID,
                       AWS_SECRET_ACCESS_KEY,
                       AWS_REGION,
                       AWS_SQS_NAME)

sender = MessageSender(AWS_ACCESS_KEY_ID,
                       AWS_SECRET_ACCESS_KEY,
                       AWS_REGION,
                       SENDER)

app = Celery('notifications')
app.conf.update(
    BROKER_URL=BROKER_URL,
    CELERY_TASK_SERIALIZER='pickle',
    CELERY_ACCEPT_CONTENT=['pickle'],
    CELERYBEAT_SCHEDULE={
        'notifications.store': {
            'task': 'notifications.store',
            'schedule': timedelta(seconds=10)
        },
        'notifications.aggregate': {
            'task': 'notifications.aggregate',
            'schedule': timedelta(minutes=30)
        }
    }
)


@app.task(name='notifications.store')
def store():
    raw_messages = reader.get()

    if len(raw_messages) > 0:
        messages = MessageReader.to_messages(raw_messages)
        storage.store(messages)
        reader.remove(raw_messages)


@app.task(name='notifications.aggregate')
def aggregate():
    for r in storage.group():
        send.delay(r['_id'], r['messages'], r['ids'])


@app.task(name='notifications.send')
def send(receiver, messages, ids):
    print 'To : {0}'.format(receiver)
    print 'What : {0}'.format(messages)
    print 'Ids: {0}'.format(ids)
    sender.send(receiver, messages)
    storage.remove(ids)

