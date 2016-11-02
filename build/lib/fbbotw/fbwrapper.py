import json
import requests

try:
    from django.conf import settings
    PAGE_ACCESS_TOKEN = settings.PAGE_ACCESS_TOKEN
except ImportError:
    PAGE_ACCESS_TOKEN = "<Set the page access token here>"

HEADER = {"Content-Type": "application/json"}

def post_settings(welcometext):
    ''' Sets the START button and welcome text. '''
    # Set the greeting texts
    url = 'https://graph.facebook.com/v2.6/me/thread_settings?access_token='
    url += PAGE_ACCESS_TOKEN
    txtpayload = {}
    txtpayload["setting_type"] = "greeting"
    txtpayload["greeting"] = {"text": welcometext}
    response_msg = json.dumps(txtpayload)
    status = requests.post(url, headers=HEADER, data=response_msg)
    # Set the start button
    btpayload = {}
    btpayload["setting_type"] = "call_to_actions"
    btpayload["thread_state"] = "new_thread"
    btpayload["call_to_actions"] = [{"payload": "USER_START"}]
    response_msg = json.dumps(btpayload)
    status = requests.post(url, headers=HEADER, data=response_msg)


def typing(fbid, sender_action):
    '''
        Displays the typing gif on facebook chat
        sender_action: typing_off/typing_on
    '''
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
    url += PAGE_ACCESS_TOKEN
    payload = {}
    payload['recipient'] = {'id': fbid}
    payload['sender_action'] = sender_action
    header = {"Content-Type": "application/json"}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)


def get_user_information(fbid):
    '''
        Gets user information: first_name, last_name, gender, profile_pic.
    '''
    # DOC: https://developers.facebook.com/docs/messenger-platform/user-profile
    user_info_url = "https://graph.facebook.com/v2.7/%s" % fbid
    payload = {}
    payload['fields'] = 'first_name,last_name,gender,profile_pic'
    payload['access_token'] = PAGE_ACCESS_TOKEN
    user_info = requests.get(user_info_url, payload).json()
    return user_info

def post_text_message(fbid, message):
    '''
        Sends a common text message
    '''
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
    url += PAGE_ACCESS_TOKEN
    payload = {}
    payload['recipient'] = {'id': fbid}
    payload['message'] = {'text': message} # Limit 320 chars
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)


def post_image_attch(fbid, imgurl):
    '''
        Sends an image attachment.
    '''
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
    url += PAGE_ACCESS_TOKEN
    payload = {}
    payload['recipient'] = {'id': fbid}
    payload['message'] = { "attachment":{ "type":"image", "payload":{ "url": imgurl}}}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)


def post_text_w_quickreplies(fbid, message, quick_replies):
    '''
        Send text with quick replies buttons
        quick_replies format:
        quick_replies = [
            {
                "content_type" : "text",
                "title" : "Yes!",
                "payload": "USER_SAY_YES"
            },
            {
                "content_type" : "text",
                "title" : "Nope",
                "payload": "USER_SAY_NOT"
            }
        ]
    '''
    url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
    url += PAGE_ACCESS_TOKEN
    payload = {}
    payload["recipient"] = {"id" : fbid}
    payload["message"] = {"text": message, "quick_replies" : quick_replies}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
