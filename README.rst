Facebook bot python wrapper
===========================

Python Wrapper for `Facebook Messenger`_ Bot Platform.

|MIT licensed| |PyPI| |Documentation Status|

This bot makes it simpler to user the *Facebook messenger bot platform*
wrapping the endpoints as functions. For example, this would be the
normal way you probably would call the Send API to send a text: (Using
``requests`` and ``json``)

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

1 - In your global settings define the variable ``PAGE_ACCESS_TOKEN``
that is your access token generated on the app configuration from
facebook.

.. code:: py

    #settings.py
    PAGE_ACCESS_TOKEN = "<your access token>"

2 - To use the functions of this wrapper do:

.. code:: py

    from fbbotw import fbbotw

    fbbotw.typing(fbid, "typing_on"):

If you want to use this package without Django
----------------------------------------------

1. Download the .zip of this directory.

2. Copy the ``fbbotw`` directory to your project root.

3. Change the variable ``PAGE_ACCESS_TOKEN`` at the line 9 in
   ``fbbotw/fbbotw.py`` adding your facebook page access token:

.. code:: py

        PAGE_ACCESS_TOKEN = "<Set the page access token here>"

Current wrapper covering for the `Menssenger Platform`_ (45%)
=============================================================

-  [x] User profile (Needs update)
-  [ ] Send API
-  [ ] Templates
-  [ ] Buttons
-  [x] Quick Replies
-  [x] Sender Actions
-  [ ] Content Types

   -  [x] Text messages
   -  [ ] Audio attachment
   -  [ ] File attachment
   -  [x] Image attachment
   -  [ ] Video attachment

-  [ ] Web view
-  [ ] Thread Settings
-  [x] Greeting Text
-  [x] Get Started Button
-  [x] Persistent Menu
-  [ ] Account Linking
-  [ ] Domain Whitelisting
-  [ ] Payment Settings

.. _Facebook Messenger: https://developers.facebook.com/products/messenger/
.. _Menssenger Platform: https://developers.facebook.com/docs/messenger-platform/product-overview

.. |MIT licensed| image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE
.. |PyPI| image:: https://img.shields.io/pypi/v/fbbotw.svg
   :target: https://pypi.python.org/pypi?name=fbbotw&version=0.1.dev1&:action=display
.. |Documentation Status| image:: https://readthedocs.org/projects/fbbotw/badge/?version=latest
   :target: http://fbbotw.readthedocs.io/en/latest/?badge=latest
