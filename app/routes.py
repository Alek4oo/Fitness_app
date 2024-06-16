from flask import request, jsonify, current_app as app
from .models import db, User

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or not 'username' in data or not 'email' in data or not 'password' in data:
        return jsonify({'message': 'Bad request'}), 400

    new_user = User(username=data['username'], email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201