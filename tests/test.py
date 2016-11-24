# import sys
import os
import unittest
from fbbotw import fbbotw


class FbbotwTest(unittest.TestCase):

    def setUp(self):
        self.fbid = os.getenv('FBID', '')

    def test_post_settings(self):
        response = fbbotw.post_settings("Hello world")
        self.assertTrue(response.status_code == 200)

    def test_post_greeting_text(self):
        response = fbbotw.post_greeting_text("Hello World")
        self.assertTrue(response.status_code == 200)

    def test_post_post_start_button(self):
        response = fbbotw.post_start_button('GET_STATED')
        self.assertTrue(response.status_code == 200)

    def test_typing(self):
        # Test typing_on option
        response = fbbotw.typing(fbid=self.fbid, sender_action="typing_on")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)
        # Test typing_off option
        response = fbbotw.typing(fbid=self.fbid, sender_action="typing_off")
        self.assertTrue(response.json()['recipient_id'] == self.fbid)
        self.assertTrue(response.status_code == 200)
        # Test mark_seen option
        response = fbbotw.typing(fbid=self.fbid, sender_action="mark_seen")
        self.assertTrue(response.json()['recipient_id'] == self.fbid)
        self.assertTrue(response.status_code == 200)


if __name__ == '__main__':
    unittest.main()
