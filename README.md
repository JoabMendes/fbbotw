# Facebook bot python wrapper
Python Wrapper for [Facebook Messenger](https://developers.facebook.com/products/messenger/) Bot Platform.

[![MIT licensed](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/hyperium/hyper/master/LICENSE) [![PyPI](https://img.shields.io/pypi/v/fbbotw.svg)](https://pypi.python.org/pypi?name=fbbotw&version=0.1.dev1&:action=display) [![Documentation Status](https://readthedocs.org/projects/fbbotw/badge/?version=latest)](http://fbbotw.readthedocs.io/en/latest/?badge=latest) [![Build Status](https://travis-ci.org/JoabMendes/fbbotw.svg?branch=master)](https://travis-ci.org/JoabMendes/fbbotw)

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


# Current wrapper covering for the [Menssenger Platform](https://developers.facebook.com/docs/messenger-platform/product-overview) (45%)

- [x] User profile
- [ ] Send API
  - [ ] Templates
  - [ ] Buttons
  - [x] Quick Replies
  - [x] Sender Actions
  - [ ] Content Types
    - [x] Text messages
    - [ ] Audio attachment
    - [ ] File attachment
    - [x] Image attachment
    - [ ] Video attachment
- [ ] Web view
- [ ] Thread Settings
  - [x] Greeting Text
  - [x] Get Started Button
  - [x] Persistent Menu
  - [ ] Account Linking
  - [ ] Domain Whitelisting
  - [ ] Payment Settings


# Available functions (+facebook documentation):

- **post_settings(welcometext):**  Sets the START button and welcome text
  - https://developers.facebook.com/docs/messenger-platform/thread-settings/greeting-text
  - https://developers.facebook.com/docs/messenger-platform/thread-settings/get-started-button

- **typing(fbid, sender_action):** Displays the typing gif on facebook chat
  - sender_action: "typing_on", "typing_off"
  - https://developers.facebook.com/docs/messenger-platform/send-api-reference/sender-actions

- **get_user_information(fbid):** Gets user information: first_name, last_name, gender, profile_pic.
  - https://developers.facebook.com/docs/messenger-platform/user-profile

- **post_text_message(fbid, message):** Sends a common text message
  - https://developers.facebook.com/docs/messenger-platform/send-api-reference

- **post_image_attch(fbid, imgurl):** ''' Sends an image attachment. '''
  - https://developers.facebook.com/docs/messenger-platform/send-api-reference/image-attachment

- **post_text_w_quickreplies(fbid, message, quick_replies):** Sends text with quick replies buttons
  - quick_replies format:
  ```
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
  ```
  - https://developers.facebook.com/docs/messenger-platform/send-api-reference/quick-replies
