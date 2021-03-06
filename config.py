import os

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'eu-west-1')
AWS_SQS_NAME = os.getenv('AWS_SQS_NAME', 'komot3')

MONGO_DB_URL = os.getenv('MONGO_DB_URL', 'mongodb://komot:komot@ds163677.mlab.com:63677/komot')
MONGO_DB_COLLECTION = os.getenv('MONGO_DB_COLLECTION', 'notifications')

BROKER_URL = os.getenv('BROKER_URL', 'mongodb://komot:komot@ds163677.mlab.com:63677/komot')
SENDER = os.getenv('SENDER', 'mkorszun@gmail.com')
DRY_RUN = os.getenv('DRY_RUN', 'true') == 'true'

FETCH_MESSAGE_FREQUENCY = int(os.getenv('FETCH_MESSAGE_FREQUENCY', 60))
SEND_MESSAGE_FREQUENCY = int(os.getenv('SEND_MESSAGE_FREQUENCY', 60))