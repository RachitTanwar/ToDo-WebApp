from flask import Flask, render_template , request ,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    desc = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
    

with app.app_context():
    db.create_all()

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/todo" , methods = ['GET','POST'])
def todo():
    if request.method == 'POST':
        title =request.form['title']
        desc =request.form['desc']
        todo = Todo(title= title, desc= desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template("todo.html" , alltodo=alltodo)

@app.route("/done/<int:sno>")
def done(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todo')

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/todo')

@app.route("/show")
def show():
    alltodo = Todo.query.all()
    print(alltodo)
    return "This is show page"

if __name__ == "__main__":
    app.run(debug=True)
