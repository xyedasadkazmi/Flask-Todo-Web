from flask import Flask, render_template, redirect, url_for, flash, session, request, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from forms import RegisterForm, LoginForm, TaskForm
import os
import models  # 👈 import models directly

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET', 'dev-secret-key-change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database with app
models.db.init_app(app)
User = models.User
Task = models.Task


def current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    return User.query.get(user_id)


@app.route('/', methods=['GET', 'POST'])
def home():
    if current_user():
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            session['user_name'] = user.name
            flash('Logged in successfully.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('home.html', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user():
        return redirect(url_for('dashboard'))
    form = RegisterForm()
    if form.validate_on_submit():
        existing = User.query.filter_by(email=form.email.data).first()
        if existing:
            flash('Email already registered.', 'warning')
            return redirect(url_for('register'))
        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        # ✅ Use models.db instead of db
        models.db.session.add(user)
        models.db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out.', 'info')
    return redirect(url_for('home'))


@app.route('/dashboard')
def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for('home'))

    f = request.args.get('filter', 'active')
    if f == 'active':
        tasks = Task.query.filter_by(user_id=user.id, is_completed=False).order_by(Task.due_date.asc().nulls_last(), Task.priority.desc()).all()
    elif f == 'inactive':
        tasks = Task.query.filter_by(user_id=user.id, is_completed=True).order_by(Task.updated_at.desc()).all()
    else:
        tasks = Task.query.filter_by(user_id=user.id).order_by(Task.is_completed, Task.due_date.asc().nulls_last()).all()
    return render_template('dashboard.html', tasks=tasks, filter=f, user=user)


@app.route('/task/add', methods=['GET', 'POST'])
def add_task():
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    form = TaskForm()
    if form.validate_on_submit():
        due = form.due_date.data
        reminder = form.reminder.data
        task = Task(
            title=form.title.data,
            description=form.description.data,
            due_date=due,
            priority=form.priority.data,
            category=form.category.data or None,
            reminder=reminder or None,
            user_id=user.id,
            is_completed=False
        )
        models.db.session.add(task)
        models.db.session.commit()
        flash('Task added.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('task_form.html', form=form, action='Add Task')


@app.route('/task/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    task = Task.query.get_or_404(task_id)
    if task.user_id != user.id:
        abort(403)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.due_date = form.due_date.data
        task.priority = form.priority.data
        task.category = form.category.data or None
        task.reminder = form.reminder.data or None
        task.updated_at = datetime.utcnow()
        models.db.session.commit()
        flash('Task updated.', 'success')
        return redirect(url_for('dashboard'))
    return render_template('task_form.html', form=form, action='Edit Task')


@app.route('/task/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    task = Task.query.get_or_404(task_id)
    if task.user_id != user.id:
        abort(403)
    models.db.session.delete(task)
    models.db.session.commit()
    flash('Task deleted.', 'info')
    return redirect(url_for('dashboard'))


@app.route('/task/toggle/<int:task_id>', methods=['POST'])
def toggle_task(task_id):
    user = current_user()
    if not user:
        return redirect(url_for('home'))
    task = Task.query.get_or_404(task_id)
    if task.user_id != user.id:
        abort(403)
    task.is_completed = not task.is_completed
    task.updated_at = datetime.utcnow()
    models.db.session.commit()
    state = 'completed' if task.is_completed else 'marked active'
    flash(f'Task {state}.', 'success')
    return redirect(url_for('dashboard', filter=('inactive' if task.is_completed else 'active')))


if __name__ == '__main__':
    if not os.path.exists('todo.db'):
        with app.app_context():
            models.db.create_all()  
            print('Database created.')
    app.run(debug=True)
