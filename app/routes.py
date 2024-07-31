from flask import Blueprint, jsonify
from gmail_trigger import watch_emails

routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return "Email Watcher is running!"

@routes.route('/check_emails')
def check_emails():
    watch_emails()
    return jsonify({"message": "Email check initiated. Check console for results."}), 200