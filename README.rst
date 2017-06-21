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

Get Started
-----------

1- Install
~~~~~~~~~~

.. code:: sh

    pip install fbbotw

2 - Configure it
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The only configuration needed is to set the ``PAGE_ACCESS_TOKEN`` with the value you got from the `facebook app dashboard`_. If you are using Django, create the variable in your ``settings.py``. If not, define the variable in your enviroment:

2.1 - Django
^^^^^^^^^^^^

In your ``settings.py`` define the variable ``PAGE_ACCESS_TOKEN`` that was generated on the app configuration from facebook.

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

See the documentation to learn about the methods provided by the package.

Documentation
=============

-  `Read the Docs`_

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

