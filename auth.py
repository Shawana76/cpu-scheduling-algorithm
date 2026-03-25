from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils import load_users, save_users

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        users = load_users()
        if not username or not password or password != confirm_password:
            flash("Invalid input or password mismatch.", "error")
            return redirect(url_for('auth.register'))
        if username in users:
            flash("Username exists.", "error")
            return redirect(url_for('auth.register'))
        users[username] = password
        save_users(users)
        flash("Registered successfully!", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        users = load_users()
        if username in users and users[username] == password:
            session['username'] = username
            session['processes'] = []
            return redirect(url_for('process.dashboard'))
        flash("Invalid credentials", "error")
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# @auth_bp.route('/dashboard')
# def dashboard():
#     if 'username' not in session:
#         return redirect(url_for('login'))
#     processes = get_processes()
#     simulation_result = session.pop('simulation_result', None)
#     return render_template('dashboard.html', processes=processes, simulation_result=simulation_result)
