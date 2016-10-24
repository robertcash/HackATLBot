from flask import Flask, request, jsonify, g, Response
from db import User, Team
from helpers import send_response
from peewee import *
import bot_postbacks
import bot_messages
import uuid

def view_team_handler(user):
    team = Team.select().where(Team.team_id == user.team_id).get()
    team_members = User.select().where((User.team_id == user.team_id) & (User.user_id != user.user_id))
    data = {'code_card':team,'team_member_cards':team_members}
    return bot_postbacks.view_team_postback(data, user)

def create_team_handler(user):
    code = str(uuid.uuid4())
    team = Team.create(code=code, team_leader_id=user.user_id)
    user.team_id = team.team_id
    user.save()
    data = {'code_card':team,'team_member_cards':[]}
    return bot_postbacks.view_team_postback(data, user)

def team_code_handler(receiver, user):
    text = receiver.get_text()
    team_query = Team.select().where(Team.code == text)
    if len(team_query) > 0:
        team = team_query[0]
        user.team_id = team.team_id
        user.save()
        return team_code_ask_success_message(team.team_id, user)

    return team_code_ask_failure_message(user)


def quick_reply_handler(receiver, user):
    payload = receiver.get_quick_reply_payload()

    if payload == 'join_team':
        return bot_messages.team_ask_message(user)
    elif payload == 'view_team':
        return view_team_handler(user)
    elif payload == 'join_join_team':
        return bot_messages.team_code_ask_message(user)
    elif payload == 'create_team':
        return create_team_handler(user)
    return send_response()

def message_handler(receiver, user):
    if not user.team_id:
        if user.state == 'team_code_waiting':
            return team_code_handler(receiver, user)
        return bot_messages.team_ask_message(user)
    else:
        return view_team_handler(user)

def postback_handler(receiver, user):
    return send_response()

def request_handler(receiver, user):
    if receiver.get_request_type() == 'message':
        if receiver.get_message_type() == 'quick_reply':
            return quick_reply_handler(receiver, user)
        return message_handler(receiver, user)
    elif receiver.get_request_type() == 'postback':
        return postback_handler(receiver, user)

    return send_response()
