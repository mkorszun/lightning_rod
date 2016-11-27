## Lightning Rod

Allows to unload social activity storm by collecting notifications from queue,
building user notifications digest and sending it in hourly rate.

TL;DR
* There is SQS queue subscribed to SNS subscription
* There is periodic task which reads messages from AWS SQS queue and stores them in MongoDB
* There is periodic task which every hour aggregates messages by name/email and sends message digest using AWS SES
* MongoDB is also used as a message broker for celery task queue worker

### Requirements

* [Python 2.7] (https://www.python.org/download/releases/2.7/)
* [Virtualenv] (https://virtualenv.pypa.io/en/stable/)
* [MongoDB] (https://docs.mongodb.com/manual/)
* [Docker] (https://www.docker.com/)

### Testing

#### Install test dependencies:
~~~bash
$ pip install -r requirements_test.txt
~~~

#### Run tests:
~~~bash
$ nosetests -v
~~~

### Installation

#### Configuration

##### MongoDB
If want to use different then default MongoDB specify this env variables as well
`MONGO_DB_URL` and `BROKER_URL` - both should contain MongoDB connection string:

`mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]`

##### Test mode
If want to send emails to sender - just for verification, set env variable:
~~~
$ export DRY_RUN=true
~~~

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

Optionally set: `MONGO_DB_URL`, `BROKER_URL`, `DRY_RUN` and `SENDER`