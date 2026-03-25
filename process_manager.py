from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from simulation import simulate_sjf, simulate_srtf
import json, os


process_bp = Blueprint('process', __name__)


def get_processes():
    return session.get('processes', [])


def set_processes(processes):
    session['processes'] = processes


@process_bp.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    processes = get_processes()
    simulation_result = session.pop('simulation_result', None)
    return render_template('dashboard.html', processes=processes, simulation_result=simulation_result)


@process_bp.route('/add', methods=['POST'])
def add_process():
    processes = get_processes()
    pid = request.form['pid']
    arrival = float(request.form['arrival'])
    burst = float(request.form['burst'])
    priority = request.form.get('priority')
    priority = float(priority) if priority else None
    if any(p['pid'] == pid for p in processes):
        flash("PID already exists!", "error")
        return redirect(url_for('process.dashboard'))
    processes.append({'pid': pid, 'arrival': arrival, 'burst': burst, 'priority': priority})
    set_processes(processes)
    flash("Process added!", "success")
    return redirect(url_for('process.dashboard'))


@process_bp.route('/modify/<pid>', methods=['GET', 'POST'])
def modify_process(pid):
    processes = get_processes()
    process = next((p for p in processes if p['pid'] == pid), None)
    if not process:
        flash("Process not found.", "error")
        return redirect(url_for('process.dashboard'))
    if request.method == 'POST':
        process['pid'] = request.form['pid']
        process['arrival'] = float(request.form['arrival'])
        process['burst'] = float(request.form['burst'])
        priority = request.form.get('priority')
        process['priority'] = float(priority) if priority else None
        set_processes(processes)
        flash("Process updated.", "success")
        return redirect(url_for('process.dashboard'))
    return render_template('modify.html', process=process)


@process_bp.route('/delete/<pid>')
def delete_process(pid):
    processes = [p for p in get_processes() if p['pid'] != pid]
    set_processes(processes)
    flash("Deleted.", "success")
    return redirect(url_for('process.dashboard'))


@process_bp.route('/simulate', methods=['POST'])
def simulate():
    algorithm = request.form.get('algorithm')
    processes = get_processes()
    if algorithm == 'sjf':
        schedule, updated = simulate_sjf(processes)
    elif algorithm == 'srtf':
        schedule, updated = simulate_srtf(processes)
    else:
        flash("Unknown algorithm.", "error")
        return redirect(url_for('process.dashboard'))
    session['simulation_result'] = {
        'schedule': schedule,
        'details': updated
    }
    return redirect(url_for('process.dashboard'))


@process_bp.route('/save', methods=['POST'])
def save_processes():
    username = session['username']
    with open(f"saved_processes_{username}.json", "w") as f:
        json.dump(get_processes(), f)
    flash("Saved successfully!", "success")
    return redirect(url_for('process.dashboard'))


@process_bp.route('/load')
def load_processes():
    username = session['username']
    filename = f"saved_processes_{username}.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            set_processes(json.load(f))
        flash("Loaded successfully!", "success")
    else:
        flash("No file found.", "error")
    return redirect(url_for('process.dashboard'))
