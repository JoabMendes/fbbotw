import json
import requests
import os

IMPORT_ERROR = "Couldn't import PAGE_ACCESS_TOKEN. \
Define this var in your settings configuration\
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


THREAD_SETTINGS_URL = ("https://graph.facebook.com/v2.6/me/"
                       "thread_settings?access_token={access_token}")
MESSAGES_URL = ("https://graph.facebook.com/v2.6/me/"
                "messages?access_token={access_token}")
MESSENGER_PROFILE_URL = ("https://graph.facebook.com/v2.6/me/"
                         "messenger_profile?access_token={access_token}")
GRAPH_URL = ("https://graph.facebook.com/v2.7/{fbid}")

MESSAGES_ATTACHMENT_URL = ("https://graph.facebook.com/v2.6/me/"
                           "message_attachments?access_token={access_token}")

#############################################
#           User Profile API                #
#############################################


def get_user_information(fbid):
    """ Gets user basic information: first_name, last_name, gender,
    profile_pic, locale, timezone, is_payment_enabled, last_ad_referral.

    :usage:
        >>> # Set the user fbid you want the information
        >>> fbid = "<user fbid>"
        >>> # Call the function passing the fbid of user.
        >>> user_information = fbbotw.get_user_information(fbid=fbid)
    :param str fbid: User id to get the information.
    :return dict:

        >>> user_information = {
            "first_name": "User First Name",
            "last_name": "User Last Name",
            "gender": "male/female",
            "profile_pic": "https://cdn_to_pic.com/123",
            "locale": "en_US",
            "timezone": -3,
            "is_payment_enabled": True,
            "last_ad_referral": "https://reference.to.ad"
        }
    :facebook docs: `/user-profile <https://developers.facebook.com/docs/\
    messenger-platform/user-profile>`_
    """
    user_info_url = GRAPH_URL.format(fbid=fbid)
    payload = {}
    payload['fields'] = 'first_name,last_name,gender,profile_pic,\
    locale,timezone,is_payment_enabled,last_ad_referral'
    payload['access_token'] = PAGE_ACCESS_TOKEN
    user_info = requests.get(user_info_url, payload).json()
    return user_info


#############################################
#          Messenger Profile API            #
#############################################


def post_settings(greeting_text):
    """ Sets the **Get Started** Button and the **Greeting Text** at once.
    The payload for the **Get Started** Button will be `USER_START`.

    :usage:

        >>> # Create a default greeting text (160 chars limit)
        >>> greeting_text = "Hello! I'm your bot!"
        >>> responses = fbbotw.post_settings(
                greeting_text=greeting_text
            )
    :param str greeting_text: Desired Greeting Text (160 chars).
    :return: tuple with two `Response object <http://docs.python-requests.\
    org/en/master/api/#requests.Response>`_ for the greeting \
    text and start button.
    """
    # Set the greeting texts
    url = THREAD_SETTINGS_URL.format(access_token=PAGE_ACCESS_TOKEN)
    txtpayload = {}
    txtpayload['setting_type'] = 'greeting'
    txtpayload['greeting'] = {'text': greeting_text}
    data = json.dumps(txtpayload)
    greeting_text_status = requests.post(
        url, headers=HEADER, data=data
    )
    # Set the start button
    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
    btpayload = {}
    btpayload['get_started'] = {'payload': 'USER_START'}
    data = json.dumps(btpayload)
    get_started_button_status = requests.post(
        url, headers=HEADER, data=data
    )
    return (greeting_text_status, get_started_button_status)


def post_greeting_text(greeting_texts):
    """Sets an array of greetings texts *(Only default required)*

    - `See suported locales <https://developers.facebook.com/docs/m\
    essenger-platform/messenger-profile/supported-locales>`_
    - `See Personalization <https://developers.facebook.com/docs/\
     messenger-platform/messenger-profile/\
     greeting-text#personalization>`_

    :usage:

        >>> # Define the greeting texts you want
        >>> list_greeting_texts = [
                {
                    "locale": "default",
                    "text": "Hello, {{user_first_name}}! I'm a bpt"
                },
            ]
        >>> # Call the function to set the greeting text
        >>> response = fbbotw.post_greeting_text(
                greeting_texts=list_greeting_texts
            )
    :param list greeting_texts: format :

        >>> list_greeting_texts = [
                {
                    "locale": "default",
                    "text": "Hello, {{user_first_name}}!" # (160 chars)
                },
                {
                    "locale": "pt_BR",
                    "text": "Texto de Greeting em Portugues" # (160 chars)
                },
                {
                    "locale": "en_US",
                    "text": "Greeting text in English USA" # (160 chars)
                }
            ]
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/greeting-text <https://developers.facebook.com/docs/\
    messenger-platform/messenger-profile/greeting-text>`_
    """
    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload['greeting'] = greeting_texts
    data = json.dumps(payload)
    status = requests.post(
        url, headers=HEADER, data=data
    )
    return status


def post_start_button(payload='START'):
    """ Sets the **Get Started button**.

    :usage:

        >>> payload = 'GET_STARTED'
        >>> response = fbbotw.post_start_button(payload=payload)
    :param str payload: Desired postback payload (Default 'START').
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/get-started-button <https://developers.facebook\
    .com/docs/messenger-platform/messenger-profile/get-started-button>`_
    """
    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload_data = {}
    payload_data['get_started'] = {'payload': payload}
    data = json.dumps(payload_data)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_persistent_menu(persistent_menu):
    """ Sets persistent menus on the messenger chat view.

    :usage:

        >>> # Define you persistent menu dict
        >>> # See the fb docs for better reference on building it
        >>> persistent_menu =  [
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
                        },
                        {
                            "type": "postback",
                            "title": "Second Option",
                            "payload": "YOUR_PAYLOAD4"
                        },
                    ]
                }
            ]
        >>> # Set the menu calling the api
        >>> response = fbbotw.post_persistent_menu(
                persistent_menu=persistent_menu
            )
    :param list persistent_menu: format:

        >>> persistent_menu =  [
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
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/persistent-menu <https://developers.facebook.\
    com/docs/messenger-platform/messenger-profile/persistent-menu>`_
    """
    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload["persistent_menu"] = persistent_menu
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_domain_whitelist(whitelisted_domains):
    """ Sets the whistelisted domains for the Messenger Extension

    :usage:

        >>> # Define the array of domains to be whitelisted (Max 10)
        >>> whistelisted_domains = [
                "https://myfirst_domain.com",
                "https://another_domain.com"
            ]
        >>> fbbotw.post_domain_whitelist(
                whitelisted_domains=whitelisted_domains
            )
    :param list whistelisted_domains: Domains to be whistelisted (Max 10).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/domain-whitelisting <https://developers.facebook.\
    com/docs/messenger-platform/messenger-profile/domain-whitelisting>`_
    """
    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload['whitelisted_domains'] = whitelisted_domains
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def delete_domain_whitelist():
    """ Deletes the domain whitelist set previously .

    :usage:

        >>> response = fbbotw.delete_domain_whitelist()
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/domain-whitelisting#delete <https://developers.facebook.\
    com/docs/messenger-platform/messenger-profile/domain-whitelisting#delete>`_
    """
    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload['fields'] = ["whitelisted_domains"]
    data = json.dumps(payload)
    status = requests.delete(url, headers=HEADER, data=data)
    return status


def post_account_linking_url(account_linking_url):
    """ Sets the **liking_url** to connect the user with your business login

    :usage:

        >>> my_callback_linking_url = "https://my_business_callback.com"
        >>> response = fbbotw.post_account_linking_url(
                account_linking_url=my_callback_linking_url
            )
    :param str account_linking_url: URL to the account linking OAuth flow.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/account-linking-url <https://developers.facebook.\
    com/docs/messenger-platform/messenger-profile/account-linking-url>`_
    """
    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload['account_linking_url'] = account_linking_url
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_payment_settings(privacy_url="", public_key="", test_users=[]):
    """ Sets the configuration for payment: privacy policy url,
    public key or test users. At least one parameter should be passed
    in this function.

    :param str privacy_url: The payment_privacy_url will appear in \
    our payment dialogs.
    :param str public_key: The payment_public_key is used to encrypt \
    sensitive payment data sent to you. (Read payment reference on the \
    docs)
    :param list test_users: You can add payment test users \
    (user page-scoped id) so that their credit card won't be \
    charged during your development.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/payment-settings <https://developers.facebook.\
    com/docs/messenger-platform/messenger-profile/payment-settings>`_
    """
    if any([privacy_url.strip(), public_key.strip(), test_users]):
        url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
        payload = {"payment_settings": {}}
        if bool(privacy_url.strip()):
            payload['payment_settings']['privacy_url'] = privacy_url
        if bool(public_key.strip()):
            payload['payment_settings']['public_key'] = public_key
        if bool(test_users):
            payload['payment_settings']['testers'] = test_users
        data = json.dumps(payload)
        status = requests.post(url, headers=HEADER, data=data)
        return status
    return {"Error": "At least one parameter should be set"}


def post_target_audience(countries, audience_type="all"):
    """ Set the audience who will see your bot in the Discover tab \
    on Messenger.

    :usage:
        >>> # If you will set the audience to specific contries
        >>> # The audience_type param should be set to 'custom'
        >>> audience_type = "custom"
        >>> countries = {
                "whitelist": ["US", "UK", "CA", "BR"]
            }
        >>> response = fbbotw.post_target_audience(
                countries=countries,
                audience_type=audience_type
            )
    :param dict countries: Country object with whitelist/blacklist. Needs\
    to be specified only when audience_type is 'custom'. Countries should \
    be in list of ISO 3166 Alpha-2 codes. format:

        >>> countries = {
            "whitelist": ["US", "BR"]
            "blacklist": []
        }
    :param str audience_type: ("all", "custom", "none"). Default: "all"
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/target-audience <https://developers.facebook.\
    com/docs/messenger-platform/messenger-profile/target-audience>`_
    """
    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {"target_audience": {}}
    payload["target_audience"]["audience_type"] = audience_type
    if audience_type in ['custom', 'none']:
        payload["target_audience"]["countries"] = countries
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_chat_extension_home_url(
     url, webview_share_button="hide", in_test=True):
    """ Sets the url field enabling a Chat Extension in the composer \
    drawer in Messenger.

    :param str url: The URL to be invoked from drawer.
    :param str webview_share_button: Controls whether the share button in \
    the webview is enabled. (Set to "show" or "hide")
    :param bool in_test: Controls whether public users (not assigned to the \
    bot or its Facebook page) can see the Chat Extension.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/home-url <https://developers.facebook.\
    com/docs/messenger-platform/messenger-profile/home-url>`_
    """
    url = MESSENGER_PROFILE_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {"home_url": {}}
    payload["home_url"]["url"] = url
    payload["home_url"]["webview_height_ratio"] = "tall"
    payload["home_url"]["webview_share_button"] = webview_share_button
    payload["home_url"]["in_test"] = in_test
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


#############################################
#           Send Api Functions              #
#############################################

# Send API Sender Actions

def post_sender_action(fbid, sender_action):
    """ Displays/Hides the typing gif or shows mark seen on
    facebook chat with user.

    :usage:

        >>> # Set the user you want to show action
        >>> fbid = "<user page scoped id>"
        >>> # To show the typing animation
        >>> fbbotw.post_sender_action(
                fbid=fbid, sender_action="typing_on"
            )
        >>> # To stop typing (Stops automatically after 20s)
        >>> fbbotw.post_sender_action(
                fbid=fbid, sender_action="typing_off"
            )
        >>> # To mark as seen
        >>> fbbotw.post_sender_action(
                fbid=fbid, sender_action="mark_seen"
            )
    :param str fbid: User id to display action.
    :param str sender_action: `typing_off/typing_on/mark_seen`.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/sender-actions <https://developers.facebook.\
    com/docs/messenger-platform/send-api-reference/sender-actions>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload['recipient'] = {'id': fbid}
    payload['sender_action'] = sender_action
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


# Send API Content Type


def post_text_message(fbid, message):
    """ Sends a common text message to the specified user.

    :usage:

        >>> # Set the user fbid and the message you want to send.
        >>> fbid = "<user page scoped id>"
        >>> text = "Hi. How are you doing today?"
        >>> # Send the message to the user
        >>> response = fbbotw.post_text_message(
                fbid=fbid,
                message=text
            )
    :param str fbid: User id to send the text.
    :param str message: Text to be displayed for the user \
    (640 chars limit).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/text-message <https://developers.facebook.\
    com/docs/messenger-platform/send-api-reference/text-message>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload['recipient'] = {'id': fbid}
    payload['message'] = {'text': message}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_text_list(fbid, messages=[]):
    """ Sends a serie of messages from a list of texts. The
    messages will be sent in the same order as the list items.

    :usage:

        >>> # Set the user fbid and the list of texts to send.
        >>> fbid = "<user page scoped id>"
        >>> texts = [
                "Hi, Todays forecast is:",
                "Morning: Sunny - 27C",
                "Afternoon: Sunny - 25C",
                "Night: Cloudy - 18C"
            ]
        >>> response = fbbotw.post_text_list(
                fbid=fbid,
                messages=texts
            )
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


def post_attachment(fbid, media_url, file_type, is_reusable=False):
    """ Sends a media attachment to the specified user

    :param str fbid: User id to send the audio.
    :param str url: Url of a hosted media.
    :param str type: 'image'/'audio'/'video'/'file'.
    :param bool is_reusable: Defines the attachment to be resusable, \
    the response will have an attachment_id that can be used to \
    re-send the attachment without need to upload it again. (You can \
    use the post_reusable_attachment method to upload using the id).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/contenttypes <https://developers.facebook.\
    com/docs/messenger-platform/send-api-reference/contenttypes>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload['recipient'] = {'id': fbid}
    attachment_payload = {}
    attachment_payload['url'] = media_url
    if is_reusable:
        attachment_payload['is_reusable'] = is_reusable
    attachment = {"type": file_type, "payload": attachment_payload}
    payload['message'] = {"attachment": attachment}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def upload_reusable_attachment(media_url, file_type):
    """ Uploads an attachment to be used later. You can optimize \
    sending multimedia by reusing attachments.\
    If you're sending the same attachments repeatedly, you should \
    consider reusing them. Attachment reuse works with sending \
    images, audio clips, videos and files.

    :usage:

        >>> # Set the url for the hosted media
        >>> media_url = "http://i.imgur.com/uAUm3VW.jpg"
        >>> # Call the upload function. The response contains
        >>> # an id that should be stored. This id is the reference
        >>> # to send the same attachment in the future.
        >>> response = fbbotw.upload_reusable_attachment(
                media_url=media_url,
                file_type="image" # Always specify the file type
            )
        >>> # to get the attachment id, call the .json() function on
        >>> # the response object and get it on the returned dict.
        >>> attachment_id = response.json()['attachment_id']
        >>> # Store the attachment id to use later (You can
        >>> # use fbbotw.post_reusable_attachment to send it)
    :param str url: Url of a hosted media.
    :param str file_type: 'image'/'audio'/'video'/'file'.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_ (Contains the attachment id \
    to be used in `fbbotw.post_reusable_attachment`).
    :facebook docs: `/send-api-reference#attachment_reuse <https://\
    developers.facebook.com/docs/messenger-platform/send-api-refe\
    rence#attachment_reuse>`_
    """
    url = MESSAGES_ATTACHMENT_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    attachment_payload = {}
    attachment_payload['url'] = media_url
    attachment_payload['is_reusable'] = True
    attachment = {"type": file_type, "payload": attachment_payload}
    payload['message'] = {"attachment": attachment}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_reusable_attachment(fbid, attachment_id, file_type):
    """ Sends a reusable attachment based on the attachment\
    id to the specified user.

    :usage:

        >>> # Set the fbid of user you want to send the attachment
        >>> fbid = "<user page scoped id>"
        >>> # Retrive the attachment_id
        >>> attachment_id = "<reusable attachment id>"
        >>> # Call the function to send the attachment to the user
        >>> response = fbbotw.post_reusable_attachment(
                fbid=fbid,
                attachment_id=attachment_id,
                file_type="video"
            )
    :param str fbid: User id to send the attachment.
    :param str attachment_id: Id of file you got when sent the \
    attachment with the is_reusable flag as True or uploaded it using \
    fbbotw.upload_reusable_attachment.

    :param str file_type: 'image'/'audio'/'video'/'file'.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/send-api-reference#attachment_reuse <https://\
    developers.facebook.com/docs/messenger-platform/send-api-refe\
    rence#attachment_reuse>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload['recipient'] = {'id': fbid}
    attachment = {
        "type": file_type,
        "payload": {"attachment_id": attachment_id}
    }
    payload['message'] = {"attachment": attachment}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_audio_attachment(fbid, audio_url, is_reusable=False):
    """ Sends an audio attachment

    :usage:

        >>> # Set the fbid of user you want to send the attachment
        >>> fbid = "<user page scoped id>"
        >>> # Set the url for the hosted audio
        >>> audio_url = "http://fbbotw.master/media/turdus.ogg"
        >>> # Send the audio
        >>> response = fbbotw.post_audio_attachment(
                fbid=fbid,
                audio_url=audio_url
            )
        >>> # If you want to make this attachment reusable, send
        >>> # a third parameter as is_reusable=True and the response
        >>> # object will have the attachment id to be used later.
    :param str fbid: User id to send the audio.
    :param str audio_url: Url of a hosted audio (10 Mb).
    :param bool is_reusable: Defines the attachment to be resusable, \
    the response will have an attachment_id that can be used to \
    re-send the attachment without need to upload it again. (You can \
    use the post_reusable_attachment method to upload using the id).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/audio-attachment <https://\
    developers.facebook.com/docs/messenger-platform/send-api-reference\
    /audio-attachment>`_
    """
    return post_attachment(
        fbid=fbid,
        media_url=audio_url,
        file_type='audio',
        is_reusable=is_reusable
    )


def post_file_attachment(fbid, file_url, is_reusable=False):
    """ Sends a file attachment

    :usage:

        >>> # Set the fbid of user you want to send the attachment
        >>> fbid = "<user page scoped id>"
        >>> # Set the url for the hosted file
        >>> file_url = "http://fbbotw.master/media/fbbotw.pdf"
        >>> # Send the file
        >>> response = fbbotw.post_file_attachment(
                fbid=fbid,
                file_url=file_url
            )
        >>> # If you want to make this attachment reusable, send
        >>> # a third parameter as is_reusable=True and the response
        >>> # object will have the attachment id to be used later.
    :param str fbid: User id to send the file.
    :param str file_url: Url of a hosted file (10 Mb).
    :param bool is_reusable: Defines the attachment to be resusable, \
    the response will have an attachment_id that can be used to \
    re-send the attachment without need to upload it again. (You can \
    use the post_reusable_attachment method to upload using the id).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/file-attachment <https://\
    developers.facebook.com/docs/messenger-platform/send-api-reference\
    /file-attachment>`_
    """
    return post_attachment(
        fbid=fbid,
        media_url=file_url,
        file_type='file',
        is_reusable=is_reusable
    )


def post_image_attachment(fbid, img_url, is_reusable=False):
    """ Sends an image attachment

    :usage:

        >>> # Set the fbid of user you want to send the attachment
        >>> fbid = "<user page scoped id>"
        >>> # Set the url for the hosted image
        >>> img_url = "http://i.imgur.com/uAUm3VW.jpg"
        >>> # Send the image
        >>> response = fbbotw.post_image_attachment(
                fbid=fbid,
                img_url=img_url
            )
        >>> # If you want to make this attachment reusable, send
        >>> # a third parameter as is_reusable=True and the response
        >>> # object will have the attachment id to be used later.
    :param str fbid: User id to send the image.
    :param str img_url: Url of a hosted image (jpg, png, gif).
    :param bool is_reusable: Defines the attachment to be resusable, \
    the response will have an attachment_id that can be used to \
    re-send the attachment without need to upload it again. (You can \
    use the post_reusable_attachment method to upload using the id)
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/image-attachment <https://\
    developers.facebook.com/docs/messenger-platform/send-api-reference\
    /image-attachment>`_
    """
    return post_attachment(
        fbid=fbid,
        media_url=img_url,
        file_type='image',
        is_reusable=is_reusable
    )


def post_video_attachment(fbid, video_url, is_reusable=False):
    """ Sends a video attachment

    :usage:

        >>> # Set the fbid of user you want to send the attachment
        >>> fbid = "<user page scoped id>"
        >>> # Set the url for the hosted video
        >>> video_url = "http://fbbotw.master/media/fbbotw_drop.mp4"
        >>> # Send the video
        >>> response = fbbotw.post_video_attachment(
                fbid=fbid,
                video_url=video_url
            )
        >>> # If you want to make this attachment reusable, send
        >>> # a third parameter as is_reusable=True and the response
        >>> # object will have the attachment id to be used later.
    :param str fbid: User id to send the file.
    :param str fbid: User id to send the video.
    :param str video_url: Url of a hosted video.
    :param bool is_reusable: Defines the attachment to be resusable, \
    the response will have an attachment_id that can be used to \
    re-send the attachment without need to upload it again. (You can \
    use the post_reusable_attachment method to upload using the id)
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/video-attachment <https://\
    developers.facebook.com/docs/messenger-platform/send-api-reference\
    /video-attachment>`_
    """
    return post_attachment(
        fbid=fbid,
        media_url=video_url,
        file_type='video',
        is_reusable=is_reusable
    )


# Send API Quick Replies

def post_text_w_quickreplies(fbid, message, quick_replies):
    """ Send text with quick replies buttons

    :usage:

        >>> # Set the user id and the message to send
        >>> fbid = "<user page scoped id>"
        >>> message = "Hi! Do you want to know today's forecast?"
        >>> # Set the quick replies list to be sent
        >>> quick_replies = [
                {
                    "content_type": "text",
                    "title": "Yes!",
                    "payload": "SEND_FORECAST"
                },
                {
                    "content_type": "text",
                    "title": "Nope",
                    "payload": "USER_SAY_NOT"
                }
            ]
        >>> # Send the message with the quick_replies
        >>> response = fbbotw.post_text_w_quickreplies(
                fbid=fbid,
                message=message,
                quick_replies=quick_replies
            )
    :param str fbid: User id to send the quick replies menu.
    :param str message: message to be displayed with the quick replies.
    :param list quick_replies: (Max 11) format :

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
            },
            {
                "content_type": "location",
            },
            {
                "content_type": "text",
                "title": "Red",
                "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                "image_url": "http://petersfantastichats.com/img/red.png"
            },
        ]
        >>> # See all the fields for the quick reply object in the docs:
        >>> # /docs/messenger-platform/send-api-reference/quick-replies
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/quick-replies <https://developers.facebook\
    .com/docs/messenger-platform/send-api-reference/quick-replies>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload["recipient"] = {"id": fbid}
    payload["message"] = {"text": message, "quick_replies": quick_replies}
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_image_w_quickreplies(fbid, image_url, quick_replies):
    """ Sends an image with quick replies menu

    :usage:

        >>> # Set the user id and the hosted image to send
        >>> fbid = "<user page scoped id>"
        >>> image_url = "http://i.imgur.com/uAUm3VW.jpg"
        >>> # Set the quick replies list to be sent
        >>> quick_replies = [
                {
                    "content_type": "text",
                    "title": "I'm a dog person",
                    "payload": "USER_DISLIKES"
                },
                {
                    "content_type": "text",
                    "title": "This is a noice cat!",
                    "payload": "USER_LIKES"
                }
            ]
        >>> # Send the image with the quick_replies
        >>> response = fbbotw.post_image_w_quickreplies(
                fbid=fbid,
                image_url=image_url,
                quick_replies=quick_replies
            )
    :param str fbid: User id to send the quick replies menu.
    :param str image_url: image to be displayed with the quick-replies.
    :param list quick_replies: (Max 11) format :

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
            },
            {
                "content_type": "location",
            },
            {
                "content_type": "text",
                "title": "Red",
                "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                "image_url": "http://petersfantastichats.com/img/red.png"
            },
        ]
        >>> # See all the fields for the quick reply object in the docs:
        >>> # /docs/messenger-platform/send-api-reference/quick-replies
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/quick-replies <https://developers.facebook\
    .com/docs/messenger-platform/send-api-reference/quick-replies>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    payload = {}
    payload["recipient"] = {"id": fbid}
    attachment = {}
    attachment['type'] = 'image'
    attachment['payload'] = {"url": image_url}
    payload["message"] = {
        "attachment": attachment,
        "quick_replies": quick_replies
    }
    data = json.dumps(payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_template_w_quickreplies(fbid, payload, quick_replies):
    """ Sends a template with quick replies buttons


    :usage:

        >>> # Set the user id and the template playload to send
        >>> fbid = "<user page scoped id>"
        >>> # This is a generic template payload dict
        >>> payload = {
                "template_type": "generic",
                "elements": [
                    {
                        "title": "Welcome to Peter\'s Hats",
                        "image_url": "https://site.com/company_image.png",
                        "subtitle": "We've got the right hat for everyone.",
                    }
                ]
            }
        >>> # Set the quick replies list to be sent
        >>> quick_replies = [
                {
                    "content_type": "text",
                    "title": "Payment options",
                    "payload": "PAYMENT_OPTIONS"
                },
                {
                    "content_type": "text",
                    "title": "See hat options",
                    "payload": "SEND_CATALOGUE"
                }
            ]
        >>> # Send the template with the quick_replies
        >>> response = fbbotw.post_template_w_quickreplies(
                fbid=fbid,
                payload=payload,
                quick_replies=quick_replies
            )
    :param str fbid: User id to send the quick replies menu.
    :param dict payload: template playload dict. See the \
    payload `field <https://developers.facebook.com/docs/\
    messenger-platform/send-api-reference/templates>`_ for \
    every template type.
    :param list quick_replies: (Max 11) format :

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
            },
            {
                "content_type": "location",
            },
            {
                "content_type": "text",
                "title": "Red",
                "payload": "DEVELOPER_DEFINED_PAYLOAD_FOR_PICKING_RED",
                "image_url": "http://petersfantastichats.com/img/red.png"
            },
        ]
        >>> # See all the fields for the quick reply object in the docs:
        >>> # /docs/messenger-platform/send-api-reference/quick-replies
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/quick-replies <https://developers.facebook\
    .com/docs/messenger-platform/send-api-reference/quick-replies>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    request_payload = {}
    request_payload["recipient"] = {"id": fbid}
    attachment = {}
    attachment['type'] = 'template'
    attachment['payload'] = payload
    request_payload["message"] = {
        "attachment": attachment,
        "quick_replies": quick_replies
    }
    data = json.dumps(request_payload)
    status = requests.post(url, headers=HEADER, data=data)
    return status


# Send API Templates

def post_button_template(fbid, text, buttons, sharable=True):
    """ Sends a button template with the specified text and buttons.
    Check the `docs <https://developers.facebook.com/docs/\
    messenger-platform/send-api-reference/buttons>`_ to \
    see the diffrent *types* of buttons.

    :usage:

        >>> # Set the user id and text to send with the template
        >>> fbid = "<user page scoped id>"
        >>> text = "Would you like to login?"
        >>> # Set the buttons list
        >>> buttons = [
                {
                    'type': 'postback',
                    'title': 'Meh',
                    'payload': 'USER_DOESNT_WANT_LOGGIN'
                },
                {
                    'type': 'web_url',
                    'url': 'https://petersapparel.parseapp.com',
                    'title': "LOG ME IN"
                }
            ]
        >>> # Send the template
        >>> response = fbbotw.post_button_template(
                fbid=fbid,
                text=text,
                buttons=buttons
            )
    :param str fbid: User id to send the buttons.
    :param str text: Message to be displayed with the buttons (640 Chars).
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
            {
                'type': 'element_share',
            }
        ]
    :param bool sharable: Able/Disable native share button in Messenger \
    for the template message (Default: True).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_.
    :facebook docs: `/button-template <https://developers.facebook\
    .com/docs/messenger-platform/send-api-reference/button-template>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    data = {}
    data['recipient'] = {'id': fbid}
    payload = {}
    payload['template_type'] = 'button'
    payload['text'] = text
    payload['buttons'] = buttons
    if not sharable:
        payload['sharable'] = False
    attachment = {"type": 'template', "payload": payload}
    data['message'] = {"attachment": attachment}
    data = json.dumps(data)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_generic_template(fbid, title, image_url='', subtitle='',
                          buttons=[], default_action={}, sharable=True,
                          image_aspect_ratio='horizontal'):
    """ Sends a single generic template for the specified User

    :usage:

        >>> # This function sends only one element of a generic template
        >>> # You can set the user id, the template title, image, subtitle
        >>> # buttons and other parameers just by the function
        >>> fbid = "<user page scoped id>"
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
        >>> # Send the template
        >>> response = fbbotw.post_generic_template(
                fbid=fbid,
                title="This is a generic template",
                image_url="http://i.imgur.com/uAUm3VW.jpg",
                buttons=buttons,
                image_aspect_ratio='square'
            )
    :param str fbid: User id to send the generic template.
    :param str title: Bubble title (80 Chars).
    :param str image_url: Bubble image (Optional)(Ratio 1.91:1).
    :param str subtitle: Bubble subtitle (Optional)(80 Chars).
    :param dict default_action: Default action to be triggered \
    when user taps on the element. See the `docs <https://develo\
    pers.facebook.com/docs/messenger-platform/send-api-reference\
    /generic-template#default_action>`_ for reference (Optional).
    :param list buttons: (Optional)(Max 3) format :

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
    :param bool sharable: Able/Disable native share button in Messenger \
    for the template message (Default: True).
    :param str image_aspect_ratio: Aspect ratio used to render images \
    specified by image_url in element objects. Must be 'horizontal' or \
    'square'. (Default 'horizontal')
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/generic-template <https://developers.facebook\
    .com/docs/messenger-platform/send-api-reference/generic-template>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    data = {}
    data['recipient'] = {'id': fbid}
    payload = {}
    payload['template_type'] = 'generic'
    if not sharable:
        payload['sharable'] = False
    if image_aspect_ratio != 'horizontal':
        payload['image_aspect_ratio'] = 'square'
    payload['elements'] = []
    element = {}
    element['title'] = title
    if bool(image_url):
        element['image_url'] = image_url
    if bool(subtitle):
        element['subtitle'] = subtitle
    if bool(buttons):
        element['buttons'] = buttons
    payload['elements'].append(element)
    attachment = {"type": 'template', "payload": payload}
    data['message'] = {"attachment": attachment}
    data = json.dumps(data)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_generic_template_carousel(fbid, elements,
                                   sharable=True,
                                   image_aspect_ratio='horizontal'):
    """  Sends up to 10 generic template elements as a carousel.

    :usage:

        >>> # Set the user to receive generic templates
        >>> fbid = "<user page scoped id>"
        >>> # Build the elements list
        >>> elements = [
                {
                    "title": "Title Texts",
                    "item_url": "https://mylink.com",
                    "subtitle": "Subtitle Text",
                    "default_action": {
                      "type": "web_url",
                      "url": "https://mylink.com",
                    }
                    "buttons": [
                        {
                            'type': 'web_url',
                            'url': 'https://mylink.com',
                            'title': 'My button'
                        }
                    ],
                    "image_url": "http://i.imgur.com/SOnSwUT.jpg"
                },
                # ... You can insert up to 10 elements in the list
            ]
        >>> # Send the carousel
        >>> response = fbbotw.post_generic_template_carousel(
                fbid=fbid,
                elements=elements
            )
    :param str fbid: User to be messaged
    :param list elements: generic templates `elements <https://deve\
    lopers.facebook.com/docs/messenger-platform/send-api-reference/\
    generic-template#element>`_ (Max 10 itens). format:

        >>> elements = [
            {
                "title": "Title Texts",
                "item_url": "https://mylink.com",
                "subtitle": "Subtitle Text",
                "default_action": {
                  "type": "web_url",
                  "url": "https://mylink.com",
                }
                "buttons": [
                    {
                        'type': 'web_url',
                        'url': 'https://mylink.com',
                        'title': 'My button'
                    }
                ],
                "image_url": "http://i.imgur.com/SOnSwUT.jpg"
            }
        ]
    :param bool sharable: Able/Disable native share button in Messenger \
    for the template message (Default: True).
    :param str image_aspect_ratio: Aspect ratio used to render images \
    specified by image_url in element objects. Must be 'horizontal' or \
    'square'. (Default 'horizontal')
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/generic-template <https://developers.facebook\
    .com/docs/messenger-platform/send-api-reference/generic-template>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    data = {}
    data['recipient'] = {'id': fbid}
    payload = {}
    payload['template_type'] = 'generic'
    payload['elements'] = elements
    if not sharable:
        payload['sharable'] = False
    if image_aspect_ratio != 'horizontal':
        payload['image_aspect_ratio'] = 'square'
    attachment = {"type": 'template', "payload": payload}
    data['message'] = {"attachment": attachment}
    data = json.dumps(data)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_list_template(fbid, elements, buttons=[],
                       top_element_style='large', sharable=True):
    """ Sends a list template for the specified User

    :param str fbid: User id to send the list template.
    :param str top_element_style: large/compact (Default 'large').
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
    :param bool sharable: Able/Disable native share button in Messenger \
    for the template message (Default: True).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/list-template <https://developers.facebook\
    .com/docs/messenger-platform/send-api-reference/list-template>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    data = {}
    data['recipient'] = {'id': fbid}
    payload = {}
    payload['template_type'] = 'list'
    payload['top_element_style'] = top_element_style
    if bool(buttons):
        payload['buttons'] = buttons
    payload['elements'] = elements
    if not sharable:
        payload['sharable'] = False
    attachment = {"type": 'template', "payload": payload}
    data['message'] = {"attachment": attachment}
    data = json.dumps(data)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_receipt_template(fbid, recipient_name, order_number, currency,
                          payment_method, summary, merchant_name='',
                          timestamp='', order_url='', elements=[],
                          address={}, adjustments=[], sharable=True):
    """ Sends a receipt template for the specified user

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
    :param bool sharable: Able/Disable native share button in Messenger \
    for the template message (Default: True).
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/receipt-template <https://developers.facebook\
    .com/docs/messenger-platform/send-api-reference/receipt-template>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
    data = {}
    data['recipient'] = {'id': fbid}
    payload = {}
    payload['template_type'] = 'receipt'
    payload['recipient_name'] = recipient_name
    payload['order_number'] = order_number
    payload['currency'] = currency
    payload['payment_method'] = payment_method
    payload['summary'] = summary
    if bool(order_url.strip()):
        payload['order_url'] = order_url
    if bool(timestamp.strip()):
        payload['timestamp'] = timestamp
    if bool(elements):
        payload['elements'] = elements
    if bool(address):
        payload['address'] = address
    if bool(adjustments):
        payload['adjustments'] = adjustments
    if bool(merchant_name):
        payload['merchant_name'] = merchant_name
    if not sharable:
        payload['sharable'] = False
    attachment = {"type": "template", "payload": payload}
    data['message'] = {"attachment": attachment}
    data = json.dumps(data)
    status = requests.post(url, headers=HEADER, data=data)
    return status


def post_call_button(fbid, text, title, phone_number):
    """ Sends a call button for the specified user.
    The Call Button can be used to initiate a phone call
    on mobile.

    :usage:

        >>> # Set the user to send the button
        >>> fbid = "<user page scoped id>"
        >>> # Set text and title of the template
        >>> response = fbbotw.post_call_button(
                fbid=fbid,
                text="Do you call an consultant?"
                title="Call now",
                phone_number="+112345678"
            )
    :param str fbid: User id to send the call button
    :param str text: Text to send with the button (Max 160 Chars).
    :param str title: Button title (Max 20 Chars).
    :param str phone_number: Format must have "+" prefix followed by\
    the country code, area code and local number.\
    For example, **+16505551234**.
    :return: `Response object <http://docs.python-requests.org/en/\
    master/api/#requests.Response>`_
    :facebook docs: `/call-button <https://developers.facebook\
    .com/docs/messenger-platform/send-api-reference/call-button>`_
    """
    url = MESSAGES_URL.format(access_token=PAGE_ACCESS_TOKEN)
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
