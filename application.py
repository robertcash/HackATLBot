from flask import Flask, request, jsonify, g, Response, render_template
from peewee import *
import bot
import db
import reminder_system

# Elastic Beanstalk initalization
application = Flask(__name__)
database = db.database

# Request handling
@application.before_request
def before_request():
    database.connect()

@application.after_request
def after_request(response):
    database.close()
    return response

# Routes

@application.route('/')
def hello_world():
    return 'Hello world! Nothing is broken!'

@application.route('/reminders', methods=['GET', 'POST'])
def reminders():
    return reminder_system.reminders_handler()

@application.route('/sendreminders', methods=['POST'])
def send_reminders():
    return reminder_system.send_reminders_handler(request)

# Webhook route for Messenger

@application.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Here webhook is verified with Facebook Messenger.
        if request.args.get('hub.verify_token') == 'bigbootycameron':
            return Response(request.args.get('hub.challenge'))
        else:
            return Response('Wrong validation token')
    else:
        # Here messages are received, code for this is handled in bot.py.
        return bot.response_handler(request.get_json())

if __name__ == '__main__':
    application.run(host='0.0.0.0',port = 8080, debug = True)
