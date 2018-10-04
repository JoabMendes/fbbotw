#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
        self.quick_replies = [
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
        self.OK = 200

    #############################################
    #           User Profile API                #
    #############################################

    def test_get_user_info(self):
        response = fbbotw.get_user_information(fbid=self.fbid)
        # print(json.dumps(response, indent=4, sort_keys=True))
        self.assertTrue(isinstance(response['name'], str))
        self.assertTrue(len(response['name']) > 0)
        self.assertTrue(isinstance(response['first_name'], str))
        self.assertTrue(len(response['first_name']) > 0)
        self.assertTrue(isinstance(response['last_name'], str))
        self.assertTrue(len(response['last_name']) > 0)
        self.assertTrue(isinstance(response['profile_pic'], str))
        self.assertTrue(len(response['profile_pic']) > 0)

    #############################################
    #          Messenger Profile API            #
    #############################################

    def test_post_settings(self):
        greeting, button = fbbotw.post_settings("Hello world")
        self.assertEqual(greeting.status_code, self.OK)
        self.assertDictEqual(
            greeting.json(),
            {'result': 'Successfully updated greeting'}
        )
        self.assertEqual(button.status_code, self.OK)
        self.assertDictEqual(
            button.json(),
            {'result': 'success'}
        )

    def test_post_greeting_text(self):
        greeting_texts = [
            {
                "locale": "default",
                "text": "Hello!"
            },
            {
                "locale": "pt_BR",
                "text": "Texto de Greeting em Português"
            },
            {
                "locale": "en_US",
                "text": "Greeting text in English USA"
            }
        ]
        response = fbbotw.post_greeting_text(
            greeting_texts=greeting_texts
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertDictEqual(
            response.json(),
            {"result": "success"}
        )

    def test_post_start_button(self):
        response = fbbotw.post_start_button('GET_STARTED')
        self.assertEqual(response.status_code, self.OK)
        self.assertDictEqual(
            response.json(),
            {'result': 'success'}
        )

    def test_post_persistent_menu(self):
        persistent_menu = [
            {
                "composer_input_disabled": False,
                "locale": "default",
                "call_to_actions": [
                        {
                            "type": "nested",
                            "title": "First Option",
                            "call_to_actions": [
                                {
                                    "type": "postback",
                                    "title": "First Option of First Option",
                                    "payload": "YOUR_PAYLOAD"
                                },
                                {
                                    "type": "nested",
                                    "title": "Second Option of First Option",
                                    "call_to_actions": [
                                        {
                                            "type": "postback",
                                            "title": "ABC",
                                            "payload": "YOUR_PAYLOAD2"
                                        },
                                        {
                                            "type": "postback",
                                            "title": "CDE",
                                            "payload": "YOUR_PAYLOAD3"
                                        }
                                    ]
                                },
                            ]
                        },
                        {
                            "type": "postback",
                            "title": "Second Option",
                            "payload": "YOUR_PAYLOAD4"
                        },
                    ]
            }
        ]
        response = fbbotw.post_persistent_menu(persistent_menu)
        self.assertEqual(response.status_code, self.OK)
        self.assertDictEqual(
            response.json(),
            {'result': 'success'}
        )

    def test_post_domain_whitelist(self):
        domain = ['https://breco.herokuapp.com']
        response = fbbotw.post_domain_whitelist(whitelisted_domains=domain)
        self.assertEqual(response.status_code, self.OK)
        self.assertDictEqual(
            response.json(),
            {'result': 'success'}
        )

    def test_delete_domain_whitelist(self):
        response = fbbotw.delete_domain_whitelist()
        self.assertEqual(response.status_code, self.OK)
        self.assertDictEqual(
            response.json(),
            {'result': 'success'}
        )

    def test_post_account_linking_url(self):
        url = 'https://breco.herokuapp.com'
        response = fbbotw.post_account_linking_url(account_linking_url=url)
        self.assertEqual(response.status_code, self.OK)
        self.assertDictEqual(
            response.json(),
            {'result': 'success'}
        )

    def test_post_payment_settings(self):
        privacy_url = "https://breco.herokuapp.com/politica-e-termos"
        response = fbbotw.post_payment_settings(privacy_url=privacy_url)
        self.assertEqual(response.status_code, self.OK)
        self.assertDictEqual(
            response.json(),
            {'result': 'success'}
        )
        response = fbbotw.post_payment_settings()
        self.assertDictEqual(
            response,
            {"Error": "At least one parameter should be set"}
        )

    def test_post_target_audience(self):
        countries = {"whitelist": ["US", "BR"]}
        response = fbbotw.post_target_audience(
            countries, audience_type="custom"
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertDictEqual(
            response.json(),
            {'result': 'success'}
        )

    '''
    def test_post_chat_extension_home_url(self):
        self.assertEqual(response.status_code, self.OK)
        self.assertDictEqual(
            response.json(),
            {'result': 'success'}
        )
    '''

    #############################################
    #           Send Api Functions              #
    #############################################

    # Send API Sender Actions

    def test_post_sender_action(self):
        # Test typing_on option
        response = fbbotw.post_sender_action(
            fbid=self.fbid, sender_action="typing_on"
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        # Test typing_off option
        response = fbbotw.post_sender_action(
            fbid=self.fbid, sender_action="typing_off"
        )
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        self.assertEqual(response.status_code, self.OK)
        # Test mark_seen option
        response = fbbotw.post_sender_action(
            fbid=self.fbid, sender_action="mark_seen"
        )
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        self.assertEqual(response.status_code, self.OK)

    # Send API Content Type

    def test_post_text_message(self):
        response = fbbotw.post_text_message(fbid=self.fbid, message="Hello")
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)

    def test_post_text_list(self):
        messages = ["Hello", "World", "FBBOTW"]
        responses = fbbotw.post_text_list(fbid=self.fbid, messages=messages)
        for response in responses:
            self.assertEqual(response.status_code, self.OK)
            self.assertEqual(response.json()['recipient_id'], self.fbid)

    def test_post_audio_attachment(self):
        ogg = ("https://raw.githubusercontent.com/JoabMendes/"
               "fbbotw/master/media/turdus.ogg")
        response = fbbotw.post_audio_attachment(fbid=self.fbid, audio_url=ogg)
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        response = fbbotw.post_audio_attachment(
            fbid=self.fbid,
            audio_url=ogg,
            is_reusable=True
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        self.assertTrue('attachment_id' in response.json())

    def test_post_file_attachment(self):
        pdf = ("https://raw.githubusercontent.com/JoabMendes/"
               "fbbotw/master/media/fbbotw.pdf")
        response = fbbotw.post_file_attachment(fbid=self.fbid, file_url=pdf)
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        response = fbbotw.post_file_attachment(
            fbid=self.fbid,
            file_url=pdf,
            is_reusable=True
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        self.assertTrue('attachment_id' in response.json())

    def test_post_image_attachment(self):
        jpg = 'https://i.imgur.com/HF9STBD.jpg'
        response = fbbotw.post_image_attachment(fbid=self.fbid, img_url=jpg)
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        response = fbbotw.post_image_attachment(
            fbid=self.fbid,
            img_url=jpg,
            is_reusable=True
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        self.assertTrue('attachment_id' in response.json())

    def test_post_video_attachment(self):
        mp4 = ("https://raw.githubusercontent.com/JoabMendes/"
               "fbbotw/master/media/fbbotw_drop.mp4")
        response = fbbotw.post_video_attachment(fbid=self.fbid, video_url=mp4)
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        response = fbbotw.post_video_attachment(
            fbid=self.fbid,
            video_url=mp4,
            is_reusable=True
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)
        self.assertTrue('attachment_id' in response.json())

    def test_upload_reusable_attachment(self):
        jpg = 'https://i.imgur.com/HF9STBD.jpg'
        response = fbbotw.upload_reusable_attachment(
            media_url=jpg, file_type='image'
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertTrue('attachment_id' in response.json())

    def test_post_reusable_attachment(self):
        jpg = 'https://i.imgur.com/HF9STBD.jpg'
        upload = fbbotw.upload_reusable_attachment(
            media_url=jpg, file_type='image'
        )
        attachment_id = upload.json()['attachment_id']
        response = fbbotw.post_reusable_attachment(
            fbid=self.fbid,
            attachment_id=attachment_id,
            file_type='image'
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)

    # Send API Quick Replies

    def test_post_text_w_quickreplies(self):
        response = fbbotw.post_text_w_quickreplies(
            fbid=self.fbid,
            message='Test?',
            quick_replies=self.quick_replies
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)

    def test_post_image_w_quickreplies(self):
        image_url = 'https://i.imgur.com/HF9STBD.jpg'
        response = fbbotw.post_image_w_quickreplies(
            fbid=self.fbid,
            image_url=image_url,
            quick_replies=self.quick_replies
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)

    def test_post_template_w_quickreplies(self):
        payload = {
            "template_type": "button",
            "text": "What do you want to do next?",
            "buttons": self.postback_buttons
        }
        response = fbbotw.post_template_w_quickreplies(
            fbid=self.fbid,
            payload=payload,
            quick_replies=self.quick_replies
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)

    def test_post_button_template(self):
        response = fbbotw.post_button_template(
            fbid=self.fbid,
            text="Test?",
            buttons=self.postback_buttons,
            sharable=False
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)

    def test_post_generic_template(self):
        title = 'This is a Generic Template'
        image_url = 'https://i.imgur.com/HF9STBD.jpg'
        subtitle = 'Generic Template Subtitle'
        default_action = {
            'type': 'web_url',
            'url': 'https://breco.herokuapp.com/',
            'messenger_extensions': True,
            'webview_height_ratio': 'tall',
            'fallback_url': 'https://breco.herokuapp.com/'
        }
        response = fbbotw.post_generic_template(
            fbid=self.fbid,
            title=title,
            image_url=image_url,
            subtitle=subtitle,
            buttons=self.postback_buttons,
            default_action=default_action,
            sharable=False,
            image_aspect_ratio='square'
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)

    def test_post_generic_template_carousel(self):
        element = {
            "title": "This is a Generic Template",
            "item_url": "http://breco.herokuapp.com/",
            "image_url": "https://i.imgur.com/HF9STBD.jpg",
            "subtitle": "Generic Template Subtitle",
            "buttons": [
                {
                    'type': 'web_url',
                    'url': 'http://breco.herokuapp.com/',
                    'title': 'My homepage'
                }
            ]
        }
        elements = []
        for i in range(1, 4):
            elements.append(element)
        response = fbbotw.post_generic_template_carousel(
            fbid=self.fbid,
            elements=elements,
            image_aspect_ratio='square'
        )
        self.assertEqual(response.status_code, self.OK)
        self.assertEqual(response.json()['recipient_id'], self.fbid)

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
        el['title'] = "Another Shirt"
        elements.append(el)
        buttons = [
            {
                'title': 'View More',
                'type': 'postback',
                'payload': 'VIEW_MORE'
            }
        ]
        response = fbbotw.post_list_template(
            fbid=self.fbid,
            elements=elements,
            buttons=buttons,
            sharable=True
        )
        self.assertEqual(response.status_code, self.OK)

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

        response = fbbotw.post_receipt_template(
            fbid=self.fbid,
            recipient_name=name,
            order_number=order_number,
            currency=currency,
            payment_method=payment_method,
            summary=summary,
            timestamp=timestamp,
            order_url=order_url,
            elements=elements,
            address=address,
            adjustments=adjustments,
            sharable=False
        )
        self.assertEqual(response.status_code, self.OK)

    def test_post_media_template(self):
        elements = [
            {
                "media_type": "image",
                "url": (
                    "https://www.facebook.com/"
                    "facebookcanada/photos/1442911455747101/"
                ),
                "buttons": [
                    {
                        "type": "web_url",
                        "url": (
                            "https://www.facebook.com/"
                            "facebookcanada/photos/1442911455747101/"
                        ),
                        "title": "View Post",
                    }
                ]
            }
        ]
        response = fbbotw.post_media_template(
            fbid=self.fbid,
            elements=elements,
        )
        self.assertEqual(response.status_code, self.OK)

    # Send API Buttons

    def test_post_call_button(self):
        text = "Do you wanna call Joabe?"
        title = "Call Now"
        phone = "+558499872770"
        response = fbbotw.post_call_button(fbid=self.fbid, text=text,
                                           title=title, phone_number=phone)
        self.assertEqual(response.status_code, self.OK)


if __name__ == '__main__':
    unittest.main()
