from flask import Flask, request, jsonify, g, Response, render_template
from peewee import *
from db import User
import bot_messages

def reminders_handler():
    return render_template('reminders.html')

def send_reminders_handler(request):
    text = request.form['rtext']

    users = User.select().where(User.new_user == False)

    for user in users:
        bot_messages.reminder_message(text, user)

    return render_template('sendreminders.html')
