FBBOTW: A Facebook Bot Wrapper
==============================

Python Wrapper for `Facebook Messenger`_ Bot Platform.

|MIT licensed| |PyPI| |Documentation Status| |Build Status|

This bot makes it simpler to user the *Facebook messenger bot platform*
wrapping the endpoints as functions.

| For example, this would be the normal way you probably would call the
  ``Send API`` to send a text:
| (Using ``requests`` and ``json``)

.. code:: py

      fbid = "<user fb id>"
      message = "Hello World"
      url = 'https://graph.facebook.com/v2.6/me/messages?access_token='
      url += PAGE_ACCESS_TOKEN
      header = {"Content-Type": "application/json"}
      payload = {}
      payload['recipient'] = {'id': fbid}
      payload['message'] = {'text': message} # Limit 320 chars
      data = json.dumps(payload)
      status = requests.post(url, headers=header, data=data)

Using fbbotw you would easily write

.. code:: py

    from fbbotw import fbbotw
    # ...


    fbid = "<user fb id>"
    message = "Hello World"

    fbbotw.post_text_message(fbid, message)

Install
-------

::

    pip install fbbotw

Using with Django
-----------------

| 1 - In your global settings define the variable ``PAGE_ACCESS_TOKEN``
  that is
| your access token generated on the app configuration from facebook.

.. code:: py

    #settings.py
    PAGE_ACCESS_TOKEN = "<your access token>"

or create environment variable with the same name:

.. code:: sh

    export PAGE_ACCESS_TOKEN='<your access token>'

2 - To use the functions of this wrapper do:

.. code:: py

    from fbbotw import fbbotw

    fbbotw.typing(fbid, "typing_on")

If you want to use this package without Django
----------------------------------------------

#. Download the .zip of this directory.

#. Copy the ``fbbotw`` directory to your project root.

#. Define a variable called ``PAGE_ACCESS_TOKEN`` as the page access
   token you got from facebook

#. Import the package in your module.

.. code:: py

    from fbbotw import fbbotw

    fbbotw.typing(fbid, "typing_on")

Documentation
=============

- `Read the docs <http://fbbotw.readthedocs.io/en/latest/>`_


Current wrapper covering for the `Menssenger Platform`_ (78%)
-------------------------------------------------------------

-  [x] `User profile <https://developers.facebook.com/docs/messenger-platform/user-profile>`_
-  [ ] Send API

   -  [x] Content Types

      -  [x] `Text messages <https://developers.facebook.com/docs/messenger-platform/send-api-reference/text-message>`_
      -  [x] `Audio attachment <https://developers.facebook.com/docs/messenger-platform/send-api-reference/audio-attachment>`_
      -  [x] `File attachment <https://developers.facebook.com/docs/messenger-platform/send-api-reference/file-attachment>`_
      -  [x] `Image attachment <https://developers.facebook.com/docs/messenger-platform/send-api-reference/image-attachment>`_
      -  [x] `Video attachment <https://developers.facebook.com/docs/messenger-platform/send-api-reference/video-attachment>`_

   -  [x] `Quick Replies <https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies>`_
   -  [x] `Sender Actions <https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions>`_
   -  [ ] Templates

      -  [x] `Button Template <https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template>`_
      -  [x] `Generic Template <https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template>`_
      -  [x] `List Template <https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template>`_
      -  [x] `Receipt Template <https://developers.facebook.com/docs/messenger-platform/send-api-reference/receipt-template>`_
      -  [ ] Airline Boarding Pass Template
      -  [ ] Airline Checkin Template
      -  [ ] Airline Itinerary Template
      -  [ ] Airline Flight Update Template

   -  [x] `Buttons: Check documentation to format your buttons in your templates <https://developers.facebook.com/docs/messenger-platform/send-api-reference/share-button>`_

      -  [x] `Call Button <https://developers.facebook.com/docs/messenger-platform/send-api-reference/call-button>`_

-  [ ] Thread Settings

    -  [x] `Greeting Text <https://developers.facebook.com/docs/messenger-platform/thread-settings/greeting-text>`_
    -  [x] `Get Started Button <https://developers.facebook.com/docs/messenger-platform/thread-settings/get-started-button>`_
    -  [x] `Persistent Menu <https://developers.facebook.com/docs/messenger-platform/thread-settings/persistent-menu>`_
    -  [X] `Account Linking (Available but not tested) <https://developers.facebook.com/docs/messenger-platform/thread-settings/account-linking>`_
    -  [x] `Domain Whitelisting <https://developers.facebook.com/docs/messenger-platform/thread-settings/domain-whitelisting>`_
    -  [ ] Payment Settings (BETA)


.. _Facebook Messenger: https://developers.facebook.com/products/messenger/

.. |MIT licensed| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE
.. |PyPI| image:: https://img.shields.io/pypi/v/fbbotw.svg
   :target: https://pypi.python.org/pypi?name=fbbotw&:action=display
.. |Documentation Status| image:: https://readthedocs.org/projects/fbbotw/badge/?version=latest
   :target: http://fbbotw.readthedocs.io/en/latest/?badge=latest
.. |Build Status| image:: https://travis-ci.org/JoabMendes/fbbotw.svg?branch=master
   :target: https://travis-ci.org/JoabMendes/fbbotw

.. _Menssenger Platform: https://developers.facebook.com/docs/messenger-platform/product-overview
