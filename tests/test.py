# import sys
import os
import unittest
from fbbotw import fbbotw


class FbbotwTest(unittest.TestCase):

    def setUp(self):
        self.fbid = os.getenv('FBID', '')
        self.postback_buttons = [
            {
                'type': 'postback',
                'title': 'Yes!',
                'payload': 'USER_SAY_YES'
            },
            {
                'type': 'postback',
                'title': 'Nope',
                'payload': 'USER_SAY_NOT'
            }
        ]

    #############################################
    #           Graph API Functions             #
    #############################################

    def test_get_user_info(self):
        response = fbbotw.get_user_information(fbid=self.fbid)
        self.assertTrue(response['first_name'] == 'Rto')
        self.assertTrue(response['last_name'] == 'Dto')
        self.assertTrue(response['gender'] == 'male')

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
        response = fbbotw.post_persistent_menu(self.postback_buttons)
        self.assertTrue(response.status_code == 200)

    def test_post_domain_whitelisting(self):
        domain = ['https://breco.herokuapp.com']
        response = fbbotw.post_domain_whitelisting(whitelisted_domains=domain)
        self.assertTrue(response.status_code == 200)

    # def test_post_account_linking_url(self):
    #    url = ''
    #    response = fbbotw.post_account_linking_url(account_linking_url=url)
    #    self.assertTrue(response.status_code == 200)

    #############################################
    #        Tread Settings Functions           #
    #############################################

    # Send API Sender Actions

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

    # Send API Content Type

    def test_post_text_message(self):
        response = fbbotw.post_text_message(fbid=self.fbid, message="Hello")
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)

    def test_post_text_list(self):
        messages = ["Hello", "World", "FBBOTW"]
        responses = fbbotw.post_text_list(fbid=self.fbid, messages=messages)
        for response in responses:
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

    # Send API Quick Replies

    def test_post_text_w_quickreplies(self):
        quick_replies = [
            {
                'content_type': 'text',
                'title': 'Yes!',
                'payload': 'USER_SAY_YES'
            },
            {
                'content_type': 'text',
                'title': 'Nope',
                'payload': 'USER_SAY_NOT'
            }
        ]
        response = fbbotw.post_text_w_quickreplies(fbid=self.fbid,
                                                   message='Test?',
                                                   quick_replies=quick_replies)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)

    def test_post_button_template(self):
        response = fbbotw.post_button_template(fbid=self.fbid, text="Test?",
                                               buttons=self.postback_buttons)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)

    def test_post_generic_template(self):
        title = 'This is a Generic Template'
        item_url = 'http://breco.herokuapp.com/'
        image_url = 'https://i.ytimg.com/vi/tntOCGkgt98/maxresdefault.jpg'
        subtitle = 'Generic Template Subtitle'
        response = fbbotw.post_generic_template(fbid=self.fbid,
                                                title=title,
                                                item_url=item_url,
                                                image_url=image_url,
                                                subtitle=subtitle,
                                                buttons=self.postback_buttons)
        self.assertTrue(response.status_code == 200)
        self.assertTrue(response.json()['recipient_id'] == self.fbid)

    def test_post_list_template(self):
        elements = []
        el = {
            'title': 'Classic White T-Shirt',
            'image_url': 'http://i.imgur.com/GHC4ZHl.jpg',
            'subtitle': 'Nice shirt',
            'default_action': {
                'type': 'web_url',
                'url': 'https://breco.herokuapp.com/',
                'messenger_extensions': True,
                'webview_height_ratio': 'tall',
                'fallback_url': 'https://breco.herokuapp.com/'
            },
            'buttons': [{
                'title': 'Buy',
                'type': 'web_url',
                'url': 'https://breco.herokuapp.com/',
                'messenger_extensions': True,
                'webview_height_ratio': 'tall',
                'fallback_url': 'https://breco.herokuapp.com/'
            }]
        }
        elements.append(el)
        el['title'] = "Anothe Shirt"
        elements.append(el)
        buttons = [
            {
                'title': 'View More',
                'type': 'postback',
                'payload': 'VIEW_MORE'
            }
        ]
        response = fbbotw.post_list_template(fbid=self.fbid,
                                             elements=elements,
                                             buttons=buttons)
        self.assertTrue(response.status_code == 200)

    def test_post_receipt_template(self):
        name = "Joab Mendes"
        order_number = "97892"
        currency = "USD"
        payment_method = "VISA 9852"
        summary = {
            "subtotal": 40.00,
            "shipping_cost": 4.95,
            "total_tax": 6.19,
            "total_cost": 61.11
        }
        timestamp = '1480316409'
        order_url = 'https://breco.herokuapp.com'
        elements = [
          {
            "title": "Classic White T-Shirt",
            "subtitle": "100% Soft and Luxurious Cotton",
            "quantity": 2,
            "price": 50,
            "currency": "USD",
            "image_url": "http://i.imgur.com/GHC4ZHl.jpg"
          }
        ]
        address = {
          "street_1": "1 Hacker Way",
          "street_2": "",
          "city": "Menlo Park",
          "postal_code": "94025",
          "state": "CA",
          "country": "US"
        }
        adjustments = [
            {
                "name": "$10 Off Coupon",
                "amount": 10
            }
        ]

        response = fbbotw.post_receipt_template(fbid=self.fbid,
                                                recipient_name=name,
                                                order_number=order_number,
                                                currency=currency,
                                                payment_method=payment_method,
                                                summary=summary,
                                                timestamp=timestamp,
                                                order_url=order_url,
                                                elements=elements,
                                                address=address,
                                                adjustments=adjustments)
        self.assertTrue(response.status_code == 200)

    # Send API Buttons

    def test_post_call_button(self):
        text = "Do you wanna call Joabe?"
        title = "Call Now"
        phone = "+558499872770"
        response = fbbotw.post_call_button(fbid=self.fbid, text=text,
                                           title=title, phone_number=phone)
        self.assertTrue(response.status_code == 200)


if __name__ == '__main__':
    unittest.main()
