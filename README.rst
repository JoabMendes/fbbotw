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

Learn more about the fbbotw methods by reading the `DOCS`_

Install
-------

.. code:: sh

    pip install fbbotw

Using with Django
-----------------

| 1 - In your ``settings.py`` define the variable ``PAGE_ACCESS_TOKEN``
  that was
| generated on the app configuration from facebook.

.. code:: py

    #settings.py
    PAGE_ACCESS_TOKEN = "<your access token>"

or create an environment variable with the same name:

.. code:: sh

    export PAGE_ACCESS_TOKEN='<your access token>'

2 - After setting the access token, just import and use fbbotw methods:

.. code:: py

    from fbbotw import fbbotw

    fbbotw.post_sender_action(fbid="<user psid>", sender_action="typing_on")

If you want to use this package without Django
----------------------------------------------

#. Download the .zip of this directory.

#. Copy the ``fbbotw`` directory to your project root.

#. Define a environment variable called ``PAGE_ACCESS_TOKEN`` as the
   page access token you got from facebook

#. Import the package in your module.

.. code:: py

    from fbbotw import fbbotw

    fbbotw.post_sender_action(fbid="<user psid>", sender_action="typing_on")

Documentation
=============

-  `Read the Docs`_

Current wrapper covering for the `Menssenger Platform 2.0`_
===========================================================

-  [ ] Send API

  -  [x] Content Types

     -  [x] [Text messages](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/text-message)
     -  [x] [Audio attachment](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/audio-attachment)
     -  [x] [Image attachment](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/image-attachment)
     -  [x] [Video attachment](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/video-attachment)
     -  [x] [File attachment](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/file-attachment)

  -  [x] [Quick Replies](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies)
  -  [x] [Sender Actions](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions)
  -  [x] [Attachment Upload API](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/attachment-upload)
  -  [ ] Templates

    -  [x] [Button Template](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template)
    -  [x] [Generic Template](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template)
    -  [x] [List Template](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template)
    -  [x] [Receipt Template](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/receipt-template)
    -  [ ] Open Graph Template
    -  [ ] Airline Boarding Pass Template
    -  [ ] Airline Checkin Template
    -  [ ] Airline Itinerary Template
    -  [ ] Airline Flight Update Template

-  [x] [Buttons: Check documentation to format your buttons in your templates](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/buttons)

  -  [x] [Call Button](\ https://developers.facebook.com/docs/messenger-platform/send-api-reference/call-button)

-  [ ] Miscellaneous

  -  [x] [User profile](\ https://developers.facebook.com/docs/messenger-platform/user-profile)
  -  [x] Messenger Profile API

    -  [x] [Persistent Menu](\ https://developers.facebook.com/docs/messenger-platform/messenger-profile/persistent-menu)
    -  [x] [Get Started Button](\ https://developers.facebook.com/docs/messenger-platform/messenger-profile/get-started-button)
    -  [x] [Greeting Text](\ https://developers.facebook.com/docs/messenger-platform/messenger-profile/greeting-text)
    -  [x] [Domain Whitelisting](\ https://developers.facebook.com/docs/messenger-platform/messenger-profile/domain-whitelisting)
    -  [x] [Account Linking](\ https://developers.facebook.com/docs/messenger-platform/messenger-profile/account-linking-url)
    -  [x] [Payment Settings](\ https://developers.facebook.com/docs/messenger-platform/messenger-profile/payment-settings)
    -  [x] [Target Audience](\ https://developers.facebook.com/docs/messenger-platform/messenger-profile/target-audience)
    -  [x] [Chat Extension Home URL (Covering but no tested)](\ https://developers.facebook.com/docs/messenger-platform/messenger-profile/home-url)

  -  [ ] Plugin Reference
  -  [ ] Messenger Code API
  -  [ ] Messaging Insights API


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

