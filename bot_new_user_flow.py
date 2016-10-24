from flask import Flask, request, jsonify, g, Response
from db import User, Participant
from helpers import send_response
from peewee import *
import bot_postbacks
import bot_messages

def email_handler(text, user):
    try:
        participant = Participant.select().where(Participant.email == text).get()
        user.email = participant.email
        user.first_name = participant.first_name
        user.last_name = participant.last_name
        user.new_user = False
        user.state = 'open'
        user.save()
        return bot_message.menu_message(user)
    except:
        return bot_message.email_failure_message(user)

def message_handler(receiver, user):
    text = receiver.get_text()
    state = user.state
    if state == 'sign_up':
        return bot_messages.welcome_message(user)
    if state == 'sign_up_email_waiting':
        return email_handler(text, user)
    return send_response()

def postback_handler(receiver, user):
    return send_response()

def request_handler(receiver, user):
    if receiver.get_request_type() == 'message':
        return message_handler(receiver, user)
    elif receiver.get_request_type() == 'postback':
        return postback_handler(receiver, user)

    return send_response()
