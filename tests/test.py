# import sys
import os
import unittest
from fbbotw import fbbotw


class FbbotwTest(unittest.TestCase):

    def setUp(self):
        self.fbid = os.getenv('FBID', '')

    #############################################
    #        Tread Settings Functions           #
    #############################################

    def test_post_settings(self):
        response = fbbotw.post_settings("Hello world")
        self.assertTrue(response.status_code == 200)

    def test_post_greeting_text(self):
        response = fbbotw.post_greeting_text("Hello World")
        self.assertTrue(response.status_code == 200)

    def test_post_post_start_button(self):
        response = fbbotw.post_start_button('GET_STATED')
        self.assertTrue(response.status_code == 200)

    def test_post_persistent_menu(self):
        call_to_actions = [
            {
                'type': 'postback',
                'title': 'About',
                'payload': 'ABOUT'
            },
            {
                'type': 'postback',
                'title': 'Help',
                'payload': 'HELP'
            },
        ]
        response = fbbotw.post_persistent_menu(call_to_actions)
        self.assertTrue(response.status_code == 200)

    #############################################
    #        Tread Settings Functions           #
    #############################################

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

    def test_get_user_info(self):
        response = fbbotw.get_user_information(fbid=self.fbid)
        self.assertTrue(response['first_name'] == 'Rto')
        self.assertTrue(response['last_name'] == 'Dto')
        self.assertTrue(response['gender'] == 'male')

    def test_post_text_message(self):
        response = fbbotw.post_text_message(fbid=self.fbid, message="Hello")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)

    def test_post_audio_attachment(self):
        ogg = 'https://dl.dropboxusercontent.com/u/85402777/turdus.ogg'
        response = fbbotw.post_audio_attachment(fbid=self.fbid, audio_url=ogg)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)

    def test_post_file_attachment(self):
        pdf = 'https://dl.dropboxusercontent.com/u/85402777/fbbotw.pdf'
        response = fbbotw.post_file_attachment(fbid=self.fbid, file_url=pdf)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)

    def test_post_image_attachment(self):
        jpg = 'https://i.ytimg.com/vi/tntOCGkgt98/maxresdefault.jpg'
        response = fbbotw.post_image_attachment(fbid=self.fbid, img_url=jpg)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)

    def test_post_video_attachment(self):
        mp4 = 'https://dl.dropboxusercontent.com/u/85402777/fbbotw_drop.mp4'
        response = fbbotw.post_video_attachment(fbid=self.fbid, video_url=mp4)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)

    def test_post_text_w_quickreplies(self):
        quick_replies = [
            {
                "content_type": "text",
                "title": "Yes!",
                "payload": "USER_SAY_YES"
            },
            {
                "content_type": "text",
                "title": "Nope",
                "payload": "USER_SAY_NOT"
            }
        ]
        response = fbbotw.post_text_w_quickreplies(fbid=self.fbid,
                                                   message="Test",
                                                   quick_replies=quick_replies)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)


if __name__ == '__main__':
    unittest.main()
