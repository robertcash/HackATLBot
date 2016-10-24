from flask import Flask, request, jsonify, g, Response
from db import User, Project
from helpers import send_response
from peewee import *
from aws_file_uploader import upload_file
import bot_postbacks
import bot_messages

def check_project_handler(user):
    project = Project.select().where(Project.proj_id == User.project_id).get()
    state = project.state
    if state == 'pre':
        text_to_send = 'Your project has been submitted, we\'ll let you know when the first round starts!'
    elif state == 'round1':
        text_to_send = 'You\'ve been assigned '+ project.assignment + '.'
    elif state == 'final':
        text_to_send = 'Congratulations! You\'ve made it to the final round! You\'ve been assigned ' + project.assignment + '.'
    else:
        # "sorry" state
        text_to_send = 'Sorry you did not make it to the final round! Thank you for participating in HackATL!'

    return bot_messages.project_status_message(user, text_to_send)

def project_submission_handler(receiver, user, type_of_sub):
    if type_of_sub == 'file':
        url = receiver.
        success = upload_file(url, user)
        if success:
            return project_file_success_message(user)
    else:
        url = receiver.get_text()
        project = Project.create(url=url, project_user_id=user.user_id, status='pre')
        if not user.team_id:
            user.project_id = project.proj_id
            user.save()
        else:
            project.team_id = user.team_id
            project.save()
            users = User.update(project_id=project.proj_id).where(User.team_id == user.team_id)
            users.execute()

        return project_file_success_message(user)

    return project_file_failure_message(user)

def attachment_handler(receiver, user):
    state = user.state

    if state == 'submission_waiting':
        return project_submission_handler(receiver, user, 'file')

    return bot_messages.generic_error_message(user)

def quick_reply_handler(receiver, user):
    payload = receiver.get_quick_reply_payload()

    if payload == 'submit_project':
        return bot_messages.project_file_ask_message(user)
    elif payload == 'check_project':
        return check_project_handler(user)

    return send_response()

def message_handler(receiver, user):
    if not user.project_id:
        if user.state == 'submission_waiting':
            return project_submission_handler(user, 'url')
        return bot_messages.submission_ask_message(user)
    else:
        return check_project_handler(user)

def postback_handler(receiver, user):
    return send_response()

def request_handler(receiver, user):
    if receiver.get_request_type() == 'message':
        if receiver.get_message_type() == 'quick_reply':
            return quick_reply_handler(receiver, user)
        elif receiver.get_message_type() == 'file':
            return attachment_handler(receiver, user)
        return message_handler(receiver, user)
    elif receiver.get_request_type() == 'postback':
        return postback_handler(receiver, user)

    return send_response()
