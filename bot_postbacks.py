from __future__ import print_function # In python 2.7
import sys
from db import User
from datetime import datetime
from helpers import send_response
from send import ButtonTemplateMessage, GenericTemplateMessage, GenericTemplateElement, PostbackButton, URLButton
import json
import uuid
import bot_messages

def view_team_postback(data, user):
    generic_elements = []
    code_card = data['code_card']
    team_member_cards = data['team_member_cards']
    title = 'Team ' + str(code_card.team_id)
    subtitle = 'Share this team code with team members: ' + code_card.code + '.'
    generic_element = GenericTemplateElement(title, '', 'https://scontent-atl3-1.xx.fbcdn.net/v/t1.0-9/14370071_1148653078547237_8830242123671034694_n.jpg?oh=b33cb0924d4812dd24ea203e7f5ff6a9&oe=58A01F5E', subtitle, [])
    generic_elements.append(generic_element)

    for team_member_card in team_member_cards:
        title = team_member_card.first_name + ' ' + team_member_card.last_name
        subtitle = team_member_card.email
        generic_element = GenericTemplateElement(title, '', 'http://gazettereview.com/wp-content/uploads/2016/03/facebook-avatar.jpg', subtitle, [])
        generic_elements.append(generic_element)

    m = GenericTemplateMessage(generic_elements, user.messenger_id)
    m.send()
    print(str(m.get_response()) + user.messenger_id, file=sys.stderr)

    return bot_messages.anything_else_message(user)
