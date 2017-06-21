FBBOTW: A `Facebook Messenger`_ Platform API Wrapper
====================================================

|Build Status| |Documentation Status| |PyPI| |MIT licensed|

This wrapper makes it simpler to user the *Facebook Messenger platform*
wrapping the endpoints as functions.

For exemple, to send a text message to the user you can easily do:

.. code:: py

    from fbbotw import fbbotw
    # ...

    user_fbid = "<user fb id>"
    my_message = "Hello World"

    fbbotw.post_text_message(fbid=user_fbid, message=my_message)
    # The user with the specified fbid will receive the text 'Hello World'

This is much less code than the traditional way to call the ``Send API``
and send a text. Using ``requests`` and ``json`` you probably would do
like this:

.. code:: py

      fbid = "<user psid>"
      message = "Hello World"
      url = 'https://graph.facebook.com/v2.6/me/messages?access_token={0}'
      url = url.format(PAGE_ACCESS_TOKEN)
      header = {"Content-Type": "application/json"}
      payload = {}
      payload['recipient'] = {'id': fbid}
      payload['message'] = {'text': message}
      data = json.dumps(payload)
      response = requests.post(url=url, headers=header, data=data)


Get Started
-----------

1- Install
~~~~~~~~~~

.. code:: sh

    pip install fbbotw

2 - Configure it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The only configuration needed is to set the ``PAGE_ACCESS_TOKEN`` with
the value you got from the `facebook app dashboard`_. If you are
using Django, create the variable in your ``settings.py``. If not,
define the variable in your enviroment:

2.1 - Django
^^^^^^^^^^^^

In your ``settings.py`` define the variable ``PAGE_ACCESS_TOKEN`` that was
generated on the app configuration from facebook.

.. code:: py

    #settings.py
    PAGE_ACCESS_TOKEN = "<your access token>"

2.2 - Not Django
^^^^^^^^^^^^^^^^

Create an **os environment** variable called ``PAGE_ACCESS_TOKEN``:

.. code:: sh

    export PAGE_ACCESS_TOKEN='<your access token>'

3 - Import and Use it
~~~~~~~~~~~~~~~~~~~~~

After setting the access token, just import and use ``fbbotw``
methods:

.. code:: py

    from fbbotw import fbbotw

    fbbotw.post_sender_action(fbid="<user psid>", sender_action="typing_on")


See the next topic to learn about the methods provided by the package

Methods Guide
=============

Send Api
--------

Sender Actions
~~~~~~~~~~~~~~

- :doc:`fbbotw.post_sender_action <methods/send_api/post_sender_action>`

Content Type
~~~~~~~~~~~~

- :doc:`fbbotw.post_text_message <methods/send_api/post_text_message>`
- :doc:`fbbotw.post_text_list <methods/send_api/post_text_list>`
- :doc:`fbbotw.post_audio_attachment <methods/send_api/post_audio_attachment>`
- :doc:`fbbotw.post_file_attachment <methods/send_api/post_file_attachment>`
- :doc:`fbbotw.post_image_attachment <methods/send_api/post_image_attachment>`
- :doc:`fbbotw.post_video_attachment <methods/send_api/post_video_attachment>`
- :doc:`fbbotw.upload_reusable_attachment <methods/send_api/upload_reusable_attachment>`
- :doc:`fbbotw.post_reusable_attachment <methods/send_api/post_reusable_attachment>`

Quick Replies
~~~~~~~~~~~~~

- :doc:`fbbotw.post_text_w_quickreplies <methods/send_api/post_text_w_quickreplies>`
- :doc:`fbbotw.post_image_w_quickreplies <methods/send_api/post_image_w_quickreplies>`
- :doc:`fbbotw.post_template_w_quickreplies <methods/send_api/post_template_w_quickreplies>`

Templates
~~~~~~~~~

- :doc:`fbbotw.post_button_template <methods/send_api/post_button_template>`
- :doc:`fbbotw.post_generic_template <methods/send_api/post_generic_template>`
- :doc:`fbbotw.post_generic_template_carousel <methods/send_api/post_generic_template_carousel>`
- :doc:`fbbotw.post_list_template <methods/send_api/post_list_template>`
- :doc:`fbbotw.post_receipt_template <methods/send_api/post_receipt_template>`
- :doc:`fbbotw.post_call_button <methods/send_api/post_call_button>`

Miscellaneous: User Profile API
-------------------------------

- :doc:`fbbotw.get_user_information <methods/user_profile_api/get_user_information>`

Miscellaneous: Messenger Profile API
------------------------------------

- :doc:`fbbotw.post_greeting_text <methods/messenger_profile_api/post_greeting_text>`
- :doc:`fbbotw.post_start_button <methods/messenger_profile_api/post_start_button>`
- :doc:`fbbotw.post_settings <methods/messenger_profile_api/post_settings>`
- :doc:`fbbotw.post_persistent_menu <methods/messenger_profile_api/post_persistent_menu>`
- :doc:`fbbotw.post_domain_whitelist <methods/messenger_profile_api/post_domain_whitelist>`
- :doc:`fbbotw.delete_domain_whitelist <methods/messenger_profile_api/delete_domain_whitelist>`
- :doc:`fbbotw.post_account_linking_url <methods/messenger_profile_api/post_account_linking_url>`
- :doc:`fbbotw.post_payment_settings <methods/messenger_profile_api/post_payment_settings>`
- :doc:`fbbotw.post_target_audience <methods/messenger_profile_api/post_target_audience>`
- :doc:`fbbotw.post_chat_extension_home_url <methods/messenger_profile_api/post_chat_extension_home_url>`

The Response Return
===================

This package uses the `Requests`_ library to consume the Messenger API.
For that reason, almost every function of this package, except *get_user_information*, returns an *Response object*

The *Response* object represent the server response to an HTTP request. In our case, the facebook response
to our request. 

.. code:: py
    
    # Response object represents what the facebook server answered
    response = fbbotw.post_text_message(fbid="1223", message="Hi user")
    # The response objects has some attributes and methods to help verify the response:
    if (response.status_code == 200): 
        # if response code is 200, request was successful
        # We can see the response body calling the method .json()
        print(response.json())
        # will print {'message_id': 'mid.$cAAJoUiFKdHJi-Oj9r1cx6O1cpi6C', 'recipient_id': '1223'}
        # message_id: id of sent message
        # recipient_id: fbid of user that got the message

This `topic <http://docs.python-requests.org/en/master/api/#requests.Response>`_ on the *Request* docs describes all the Response attributes and methods.

Debugging
=========

**fbbotw** doesn't do any verification on the parameters and all
validation is done on the facebook server. If one method isn't working, check the
response object returned. It will describe which was the error or
bad parameter. You can check that by calling the `.json()` method on the `response object <#the-response-return>`_.

Current wrapper covering for the `Menssenger Platform 2.0`_
===========================================================

-  [ ] Send API
  -  [x] Content Types
    -  [x] `Text messages <https://developers.facebook.com/docs/messenger-platform/send-api-reference/text-message>`_
    -  [x] `Audio attachment <https://developers.facebook.com/docs/messenger-platform/send-api-reference/audio-attachment>`_
    -  [x] `Image attachment <https://developers.facebook.com/docs/messenger-platform/send-api-reference/image-attachment>`_
    -  [x] `Video attachment <https://developers.facebook.com/docs/messenger-platform/send-api-reference/video-attachment>`_
    -  [x] `File attachment <https://developers.facebook.com/docs/messenger-platform/send-api-reference/file-attachment>`_
  -  [x] `Quick Replies <https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies>`_
  -  [x] `Sender Actions <https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions>`_
  -  [x] `Attachment Upload API <https://developers.facebook.com/docs/messenger-platform/send-api-reference/attachment-upload>`_
  -  [ ] Templates
    -  [x] `Button Template <https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template>`_
    -  [x] `Generic Template <https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template>`_
    -  [x] `List Template <https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template>`_
    -  [x] `Receipt Template <https://developers.facebook.com/docs/messenger-platform/send-api-reference/receipt-template>`_
    -  [ ] Open Graph Template
    -  [ ] Airline Boarding Pass Template
    -  [ ] Airline Checkin Template
    -  [ ] Airline Itinerary Template
    -  [ ] Airline Flight Update Template
-  [x] `Buttons: Check documentation to format your buttons in your templates <https://developers.facebook.com/docs/messenger-platform/send-api-reference/buttons>`_
  -  [x] `Call Button <https://developers.facebook.com/docs/messenger-platform/send-api-reference/call-button>`_

-  [ ] Miscellaneous
  -  [x] `User profile <https://developers.facebook.com/docs/messenger-platform/user-profile>`_
  -  [x] Messenger Profile API
    -  [x] `Persistent Menu <https://developers.facebook.com/docs/messenger-platform/messenger-profile/persistent-menu>`_
    -  [x] `Get Started Button <https://developers.facebook.com/docs/messenger-platform/messenger-profile/get-started-button>`_
    -  [x] `Greeting Text <https://developers.facebook.com/docs/messenger-platform/messenger-profile/greeting-text>`_
    -  [x] `Domain Whitelisting <https://developers.facebook.com/docs/messenger-platform/messenger-profile/domain-whitelisting>`_
    -  [x] `Account Linking <https://developers.facebook.com/docs/messenger-platform/messenger-profile/account-linking-url>`_
    -  [x] `Payment Settings <https://developers.facebook.com/docs/messenger-platform/messenger-profile/payment-settings>`_
    -  [x] `Target Audience <https://developers.facebook.com/docs/messenger-platform/messenger-profile/target-audience>`_
    -  [x] `Chat Extension Home URL (Covered but no tested) <https://developers.facebook.com/docs/messenger-platform/messenger-profile/home-url>`_
  -  [ ] Plugin Reference
  -  [ ] Messenger Code API
  -  [ ] Messaging Insights API

.. _Requests: http://docs.python-requests.org/en/master/
.. _facebook app dashboard: https://developers.facebook.com/docs/messenger-platform/guides/setup#page_access_token
.. _Facebook Messenger: https://developers.facebook.com/products/messenger/
.. _DOCS: http://fbbotw.readthedocs.io/en/latest/
.. _Read the Docs: http://fbbotw.readthedocs.io/en/latest/
.. _Menssenger Platform 2.0: https://developers.facebook.com/docs/messenger-platform/product-overview

.. |Build Status| image:: https://travis-ci.org/JoabMendes/fbbotw.svg?branch=master
   :target: https://travis-ci.org/JoabMendes/fbbotw
.. |Documentation Status| image:: https://readthedocs.org/projects/fbbotw/badge/?version=latest
   :target: http://fbbotw.readthedocs.io
.. |PyPI| image:: https://img.shields.io/pypi/v/fbbotw.svg
   :target: https://pypi.python.org/pypi?name=fbbotw&:action=display
.. |MIT licensed| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE
