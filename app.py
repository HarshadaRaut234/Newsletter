from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Subscriber(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f"<Subscriber {self.email}>"

# Creates the table if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return send_file('webpage.html')

@app.route('/update_subscription', methods=['POST'])
def update_subscription():
    data = request.get_json()
    email = data.get("email")
    action = data.get("action")

    if not email or not action:
        return jsonify({"message": "Missing email or action"}), 400

    subscriber = Subscriber.query.filter_by(email=email).first()

    if action == 'subscribe':
        if not subscriber:
            new_subscriber = Subscriber(email=email)
            db.session.add(new_subscriber)
            db.session.commit()
            message = 'Subscribed successfully!'
        else:
            message = 'You are already subscribed.'
    elif action == 'unsubscribe':
        if subscriber:
            db.session.delete(subscriber)
            db.session.commit()
            message = 'Unsubscribed successfully.'
        else:
            message = 'Email not found in the list.'

    return jsonify({"message": message})

if __name__ == '__main__':
    app.run(debug=True)
