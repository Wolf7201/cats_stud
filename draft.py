from flask import Flask, jsonify, request

app = Flask(__name__)

# Эмуляция базы данных в памяти
users = [
    {"ID": 1, "Name": "Alice", "Age": 30, "Mail": "alice@example.com", "LanguageID": 3},
    {"ID": 2, "Name": "Bob", "Age": 24, "Mail": "bob@example.com", "LanguageID": 3}
]


@app.route('/rest/person', methods=['PUT'])
def create_user():
    user = request.get_json()
    users.append(user)
    return jsonify(user), 201


@app.route('/rest/people', methods=['GET'])
def list_users():
    return jsonify(users)


@app.route('/rest/person', methods=['GET'])
def read_user():
    user_id = request.args.get('id', type=int)
    user = next((u for u in users if u['ID'] == user_id), None)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/rest/person', methods=['PATCH'])
def update_user():
    user_id = request.args.get('id', type=int)
    user_data = request.get_json()
    user = next((u for u in users if u['ID'] == user_id), None)
    if user:
        user.update(user_data)
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/rest/person', methods=['DELETE'])
def delete_user():
    user_id = request.args.get('id', type=int)
    global users
    users = [u for u in users if u['ID'] != user_id]
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)
