import unittest
import message
from mock import patch, Mock

MESSAGES = [
    {'msg': 'A likes your photo', 'timestamp': '2016-11-27T16:13:30'},
    {'msg': 'H did a bike tour', 'timestamp': '2016-11-27T16:12:30'},
    {'msg': 'I likes your photo', 'timestamp': '2016-11-27T16:08:30'},
    {'msg': 'B likes your photo', 'timestamp': '2016-11-27T16:07:31'}
]


class TestMessageSender(unittest.TestCase):

    @patch('boto.ses.connect_to_region')
    def test_should_send_messages(self, ses):
        sender = message.MessageSender('key', 'secret', 'region', 'sender', False)
        sender.send({'name': 'Mat', 'email': 'email'}, MESSAGES)
        ses.assert_called_with('region', aws_access_key_id='key', aws_secret_access_key='secret')
        ses.return_value.send_email.assert_called_with('sender', 'Hi Mat, your friends are active!', 'Hi Mat, your friends are active!\n\nSunday,\t\t16:07\t\t\tB likes your photo\nSunday,\t\t16:08\t\t\tI likes your photo\nSunday,\t\t16:12\t\t\tH did a bike tour\nSunday,\t\t16:13\t\t\tA likes your photo', ['email'])

    @patch('boto.ses.connect_to_region')
    def test_should_send_messages_in_dry_mode(self, ses):
        sender = message.MessageSender('key', 'secret', 'region', 'sender', True)
        sender.send({'name': 'Mat', 'email': 'email'}, MESSAGES)
        ses.assert_called_with('region', aws_access_key_id='key', aws_secret_access_key='secret')
        ses.return_value.send_email.assert_called_with('sender', 'Hi Mat, your friends are active!', 'Hi Mat, your friends are active!\n\nSunday,\t\t16:07\t\t\tB likes your photo\nSunday,\t\t16:08\t\t\tI likes your photo\nSunday,\t\t16:12\t\t\tH did a bike tour\nSunday,\t\t16:13\t\t\tA likes your photo', ['sender'])


class TestFeedConstruction(unittest.TestCase):
    def test_should_return_empty_string_when_messages_empty(self):
        body = message.messages_to_string([])
        self.assertEquals(body, '')

    def test_should_return_message_body_in_time_order(self):
        body = message.messages_to_string(MESSAGES)
        self.assertEqual(body, 'Sunday,\t\t16:07\t\t\tB likes your photo\nSunday,\t\t16:08\t\t\tI likes your photo\nSunday,\t\t16:12\t\t\tH did a bike tour\nSunday,\t\t16:13\t\t\tA likes your photo')