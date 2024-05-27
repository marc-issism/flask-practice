from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
import time
import datetime

# Create instance of the Flask class which is the WSGI application
# WSGI means Web Server Gateway Interface
app = Flask(__name__)

# initializing the DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# Create a class
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) #Nullable means you can leave it blank
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repr__(self):
        return '<Task %r>' % self.id

# Create the database
with app.app_context():
    db.create_all()

# Flask route decorators map '/' and '/hello' to the hello() function
@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        task_content = request.form['content'] # id of input that we want to get content of
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)
    
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id) # attempt to get task by id
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was an issue deleting that task"

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task_to_update = Todo.query.get_or_404(id) # attempt to get task by id

    if request.method == 'POST':
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            "AN ISSEU POCFURED"
    else:
        return render_template('update.html', task=task_to_update)

if __name__ == '__main__':
    # Run app server on localhost
    app.run(debug=True)