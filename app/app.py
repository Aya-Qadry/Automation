from flask import Flask
from routes import routes
from gmail_trigger import setup_email_watcher

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == '__main__':
    setup_email_watcher()
    app.run(debug=True)