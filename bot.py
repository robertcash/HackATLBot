from flask import Flask, request, jsonify, g, Response
from db import User
from helpers import send_response
from peewee import *
from receive import Receiver
import json
import bot_messages
import bot_new_user_flow
import bot_project_flow
import bot_team_flow

def get_user(sender_messenger_id):
    try:
        user = User.select().where(User.messenger_id == sender_messenger_id).get()
        return user
    except:
        user = User.create(messenger_id=sender_messenger_id, new_user=True, state='sign_up')
        return user

def parser(receiver, user):
    if receiver.get_request_type() == 'message' and receiver.get_message_type() == 'message':
        text = receiver.get_text().lower()
        if 'help' in text or 'menu' in text:
            return bot_messages.menu_message(user)
        elif 'when' in text or 'schedule' in text:
            return bot_messages.schedule_message(user)
        elif 'where' in text or 'map' in text:
            return bot_messages.map_message(user)
        elif 'project' in text or 'submit' in text or 'results' in text:
            return bot_project_flow.request_handler(receiver, user)
        elif 'team' in text:
            return bot_team_flow.request_handler(receiver, user)
        elif 'hi' in text or 'hey' in text or 'hello' in text or 'yo' in text:
            return bot_messages.greeting_message(user)
        else:
            bot_messages.generic_error_message(user, False)
            return bot_messages.menu_message(user)
    else:
        return send_response()

def payload_parser(payload, user):
    if payload == 'menu':
        return bot_messages.menu_message(user)
    elif payload == 'view_schedule':
        return bot_messages.schedule_message(user)
    elif payload == 'view_map':
        return bot_messages.map_message(user)

def qr_payload_parser(payload, receiver, user):
    if payload == 'view_schedule':
        return bot_messages.schedule_message(user)
    elif payload == 'view_map':
        return bot_messages.map_message(user)
    elif payload == 'menu':
        return bot_messages.menu_message(user)
    elif 'team' in payload:
        return bot_team_flow.request_handler(receiver, user)
    elif 'project' in payload:
        return bot_project_flow.request_handler(receiver, user)

def response_handler(request):
    try:
        # Receive request
        receiver = Receiver(request)

        # Get user
        user = get_user(receiver.get_sender_messenger_id())

        # Check postbacks
        if receiver.get_request_type() == 'postback':
            payload = receiver.get_payload()
            return payload_parser(payload, user)
        elif receiver.get_request_type() == 'message' and receiver.get_message_type() == 'quick_reply':
            qr_payload = receiver.get_quick_reply_payload()
            return qr_payload_parser(qr_payload, receiver, user)

        # Check states for message requests
        if user.new_user:
            return bot_new_user_flow.request_handler(receiver, user)
        elif user.state == 'open':
            return parser(receiver, user)
        elif user.state == 'team_code_waiting':
            return bot_team_flow.request_handler(receiver, user)
        elif user.state == 'submission_waiting':
            return bot_project_flow.request_handler(receiver, user)
        return bot_messages.generic_error_message(user)

    except:
        return send_response()
