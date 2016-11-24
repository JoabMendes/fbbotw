import json
import requests
import os

IMPORT_ERROR = "Couldn't import PAGE_ACCESS_TOKEN. \
Define this var in your settings configuration\
or as environment variable."

HEADER = {"Content-Type": "application/json"}

try:
    from django.conf import settings
    PAGE_ACCESS_TOKEN = settings.PAGE_ACCESS_TOKEN
except ImportError:
    # Not using Django
    PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN', False)
    if not PAGE_ACCESS_TOKEN:
        raise ImportError(IMPORT_ERROR)
except AttributeError:
    # Using django but did defined the config var PAGE_ACCESS_TOKEN
    raise ImportError(IMPORT_ERROR)

TD_STS_URL = 'https://graph.facebook.com/v2.6/me/thread_settings?access_token='
MSG_URL = 'https://graph.facebook.com/v2.6/me/messages?access_token='


#############################################
#        Tread Settings Functions           #
#############################################


def post_settings(greeting_text):
    """ Sets the START Button and also the Greeting Text.
        The payload for the START Button will be 'USER_START'

    :param str greeting_text: Desired Greeting Text (160 chars)
    :return: Response object
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

    :param str greeting_text: Desired Greeting Text (160 chars)
    :return: Response object
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

    :param str payload: Desired postback payload (Default START)
    :return: Response object
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

    :param list call_to_actions: example
    call_to_actions =  [
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
    :return: Response object
    """
    url = TD_STS_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload["setting_type"] = "call_to_actions"
    payload["thread_state"] = "existing_thread"
    payload["call_to_actions"] = call_to_actions
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


#############################################
#           Send Api Functions              #
#############################################


def typing(fbid, sender_action):
    """ Displays/Hides the typing gif/mark seen on facebook chat

    :param str fbid: User id to display action
    :param str sender_action: typing_off/typing_on/mark_seen
    :return: Response object
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload['recipient'] = {'id': fbid}
    payload['sender_action'] = sender_action
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def get_user_information(fbid):
    """ Gets user information: first_name, last_name, gender, profile_pic,
    locale, timezone, is_payment_enabled.
    https://developers.facebook.com/docs/messenger-platform/user-profile

    :param str fbid: User id to get the information
    :return: dict with keys
    """
    user_info_url = "https://graph.facebook.com/v2.7/%s" % fbid
    payload = {}
    payload['fields'] = 'first_name,last_name,gender,profile_pic,\
    locale,timezone,is_payment_enabled'
    payload['access_token'] = PAGE_ACCESS_TOKEN
    user_info = requests.get(user_info_url, payload).json()
    return user_info


def post_text_message(fbid, message):
    """ Sends a common text message

    :param str fbid: User id to get the text.
    :param str message: Text to be displayed for the user (230 chars)
    :return: Response object
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload['recipient'] = {'id': fbid}
    payload['message'] = {'text': message}  # Limit 320 chars
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_image_attachment(fbid, img_url):
    """ Sends an image attachment

    :param str fbid: User id to send the image.
    :para str img_url: Url of a hosted image.
    :return: Response object
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload['recipient'] = {'id': fbid}
    attachment = {"type": "image", "payload": {"url": img_url}}
    payload['message'] = {"attachment": attachment}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_text_w_quickreplies(fbid, message, quick_replies):
    """ Send text with quick replies buttons

    :param str fbid: User id to send the quick replies menu.
    :param str message: message to be displayed with the menu.
    :param list quick_replies: example
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
    :return: Response object
    """
    url = MSG_URL + PAGE_ACCESS_TOKEN
    payload = {}
    payload["recipient"] = {"id": fbid}
    payload["message"] = {"text": message, "quick_replies": quick_replies}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status
