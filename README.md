# FBBOTW: A Facebook Bot Wrapper
Python Wrapper for [Facebook Messenger](https://developers.facebook.com/products/messenger/) Bot Platform.

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE) [![PyPI](https://img.shields.io/pypi/v/fbbotw.svg)](https://pypi.python.org/pypi?name=fbbotw&:action=display) [![Documentation Status](https://readthedocs.org/projects/fbbotw/badge/?version=latest)](http://fbbotw.readthedocs.io) [![Build Status](https://travis-ci.org/JoabMendes/fbbotw.svg?branch=master)](https://travis-ci.org/JoabMendes/fbbotw)

This bot makes it simpler to user the *Facebook messenger bot platform*  wrapping the endpoints as functions.

For example, this would be the normal way you probably would call the `Send API` to send a text:
(Using `requests` and `json`)

```py
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
```

Using fbbotw you would easily write

```py
from fbbotw import fbbotw
# ...


fbid = "<user fb id>"
message = "Hello World"

fbbotw.post_text_message(fbid, message)

```

## Install

```
pip install fbbotw
```

## Using with Django

1 - In your global settings define the variable `PAGE_ACCESS_TOKEN` that is
your access token generated on the app configuration from facebook.

```py
#settings.py
PAGE_ACCESS_TOKEN = "<your access token>"
```

or create environment variable with the same name:

```sh
export PAGE_ACCESS_TOKEN='<your access token>'
```

2 - To use the functions of this wrapper do:

```py
from fbbotw import fbbotw

fbbotw.typing(fbid, "typing_on")

```

## If you want to use this package without Django

1. Download the .zip of this directory.

2. Copy the `fbbotw` directory to your project root.

3. Define a variable called `PAGE_ACCESS_TOKEN` as the page access token you got from facebook

4. Import the package in your module.

```py
from fbbotw import fbbotw

fbbotw.typing(fbid, "typing_on")
```

# Documentation

- [Read the Docs](http://fbbotw.readthedocs.io/en/latest/)

# Current wrapper covering for the [Menssenger Platform](https://developers.facebook.com/docs/messenger-platform/product-overview) (78%)

- [x] [User profile](https://developers.facebook.com/docs/messenger-platform/user-profile)
- [ ] Send API
    - [x] Content Types
        - [x] [Text messages](https://developers.facebook.com/docs/messenger-platform/send-api-reference/text-message)
        - [x] [Audio attachment](https://developers.facebook.com/docs/messenger-platform/send-api-reference/audio-attachment)
        - [x] [File attachment](https://developers.facebook.com/docs/messenger-platform/send-api-reference/file-attachment)
        - [x] [Image attachment](https://developers.facebook.com/docs/messenger-platform/send-api-reference/image-attachment)
        - [x] [Video attachment](https://developers.facebook.com/docs/messenger-platform/send-api-reference/video-attachment)
    - [x] [Quick Replies](https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies)
    - [x] [Sender Actions](https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions)
    - [ ] Templates
        - [x] [Button Template](https://developers.facebook.com/docs/messenger-platform/send-api-reference/button-template)
        - [x] [Generic Template](https://developers.facebook.com/docs/messenger-platform/send-api-reference/generic-template)
        - [x] [List Template](https://developers.facebook.com/docs/messenger-platform/send-api-reference/list-template)
        - [x] [Receipt Template](https://developers.facebook.com/docs/messenger-platform/send-api-reference/receipt-template)
        - [ ] Airline Boarding Pass Template
        - [ ] Airline Checkin Template
        - [ ] Airline Itinerary Template
        - [ ] Airline Flight Update Template
    - [x] [Buttons: Check documentation to format your buttons in your templates](https://developers.facebook.com/docs/messenger-platform/send-api-reference/share-button)
        - [x] [Call Button](https://developers.facebook.com/docs/messenger-platform/send-api-reference/call-button)
- [ ] Thread Settings
  - [x] [Greeting Text](https://developers.facebook.com/docs/messenger-platform/thread-settings/greeting-text)
  - [x] [Get Started Button](https://developers.facebook.com/docs/messenger-platform/thread-settings/get-started-button)
  - [x] [Persistent Menu](https://developers.facebook.com/docs/messenger-platform/thread-settings/persistent-menu)
  - [X] [Account Linking (Available but not tested)](https://developers.facebook.com/docs/messenger-platform/thread-settings/account-linking)
  - [x] [Domain Whitelisting](https://developers.facebook.com/docs/messenger-platform/thread-settings/domain-whitelisting)
  - [ ] Payment Settings (BETA)
