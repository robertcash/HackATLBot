from db import User
from helpers import send_response, get_menu_state
from send import Message, QuickReplyMessage, QuickReply
import json

# REMINDER MESSAGE ACCESSED MANUALLY THROUGH PORTAL
def reminder_message(text, user):
    m = Message(text, user.messenger_id)
    m.send()

def welcome_message(user):
    text = 'Hi I\'m Hallie, the HackATL bot! Tell me your email you applied to HackATL with so I can set up your HackATL experience!'
    m = Message(text, user.messenger_id)
    m.send()
    return send_response()

def email_failure_message(user):
    text = 'The email you gave me does\'t match our records. Please send me the email you applied to HackATL with!'
    m = Message(text, user.messenger_id)
    m.send()
    return send_response()

def generic_error_message(user, response=True):
    text = 'I\'m sorry ' + user.first_name + ', I didn\'t quite understand that.'
    m = Message(text, user.messenger_id)
    m.send()
    if response:
        return send_response()

def menu_message(user):
    text = 'What would you like to do, '+ user.first_name + '?'
    menu_state = get_menu_state(user)
    quick_replies = []

    # Variable: Join Team and View Team
    if 'vteam' in menu_state:
        vteam_qr = QuickReply('text', title='View Team', payload='view_team')
        quick_replies.append(vteam_qr)
    else:
        jteam_qr = QuickReply('text', title='Join a Team', payload='join_team')
        quick_replies.append(jteam_qr)

    # Constants: View Schedule and View Map
    schedule_qr = QuickReply('text', title='View Schedule', payload='view_schedule')
    map_qr = QuickReply('text', title='View Map', payload='view_map')
    quick_replies.append(schedule_qr)
    quick_replies.append(map_qr)

    # Variable: Submit and View Team
    if 'osubmission' in menu_state:
        osubmission_qr = QuickReply('text', title='Submit Project', payload='submit_project')
        quick_replies.append(osubmission_qr)
    else:
        csubmission_qr = QuickReply('text', title='Check Project Status', payload='check_project')
        quick_replies.append(csubmission_qr)

    m = QuickReplyMessage(text, user.messenger_id, quick_replies)
    m.send()
    if m.get_status_code() == 200:
        user.state = 'open'
        user.save()
    return send_response()

def map_message(user):
    text = 'Here is the HackATL Map, ' + user.first_name + '.'
    m = Message(text, user.messenger_id)
    m.send()
    s3_map_pic_url = ''
    mm = MediaMessage('image', s3_map_pic_url, user.messenger_id)
    mm.send()
    if m.get_status_code() == 200:
        user.state = 'open'
        user.save()
    return send_response()

def schedule_message(user):
    text = 'Here is the HackATL Schedule, ' + user.first_name + '.'
    m = Message(text, user.messenger_id)
    m.send()
    s3_schedule_pic_url = ''
    mm = MediaMessage('image', s3_schedule_pic_url, user.messenger_id)
    mm.send()
    if m.get_status_code() == 200:
        user.state = 'open'
        user.save()
    return send_response()

def team_ask_message(user):
    text = 'Do you want to create or join a team?'
    create_qr = QuickReply('text', title='Create', payload='create_team')
    join_qr = QuickReply('text', title='Join', payload='join_join_team')
    neither_qr = QuickReply('text', title='Neither', payload='menu')
    quick_replies = [create_qr, join_qr, neither_qr]

    m = QuickReplyMessage(text, user.messenger_id, quick_replies)
    m.send()
    return send_response()

def team_code_ask_message(user):
    text = 'What\'s the code for the team you want to join?'
    never_mind_qr = QuickReply('text', title='Never Mind', payload='menu')
    quick_replies = [never_mind_qr]
    m = QuickReplyMessage(text, user.messenger_id, quick_replies)
    m.send()
    if m.get_status_code() == 200:
        user.state = 'team_code_waiting'
        user.save()
    return send_response()

def team_code_ask_success_message(team_id, user):
    text = 'You\'ve been added to Team ' + team_id +'! Have a great time at HackATL!'
    ok_qr = QuickReply('text', title='Will Do!', payload='menu')
    quick_replies = [ok_qr]
    m = QuickReplyMessage(text, user.messenger_id, quick_replies)
    m.send()
    if m.get_status_code() == 200:
        user.state = 'open'
        user.save()
    return send_response()

def team_code_ask_failure_message(user):
    text = 'I\'m sorry, but that is not a valid code!'
    ok_qr = QuickReply('text', title='Ok', payload='menu')
    try_again_qr = QuickReply('text', title='Try Again', payload='join_join_team')
    quick_replies = [try_again_qr, ok_qr]
    m = QuickReplyMessage(text, user.messenger_id, quick_replies)
    m.send()
    if m.get_status_code() == 200:
        user.state = 'open'
        user.save()
    return send_response()

def project_file_ask_message(user):
    text = 'Send me your project file in a zip (25MB limit) or send us a link to your project. I recommend you send this from your computer on Facebook.'
    never_mind_qr = QuickReply('text', title='I\'m Not Ready', payload='menu')
    quick_replies = [never_mind_qr]
    m = QuickReplyMessage(text, user.messenger_id, quick_replies)
    m.send()
    if m.get_status_code() == 200:
        user.state = 'submission_waiting'
        user.save()
    return send_response()

def project_file_success_message(user):
    text = 'Your project has been submitted! We will let you know about the first round later!'
    ok_ar = QuickReply('text', title='Ok', payload='menu')
    quick_replies = [ok_ar]
    m = QuickReplyMessage(text, user.messenger_id, quick_replies)
    m.send()
    if m.get_status_code() == 200:
        user.state = 'open'
        user.save()
    return send_response()

def project_file_failure_message(user):
    text = 'I\'m sorry, something went wrong with your submission. The file size limit is 25mb, but you can always send us a link!'
    never_mind_qr = QuickReply('text', title='Never Mind', payload='menu')
    try_again_qr = QuickReply('text', title='Try Again', payload='submit_project')
    quick_replies = [try_again_qr, never_mind_qr]
    m = QuickReplyMessage(text, user.messenger_id, quick_replies)
    m.send()
    if m.get_status_code() == 200:
        user.state = 'open'
        user.save()
    return send_response()

def project_status_message(user, text):
    ok_qr = QuickReply('text', title='Ok', payload='menu')
    quick_replies = [ok_qr]
    m = QuickReplyMessage(text, user.messenger_id, quick_replies)
    m.send()
    return send_response()
