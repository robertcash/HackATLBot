from db import User
from datetime import datetime
from helpers import send_response
from send import ButtonTemplateMessage, GenericTemplateMessage, GenericTemplateElement, PostbackButton, URLButton
import json
import uuid

def view_team_postback(data, user):
    generic_elements = []
    code_card = data['code_card']
    team_member_cards = data['team_member_cards']
    title = 'Team ' + code_card.team_id
    subtitle = 'Share this team code to team members: ' + code_card.code + '.'
    generic_element = GenericTemplateElement(title, '', '', subtitle, [])
    generic_elements.append(generic_element)

    for team_member_card in team_member_cards:
        title = team_member_card.first_name + ' ' + team_member_card.last_name
        subtitle = team_member_card.email
        generic_element = GenericTemplateElement(title, '', '', subtitle, [])
        generic_elements.append(generic_element)

    m = GenericTemplateMessage(generic_elements, user.messenger_id)
    m.send()

    return send_response()
