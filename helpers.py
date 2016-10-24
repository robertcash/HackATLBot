from flask import Flask, request, jsonify, g, Response
from datetime import datetime, timedelta
from pytz import timezone
import json

def send_response():
    response = jsonify({})
    response.status_code = 200
    return response

def get_menu_state(user):
    submitted = False
    if user.project_id:
        submitted = True
    menu_state = 'state'
    current_est_time = datetime.now() - timedelta(hours = 4)
    submission_close_time = datetime(2016, 11, 6, 10, 0)
    if user.team_id:
        menu_state = menu_state + '_vteam'
    else:
        menu_state = menu_state + '_jteam'

    if current_est_time < submission_close_time and not submitted:
        menu_state = menu_state + '_osubmission'
    else:
        menu_state = menu_state + '_csubmission'

    return menu_state
