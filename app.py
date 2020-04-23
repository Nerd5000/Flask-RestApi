from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id


@app.route('/create', methods=['POST'])
def create():
    jsonData = request.json
    try:
        user = User(username=jsonData['username'], email=jsonData['email'])
        db.session.add(user)
        db.session.commit()
        return 'created'
    except:
        return 'Error Has Occurd Check json'


@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    user = User.query.get_or_404(id)

    user.username = request.json['username']
    user.email = request.json['email']

    try:
        db.session.commit()
        return 'Updated'
    except:
        return 'There was an issue updating user'


@app.route('/read', methods=['GET'])
def read():
    users = User.query.all()
    if len(users) > 0:
        userList = []
        for user in users:
            userList.append({'username': user.username, 'email': user.email})
        return jsonify(userList)
    else:
        return 'their\'s no users'


@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    taskToDelete = User.query.get_or_404(id)

    try:
        db.session.delete(taskToDelete)
        db.session.commit()
        return 'Deleted'
    except:
        return 'There was a problem deleting that User'


if __name__ == "__main__":
    app.run(debug=True)
