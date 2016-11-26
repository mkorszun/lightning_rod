## Lightning Rod

Allows to unload social activity storm by collecting notifications from queue,
building user notifications digest and sending it in hourly rate.

TL;DR
* There is SQS queue subscribed to notifications topic
* There is periodic task which reads messages from AWS SQS queue and stores them in MongoDB
* There is periodic task which every hour aggregates messages by name/email and sends message digest using AWS SES
* MongoDB is also used as a message broker for celery task queue worker

### Requirements

* [Python 2.7] (https://www.python.org/download/releases/2.7/)
* [Virtualenv] (https://virtualenv.pypa.io/en/stable/)
* [MongoDB] (https://docs.mongodb.com/manual/)
* [Docker] (https://www.docker.com/)

### Installation

#### Virtualenv

Create new virtualenv and install dependencies:
~~~bash
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
~~~

Ensure AWS IAM credentials:
~~~bash
$ export AWS_ACCESS_KEY_ID=""
$ export AWS_SECRET_ACCESS_KEY=""
~~~

Start application:
~~~bash
$ celery -A application worker -B -l info
~~~

#### Docker

Build image:
~~~bash
$ docker build -t lightning-rod .
~~~

Start container:
~~~bash
$ docker run -e "AWS_ACCESS_KEY_ID=" -e "AWS_SECRET_ACCESS_KEY=" -e "C_FORCE_ROOT=true" -d lightning-rod
~~~