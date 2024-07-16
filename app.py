from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from __appsignal__ import appsignal
from opentelemetry.instrumentation.flask import FlaskInstrumentor
import os

appsignal.start()

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)

# Create the database
with app.app_context():
    db.create_all()

# Endpoint to get user information
@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 200
    except Exception as e:
        app.logger.error(f"Error retrieving user: {e}")
        abort(500, description="Internal Server Error")

# Endpoint to update user information
@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        db.session.commit()
        return jsonify({'message': 'User updated', 'user': {'id': user.id, 'name': user.name, 'email': user.email}}), 200
    except Exception as e:
        app.logger.error(f"Error updating user: {e}")
        abort(500, description="Internal Server Error")

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)