import os

from dotenv import load_dotenv
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap5(app)


# Create base Model
class Base(DeclarativeBase):
    pass


# Load env variables
load_dotenv()

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Create Task table
class Task(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    status: Mapped[bool] = mapped_column(Boolean, default=False)


with app.app_context():
    db.create_all()


# Form to adding new tasks
class TaskForm(FlaskForm):
    task = StringField("Add new task ", validators=[DataRequired()])
    submit = SubmitField('Add')

    # Clear field after clicking submit
    def clear(self):
        self.task = ""


def get_all():
    """
    Get all tasks in database
    :return: list of tasks
    """
    all_tasks = db.session.execute(db.select(Task).order_by(Task.id),
                                   execution_options={"prebuffer_rows": True}).scalars()
    tasks = []
    for task in all_tasks:
        dict_task = {"id": task.id, "task": task.task, "status": task.status}
        tasks.append(dict_task)
    return tasks


@app.route("/", methods=["GET", "POST"])
def home():
    """
    Render index page
    """
    form = TaskForm()
    form.task = ""
    if request.method == "POST":
        new_task = Task(task=request.form.get("task"))
        with app.app_context():
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("index.html", form=form, tasks=get_all())


@app.route("/update/<task_id>", methods=["GET", "POST"])
def update_status(task_id):
    """
    Update an existing task
    :param task_id: ID of the task in the database
    """
    with app.app_context():
        task_to_update = db.get_or_404(Task, task_id)
        task_to_update.status = True
        db.session.commit()
    return redirect(url_for("home"))


@app.route("/del")
def clear_all():
    """
    Clear the task list
    """
    with app.app_context():
        db.session.query(Task).delete()
        db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
