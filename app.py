from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime, timedelta, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
database_url = os.environ.get('DATABASE_URL')
if database_url:
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get('SECRET_KEY', 'your_secret_key')
app.permanent_session_lifetime = timedelta(weeks=999)
db = SQLAlchemy(app)


class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    priority = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    source = db.Column(db.String(30), nullable=False, default='Manual')
    external_id = db.Column(db.String(150), nullable=True, unique=True)
    subject = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(30), nullable=False, default='Pending')


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default='club_admin')
    club_name = db.Column(db.String(100), nullable=True)


class Club(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(300), nullable=True)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(800), nullable=True)
    event_date = db.Column(db.String(20), nullable=False)
    event_time = db.Column(db.String(20), nullable=True)
    venue = db.Column(db.String(150), nullable=True)
    club_name = db.Column(db.String(100), nullable=False)
    registration_url = db.Column(db.String(500), nullable=True)
    created_by = db.Column(db.String(80), nullable=False)


class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('event_id', 'user_id', name='unique_event_user'),)


with app.app_context():
    db.create_all()
    # Fixed starter clubs. A super admin can add more later.
    starter_clubs = [
        ('Coding Club', 'Technology, coding and hackathon activities.'),
        ('Atrangi Club', 'Creative, cultural and artistic activities.'),
        ('College Events', 'College-wide events, workshops and competitions.')
    ]
    for name, desc in starter_clubs:
        if not Club.query.filter_by(name=name).first():
            db.session.add(Club(name=name, description=desc))

    # Demo admin accounts. Change these before deployment.
    default_admins = [
        ('superadmin', 'super123', 'super_admin', None),
        ('codingadmin', 'coding123', 'club_admin', 'Coding Club'),
        ('atrangiadmin', 'atrangi123', 'club_admin', 'Atrangi Club'),
        ('collegeadmin', 'college123', 'club_admin', 'College Events')
    ]
    for username, password, role, club_name in default_admins:
        if not Admin.query.filter_by(username=username).first():
            db.session.add(Admin(
                username=username,
                password_hash=generate_password_hash(password),
                role=role,
                club_name=club_name
            ))
    db.session.commit()


def calculate_priority(date):
    IST = timezone(timedelta(hours=5, minutes=30))
    due_date = datetime.strptime(date, '%Y-%m-%d').date()
    current_date = datetime.now(IST).date()
    if due_date < current_date:
        return 'Date Missed'
    if due_date == current_date:
        return 'Very High'
    if current_date + timedelta(days=3) >= due_date:
        return 'High'
    if current_date + timedelta(days=7) >= due_date:
        return 'Medium'
    return 'Low'


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if 'admin_id' not in session:
            return redirect(url_for('admin_login'))
        return view(*args, **kwargs)
    return wrapped


def get_admin():
    return db.session.get(Admin, session.get('admin_id')) if session.get('admin_id') else None


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user_id', '').strip()
        if not user:
            flash('Please enter your student ID.', 'warning')
            return render_template('login.html')
        session.permanent = True
        session['user_id'] = user
        return redirect(url_for('your_tasks'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/add-task', methods=['GET', 'POST'])
@login_required
def add_tasks():
    if request.method == 'POST':
        title = request.form.get('ts', '').strip()
        date = request.form.get('dt')
        description = request.form.get('ds', '').strip()
        subject = request.form.get('subject', '').strip()
        if not title or not date:
            flash('Task and due date are required.', 'warning')
            return render_template('add_task.html')
        task = Tasks(
            title=title, date=date, description=description,
            priority=calculate_priority(date), user_id=session['user_id'],
            source='Manual', subject=subject or None
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully.', 'success')
        return redirect(url_for('your_tasks'))
    return render_template('add_task.html')


@app.route('/your-tasks', methods=['GET', 'POST'])
@login_required
def your_tasks():
    tasks = db.session.execute(
        db.select(Tasks).filter_by(user_id=session['user_id']).order_by(Tasks.date.asc())
    ).scalars().all()
    for task in tasks:
        if task.status != 'Completed':
            task.priority = calculate_priority(task.date)
    db.session.commit()
    return render_template('your_tasks.html', tasks=tasks)


@app.route('/complete-task/<int:task_id>', methods=['POST'])
@login_required
def complete_task(task_id):
    task = db.session.get(Tasks, task_id)
    if task and task.user_id == session['user_id']:
        task.status = 'Completed'
        db.session.commit()
    return redirect(url_for('your_tasks'))


@app.route('/delete-task', methods=['POST', 'GET'])
@login_required
def delete_task():
    task_id = request.args.get('task_id')
    task = db.session.get(Tasks, int(task_id)) if task_id and task_id.isdigit() else None
    if task and task.user_id == session['user_id']:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('your_tasks'))


@app.route('/sync-teams', methods=['POST'])
@login_required
def sync_teams():
    # Demo importer until Microsoft Graph access is approved.
    # This function is intentionally isolated so it can later be replaced by the real Graph API call.
    demo_assignments = [
        {
            'id': f'demo-{session["user_id"]}-oop-01',
            'title': 'OOP Assignment 3',
            'subject': 'Object Oriented Programming',
            'date': (datetime.now() + timedelta(days=3)).strftime('%Y-%m-%d'),
            'description': 'Imported from Microsoft Teams (demo). Replace with Graph API when approved.'
        },
        {
            'id': f'demo-{session["user_id"]}-cn-01',
            'title': 'CN Lab Report',
            'subject': 'Computer Networks',
            'date': (datetime.now() + timedelta(days=6)).strftime('%Y-%m-%d'),
            'description': 'Imported from Microsoft Teams (demo). Replace with Graph API when approved.'
        }
    ]
    added = 0
    for item in demo_assignments:
        existing = Tasks.query.filter_by(external_id=item['id']).first()
        if existing:
            continue
        db.session.add(Tasks(
            title=item['title'], date=item['date'], description=item['description'],
            priority=calculate_priority(item['date']), user_id=session['user_id'],
            source='Teams', external_id=item['id'], subject=item['subject']
        ))
        added += 1
    db.session.commit()
    flash(f'Teams sync complete. {added} new assignment(s) imported.', 'success')
    return redirect(url_for('your_tasks'))


@app.route('/events')
@login_required
def events():
    all_events = Event.query.order_by(Event.event_date.asc(), Event.event_time.asc()).all()
    registered_ids = {r.event_id for r in Registration.query.filter_by(user_id=session['user_id']).all()}
    return render_template('events.html', events=all_events, registered_ids=registered_ids)


@app.route('/events/<int:event_id>/register', methods=['POST'])
@login_required
def register_event(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('events'))
    existing = Registration.query.filter_by(event_id=event_id, user_id=session['user_id']).first()
    if not existing:
        db.session.add(Registration(event_id=event_id, user_id=session['user_id']))
        db.session.commit()
        flash(f'Registered for {event.title}.', 'success')
    else:
        flash('You are already registered for this event.', 'info')
    return redirect(url_for('events'))


@app.route('/my-events')
@login_required
def my_events():
    regs = Registration.query.filter_by(user_id=session['user_id']).all()
    event_ids = [r.event_id for r in regs]
    my_events_list = Event.query.filter(Event.id.in_(event_ids)).order_by(Event.event_date.asc()).all() if event_ids else []
    return render_template('my_events.html', events=my_events_list)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password_hash, password):
            session['admin_id'] = admin.id
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials.', 'danger')
    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('admin_login'))


@app.route('/admin')
@admin_required
def admin_dashboard():
    admin = get_admin()
    if admin.role == 'super_admin':
        event_list = Event.query.order_by(Event.event_date.asc()).all()
        club_list = Club.query.order_by(Club.name.asc()).all()
    else:
        event_list = Event.query.filter_by(club_name=admin.club_name).order_by(Event.event_date.asc()).all()
        club_list = Club.query.filter_by(name=admin.club_name).all()
    return render_template('admin_dashboard.html', admin=admin, events=event_list, clubs=club_list)


@app.route('/admin/events/new', methods=['GET', 'POST'])
@admin_required
def admin_create_event():
    admin = get_admin()
    if request.method == 'POST':
        club_name = request.form.get('club_name') if admin.role == 'super_admin' else admin.club_name
        title = request.form.get('title', '').strip()
        event_date = request.form.get('event_date')
        if not title or not event_date or not club_name:
            flash('Event title, date and club are required.', 'warning')
            return render_template('admin_event_form.html', admin=admin, clubs=Club.query.all(), event=None)
        event = Event(
            title=title,
            description=request.form.get('description', '').strip(),
            event_date=event_date,
            event_time=request.form.get('event_time', '').strip(),
            venue=request.form.get('venue', '').strip(),
            club_name=club_name,
            registration_url=request.form.get('registration_url', '').strip(),
            created_by=admin.username
        )
        db.session.add(event)
        db.session.commit()
        flash('Event published.', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_event_form.html', admin=admin, clubs=Club.query.all(), event=None)


@app.route('/admin/events/<int:event_id>/delete', methods=['POST'])
@admin_required
def admin_delete_event(event_id):
    admin = get_admin()
    event = db.session.get(Event, event_id)
    if event and (admin.role == 'super_admin' or event.club_name == admin.club_name):
        Registration.query.filter_by(event_id=event_id).delete()
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/events/<int:event_id>/registrations')
@admin_required
def admin_registrations(event_id):
    admin = get_admin()
    event = db.session.get(Event, event_id)
    if not event or (admin.role != 'super_admin' and event.club_name != admin.club_name):
        return redirect(url_for('admin_dashboard'))
    registrations = Registration.query.filter_by(event_id=event_id).order_by(Registration.registered_at.desc()).all()
    return render_template('admin_registrations.html', event=event, registrations=registrations, admin=admin)


@app.route('/admin/clubs/new', methods=['GET', 'POST'])
@admin_required
def admin_create_club():
    admin = get_admin()
    if admin.role != 'super_admin':
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        if name and not Club.query.filter_by(name=name).first():
            db.session.add(Club(name=name, description=description))
            db.session.commit()
            flash('Club created. You can now assign an admin to it in the database.', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Club name is empty or already exists.', 'warning')
    return render_template('admin_club_form.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
