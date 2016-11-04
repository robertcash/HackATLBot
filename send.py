# Send API script for RCFBBotTemplate
import requests

ACCESS_TOKEN = ''
SEND_API_URL = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ACCESS_TOKEN

# NORMAL MESSAGES

class Message():
    def __init__(self, text, receiver_messenger_id):
        self.text = text
        self.receiver_messenger_id = receiver_messenger_id

    # GETTERS

    def get_response(self):
        return self.response

    def get_headers(self):
        return self.headers

    def get_status_code(self):
        return self.status_code

    # CLASS FUNCTIONS

    def send(self):
        recipient = {'id':self.receiver_messenger_id}
        message = {'text':self.text}
        params = {
            'recipient':recipient,
            'message':message
        }

        r = requests.post(SEND_API_URL,json=params)
        self.response = r.json()
        self.headers = r.headers
        self.status_code = r.status_code

class MediaMessage():
    def __init__(self, media_type, url, receiver_messenger_id):
        self.type = media_type
        self.url = url
        self.receiver_messenger_id = receiver_messenger_id

    # GETTERS

    def get_response(self):
        return self.response

    def get_headers(self):
        return self.headers

    def get_status_code(self):
        return self.status_code

    # CLASS FUNCTIONS

    def send(self):
        recipient = {'id':self.receiver_messenger_id}
        url = {'url':self.url}
        attachment = {
            'type':self.type,
            'payload':url
        }
        message = {'attachment': attachment}
        params = {
            'recipient':recipient,
            'message':message
        }

        r = requests.post(SEND_API_URL,json=params)
        self.response = r.json()
        self.headers = r.headers
        self.status_code = r.status_code

class QuickReplyMessage(Message):
    def __init__(self, text, receiver_messenger_id, quick_replies):
        Message.__init__(self, text, receiver_messenger_id)
        self.quick_replies = []
        for quick_reply in quick_replies:
            self.quick_replies.append(quick_reply.request_json)

    # GETTERS

    def get_response(self):
        return self.response

    def get_headers(self):
        return self.headers

    def get_status_code(self):
        return self.status_code

    # CLASS FUNCTIONS

    def send(self):
        recipient = {'id':self.receiver_messenger_id}
        message = {
            'text':self.text,
            'quick_replies':self.quick_replies
        }
        params = {
            'recipient':recipient,
            'message':message
        }

        r = requests.post(SEND_API_URL, json=params)
        self.response = r.json()
        self.headers = r.headers
        self.status_code = r.status_code

# STRUCTURED MESSAGES

class ButtonTemplateMessage(Message):
    def __init__(self, text, buttons, receiver_messenger_id):
        Message.__init__(self, text, receiver_messenger_id)
        self.buttons = []
        for button in buttons:
            self.buttons.append(button.request_json)

    # GETTERS

    def get_response(self):
        return self.response

    def get_headers(self):
        return self.headers

    def get_status_code(self):
        return self.status_code

    # CLASS FUNCTIONS

    def send(self):
        recipient = {'id':self.receiver_messenger_id}
        payload = {
            'template_type':'button',
            'text':self.text,
            'buttons':self.buttons
        }
        attachment = {
            'type':'template',
            'payload':payload
        }
        message = {
            'attachment': attachment,
        }
        params = {
            'recipient':recipient,
            'message':message
        }

        r = requests.post(SEND_API_URL,json=params)
        self.response = r.json()
        self.headers = r.headers
        self.status_code = r.status_code

class GenericTemplateMessage():
    def __init__(self, generic_elements, receiver_messenger_id):
        self.generic_elements = []
        for generic_element in generic_elements:
            self.generic_elements.append(generic_element.request_json)
        self.receiver_messenger_id = receiver_messenger_id

    # GETTERS

    def get_response(self):
        return self.response

    def get_headers(self):
        return self.headers

    def get_status_code(self):
        return self.status_code

    # CLASS FUNCTIONS

    def send(self):
        recipient = {'id':self.receiver_messenger_id}
        payload = {
            'template_type':'generic',
            'elements':self.generic_elements
        }
        attachment = {
            'type':'template',
            'payload':payload
        }
        message = {
            'attachment': attachment
        }
        params = {
            'recipient':recipient,
            'message':message
        }

        r = requests.post(SEND_API_URL,json=params)
        self.response = r.json()
        self.headers = r.headers
        self.status_code = r.status_code

# MESSAGE OBJECTS

class GenericTemplateElement():
    def __init__(self, title, item_url, image_url, subtitle, buttons):
        self.title = title
        self.item_url = item_url
        self.image_url = image_url
        self.subtitle = subtitle
        self.buttons = []
        for button in buttons:
            self.buttons.append(button.request_json)
        if len(self.buttons) > 0:
            self.request_json = {
                'title':self.title,
                'item_url':self.item_url,
                'image_url':self.image_url,
                'subtitle':self.subtitle,
                'buttons':self.buttons
            }
        else:
            self.request_json = {
                'title':self.title,
                'item_url':self.item_url,
                'image_url':self.image_url,
                'subtitle':self.subtitle
            }

class QuickReply():
    def __init__(self, content_type, title='', payload='', image_url=''):
        self.content_type = content_type
        self.title = title
        self.payload = payload
        self.image_url = image_url
        if self.content_type == 'text':
            if self.image_url != '':
                self.request_json = {
                    'content_type':'text',
                    'title':title,
                    'payload':payload,
                    'image_url':image_url
                }
            else:
                self.request_json = {
                    'content_type':'text',
                    'title':title,
                    'payload':payload
                }
        else:
            self.request_json = {
                'content_type':'location'
            }

class Button():
    def __init__(self, title):
        self.title = title
        self.request_json = {}

class URLButton(Button):
    def __init__(self, title, url, webview_height_ratio):
        Button.__init__(self, title)
        self.url = url
        self.webview_height_ratio = webview_height_ratio
        self.request_json = {
            'type': 'web_url',
            'url':self.url,
            'title':self.title,
            'webview_height_ratio':self.webview_height_ratio
        }

class PostbackButton(Button):
    def __init__(self, title, payload):
        Button.__init__(self, title)
        self.payload = payload
        self.request_json = {
            'type':'postback',
            'title':self.title,
            'payload':self.payload
        }
