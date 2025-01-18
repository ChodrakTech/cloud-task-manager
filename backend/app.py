from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

# Create the database
with app.app_context():
    db.create_all()

# Routes
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'name': task.name} for task in tasks])

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(name=data['name'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'message': 'Task added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


