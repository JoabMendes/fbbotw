import json
import requests
import os

IMPORT_ERROR = "Couldn't import PAGE_ACCESS_TOKEN. \
Define this var in your django settings configuration\
or as environment variable."

HEADER = {"Content-Type": "application/json"}


# Not using Django
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN', False)
if not PAGE_ACCESS_TOKEN:
    try:
        from django.conf import settings
        PAGE_ACCESS_TOKEN = settings.PAGE_ACCESS_TOKEN
    except ImportError:
        # Not using django
        raise ImportError(IMPORT_ERROR)
    except AttributeError:
        # Using django but did defined the config var PAGE_ACCESS_TOKEN
        raise ImportError(IMPORT_ERROR)


TD_STS_URL = 'https://graph.facebook.com/v2.6/me/thread_settings?access_token='
MSG_URL = 'https://graph.facebook.com/v2.6/me/messages?access_token='


#############################################
#        Graph API Functions                #
#############################################


def get_user_information(fbid):
    """ Gets user information: first_name, last_name, gender, profile_pic,
    locale, timezone, is_payment_enabled
    (/docs/messenger-platform/user-profile).

    :param str fbid: User id to get the information
    :return: dict with keys : first_name, last_name, gender, profile_pic,\
    locale, timezone, is_payment_enabled.
    """
    user_info_url = "https://graph.facebook.com/v2.7/%s" % fbid
    payload = {}
    payload['fields'] = 'first_name,last_name,gender,profile_pic,\
    locale,timezone,is_payment_enabled'
    payload['access_token'] = PAGE_ACCESS_TOKEN
    user_info = requests.get(user_info_url, payload).json()
    return user_info


#############################################
#        Tread Settings Functions           #
#############################################


def post_settings(greeting_text):
    """ Sets the START Button and also the Greeting Text.
        The payload for the START Button will be 'USER_START'

    :param str greeting_text: Desired Greeting Text (160 chars).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    # Set the greeting texts
    url = TD_STS_URL + PAGE_ACCESS_TOKEN
    txtpayload = {}
    txtpayload['setting_type'] = 'greeting'
    txtpayload['greeting'] = {'text': greeting_text}
    response_msg = json.dumps(txtpayload)
    status = requests.post(url, headers=HEADER, data=response_msg)
    # Set the start button
    btpayload = {}
    btpayload['setting_type'] = 'call_to_actions'
    btpayload['thread_state'] = 'new_thread'
    btpayload['call_to_actions'] = [{'payload': 'USER_START'}]
    response_msg = json.dumps(btpayload)
    status = requests.post(url, headers=HEADER, data=response_msg)
    return status


def post_greeting_text(greeting_text):
    """ Sets the Thread Settings Greeting Text
    (/docs/messenger-platform/thread-settings/greeting-text).

    :param str greeting_text: Desired Greeting Text (160 chars)
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = TD_STS_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload["setting_type"] = "greeting"
    payload["greeting"] = {"text": greeting_text}
    response_msg = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=response_msg)
    return status


def post_start_button(payload='START'):
    """ Sets the Thread Settings Greeting Text
    (/docs/messenger-platform/thread-settings/get-started-button).

    :param str payload: Desired postback payload (Default START).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = TD_STS_URL + PAGE_ACCESS_TOKEN
    btpayload = {}
    btpayload["setting_type"] = "call_to_actions"
    btpayload["thread_state"] = "new_thread"
    btpayload["call_to_actions"] = [{"payload": payload}]
    response_msg = json.dumps(btpayload)
    status = requests.post(url, headers=HEADER, data=response_msg)
    return status


def post_persistent_menu(call_to_actions):
    """ Sets a persistent menu on the chat
    (/docs/messenger-platform/thread-settings/persistent-menu)

    :param list call_to_actions: format :

        >>> call_to_actions =  [
            {
                'type': 'postback',
                'title': 'About',
                'payload': 'ABOUT'
            },
            {
                'type': 'web_url',
                'title': 'Google it',
                'url': 'https://www.google.com',
                'webview_height_ratio': 'full',
                'messenger_extensions': True
            },
        ]
    :return: `Response object <http://docs.python-requests.org/en/\
  master/api/#requests.Response>`_
    """
    url = TD_STS_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload["setting_type"] = "call_to_actions"
    payload["thread_state"] = "existing_thread"
    payload["call_to_actions"] = call_to_actions
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_domain_whitelisting(whitelisted_domains, domain_action_type='add'):
    """ Sets the whistelisted domains for the Messenger Extension
    (/docs/messenger-platform/thread-settings/domain-whitelisting).

    :param list whistelisted_domains: Domains to be whistelisted.
    :param str domain_action_type: Action to run `add/remove` (Defaut add).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = TD_STS_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload['setting_type'] = 'domain_whitelisting'
    payload['whitelisted_domains'] = whitelisted_domains
    payload['domain_action_type'] = domain_action_type
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_account_linking_url(account_linking_url):
    """ Sets the liking url to link the user with your business login
    (/docs/messenger-platform/thread-settings/account-linking).

    :param str account_linking_url: URL to the account linking OAuth flow.
    :return: `Response object <http://docs.python-requests.org/en/\
  master/api/#requests.Response>`_
    """
    url = TD_STS_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload['setting_type'] = 'account_linking'
    payload['account_linking_url'] = account_linking_url
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


#############################################
#           Send Api Functions              #
#############################################

# Send API Sender Actions

def typing(fbid, sender_action):
    """ Displays/Hides the typing gif/mark seen on facebook chat
    (/docs/messenger-platform/send-api-reference/sender-actions)

    :param str fbid: User id to display action.
    :param str sender_action: `typing_off/typing_on/mark_seen`.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload['recipient'] = {'id': fbid}
    payload['sender_action'] = sender_action
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


# Send API Content Type


def post_text_message(fbid, message):
    """ Sends a common text message
    (/docs/messenger-platform/send-api-reference/text-message)

    :param str fbid: User id to send the text.
    :param str message: Text to be displayed for the user (230 chars).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload['recipient'] = {'id': fbid}
    payload['message'] = {'text': message}  # Limit 320 chars
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_text_list(fbid, messages=[]):
    """ Sends a serie of messages from list of text.

    :param str fbid: User id to send the text list.
    :param list messages: A list of messages to be sent.
    :return: A list of `Response objects <http://docs.python-\
    requests.org/en/master/api/#requests.Response>`_\
    for every message sent.
    """
    responses = []
    for msg in messages:
        responses.append(post_text_message(fbid=fbid, message=msg))
    return responses


def post_attachment(fbid, media_url, file_type):
    """ Sends a media attachment
    (/docs/messenger-platform/send-api-reference/contenttypes)

    :param str fbid: User id to send the audio.
    :param str url: Url of a hosted media.
    :param str type: image/audio/video/file.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload['recipient'] = {'id': fbid}
    attachment = {"type": file_type, "payload": {"url": media_url}}
    payload['message'] = {"attachment": attachment}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_audio_attachment(fbid, audio_url):
    """ Sends an audio attachment
    (/docs/messenger-platform/send-api-reference/audio-attachment)

    :param str fbid: User id to send the audio.
    :param str audio_url: Url of a hosted audio (10 Mb).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    return post_attachment(fbid, audio_url, 'audio')


def post_file_attachment(fbid, file_url):
    """ Sends a file attachment
    (/docs/messenger-platform/send-api-reference/file-attachment)

    :param str fbid: User id to send the file.
    :param str file_url: Url of a hosted file (10 Mb).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    return post_attachment(fbid, file_url, 'file')


def post_image_attachment(fbid, img_url):
    """ Sends an image attachment
    (/docs/messenger-platform/send-api-reference/image-attachment)

    :param str fbid: User id to send the image.
    :param str img_url: Url of a hosted image (jpg, png, gif).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    return post_attachment(fbid, img_url, 'image')


def post_video_attachment(fbid, video_url):
    """ Sends a video attachment
    (/docs/messenger-platform/send-api-reference/video-attachment)

    :param str fbid: User id to send the video.
    :param str video_url: Url of a hosted video.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    return post_attachment(fbid, video_url, 'video')


# Send API Quick Replies

def post_text_w_quickreplies(fbid, message, quick_replies):
    """ Send text with quick replies buttons
    (/docs/messenger-platform/send-api-reference/quick-replies).

    :param str fbid: User id to send the quick replies menu.
    :param str message: message to be displayed with the menu.
    :param list quick_replies: (Max 10) format :

        >>> quick_replies = [
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
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload["recipient"] = {"id": fbid}
    payload["message"] = {"text": message, "quick_replies": quick_replies}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


# Send API Templates

def post_button_template(fbid, text, buttons):
    """ Sends a button template with the specified text and buttons
    (/docs/messenger-platform/send-api-reference/button-template).

    :param str fbid: User id to send the buttons.
    :param str text: Message to be displayed with the buttons (320 Chars).
    :param list buttons: Dict of buttons that appear as call-to-actions, \
    format :

        >>> buttons = [
            {
                'type': 'web_url',
                'url': 'https://petersapparel.parseapp.com',
                'title': 'Show Website'
            },
            {
                'type': 'postback',
                'title': 'Start Chatting',
                'payload': 'USER_DEFINED_PAYLOAD'
            }
        ]
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_.
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    data = {}
    data['recipient'] = {'id': fbid}
    payload = {}
    payload['template_type'] = 'button'
    payload['text'] = text
    payload['buttons'] = buttons
    attachment = {"type": 'template', "payload": payload}
    data['message'] = {"attachment": attachment}
    data = json.dumps(data)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_generic_template(fbid, title, item_url='', image_url='', subtitle='',
                          buttons=[]):
    """ Sends a generic template for the specified User
    (/docs/messenger-platform/send-api-reference/generic-template).

    :param str fbid: User id to send the generic template.
    :param str title: Bubble title (80 Chars).
    :param str item_url: URL that is opened when bubble is tapped.
    :param str image_url: Bubble image (Ratio 1.91:1).
    :param str subtitle: Bubble subtitle (80 Chars).
    :param list buttons: (Max 3) format :

        >>> buttons = [
            {
                'type': 'web_url',
                'url': 'https://petersfancybrownhats.com',
                'title': 'View Website'
            },
            {
                'type': 'postback',
                'title': 'Start Chatting',
                'payload': 'DEVELOPER_DEFINED_PAYLOAD'
            }
        ]
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    data = {}
    data['recipient'] = {'id': fbid}
    payload = {}
    payload['template_type'] = 'generic'
    payload['elements'] = []
    element = {}
    element['title'] = title
    element['item_url'] = item_url
    element['image_url'] = image_url
    element['subtitle'] = subtitle
    element['buttons'] = buttons
    payload['elements'].append(element)
    attachment = {"type": 'template', "payload": payload}
    data['message'] = {"attachment": attachment}
    data = json.dumps(data)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_list_template(fbid, elements, buttons=[], top_element_style='large'):
    """ Sends a list template for the specified User
    (/docs/messenger-platform/send-api-reference/list-template).

    :param str fbid: User id to send the list template.
    :param str top_element_style: large/compact (Default Large).
    :param list elements: List view elements (Max 4/Min 2 elements), \
    format :

        >>> elements = [{
            'title': 'Classic Gray T-Shirt',
            'image_url': 'https://app.ngrok.io/img/gray-t-shirt.png',
            'subtitle': '100% Cotton, 200% Comfortable',
            'default_action': {
                'type': 'web_url',
                'url': 'https://app.ngrok.io/view?item=103',
                'messenger_extensions': true,
                'webview_height_ratio': 'tall',
                'fallback_url': 'https://peterssendreceiveapp.ngrok.io/'
            },
            'buttons': [
                {
                    'title': 'Buy',
                    'type': 'web_url',
                    'url': 'https://app.ngrok.io/shop?item=103',
                    'messenger_extensions': true,
                    'webview_height_ratio': 'tall',
                    'fallback_url': 'https://app.ngrok.io/'
                }
            ]
        }]

    :param list buttons: List of buttons associated on the list \
    template message (Max 1). format :

        >>> buttons = [
            {
                'title': 'View More',
                'type': 'postback',
                'payload': 'payload'
            }
        ]
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    data = {}
    data['recipient'] = {'id': fbid}
    payload = {}
    payload['template_type'] = 'list'
    payload['top_element_style'] = top_element_style
    payload['buttons'] = buttons
    payload['elements'] = elements
    attachment = {"type": 'template', "payload": payload}
    data['message'] = {"attachment": attachment}
    data = json.dumps(data)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_receipt_template(fbid, recipient_name, order_number, currency,
                          payment_method, summary, merchant_name='',
                          timestamp='', order_url='', elements=[],
                          address={}, adjustments=[]):
    """ Sends a receipt template for the specified user
    /docs/messenger-platform/send-api-reference/receipt-template

    :param str fbid: User id to send the receipt template.
    :param str recipient_name: Recipient's name.
    :param str order_number: Unique order number.
    :param str currency: Currency for order.
    :param str payment_method: Payment method details. ex - "Visa 1234".
    :param dict summary: Payment summary, format :

        >>> summary = {
          "subtotal": 75.00,
          "shipping_cost": 4.95,
          "total_tax": 6.19,
          "total_cost": 56.14
        }
    :param str timestamp: Timestamp of the order, in seconds.
    :param str order_url: URL of order.
    :param list elements: Items in order (Max 100), format :

        >>> elements = [
          {
            "title": "Classic White T-Shirt",
            "subtitle": "100% Soft and Luxurious Cotton",
            "quantity": 2,
            "price": 50,
            "currency": "USD",
            "image_url": "http://i.imgur.com/GHC4ZHl.jpg"
          },
          {
            "title": "Classic Gray T-Shirt",
            "subtitle": "100% Soft and Luxurious Cotton",
            "quantity": 1,
            "price": 25,
            "currency": "USD",
            "image_url": "http://i.imgur.com/GHC4ZHl.jpg"
          }
        ],
    :param dict address: Shipping address (If order has shipping),\
    format :

        >>> address = {
          "street_1": "1 Hacker Way",
          "street_2": "",
          "city": "Menlo Park",
          "postal_code": "94025",
          "state": "CA",
          "country": "US"
        }
    :param list adjustments: Payment adjustments, format :

        >>> adjustments = [
          {
            "name":"New Customer Discount",
            "amount":20
          },
          {
            "name":"$10 Off Coupon",
            "amount":10
          }
        ]
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    data = {}
    data['recipient'] = {'id': fbid}
    payload = {}
    payload['template_type'] = 'receipt'
    payload['recipient_name'] = recipient_name
    payload['order_number'] = order_number
    payload['currency'] = currency
    payload['payment_method'] = payment_method
    payload['summary'] = summary
    payload['order_url'] = order_url
    payload['timestamp'] = timestamp
    payload['elements'] = elements
    payload['address'] = address
    payload['adjustments'] = adjustments
    payload['merchant_name'] = merchant_name
    attachment = {"type": "template", "payload": payload}
    data['message'] = {"attachment": attachment}
    data = json.dumps(data)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_call_button(fbid, text, title, phone_number):
    """ Sends a call button for the specified user
    (/docs/messenger-platform/send-api-reference/call-button).

    :param str fbid: User id to send the call button
    :param str text: Text to send with the button (Max 160 Chars).
    :param str title: Button title (Max 20 Chars).
    :param str phone_number: Format must have "+" prefix followed by\
    the country code, area code and local number.\
    For example, **+16505551234**.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    data = {}
    data['recipient'] = {'id': fbid}
    payload = {}
    payload['template_type'] = 'button'
    payload['text'] = text
    button = {}
    button['type'] = 'phone_number'
    button['title'] = title
    button['payload'] = phone_number
    payload['buttons'] = [button]
    attachment = {"type": "template", "payload": payload}
    data['message'] = {"attachment": attachment}
    data = json.dumps(data)
    status = requests.post(url, headers=HEADER, data=data)
    return status
