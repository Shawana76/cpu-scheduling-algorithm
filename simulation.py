import json
import os
import copy
def simulate_sjf(processes):
    """
    Non-preemptive Shortest Job First simulation.
    This version uses a different internal structure but produces the same output.
    """
    proc_list = copy.deepcopy(processes)
    schedule = []
    completed = []
    time = 0

    while proc_list:
        # Get processes that have arrived by the current time.
        available = [p for p in proc_list if p['arrival'] <= time]
        if not available:
            # If none are available, jump time forward to the next arrival.
            time = min(p['arrival'] for p in proc_list)
            available = [p for p in proc_list if p['arrival'] <= time]
        # Select the process with the minimum burst time.
        current = min(available, key=lambda p: p['burst'])
        start = time
        finish = time + current['burst']
        # Update process metrics.
        current['completion'] = finish
        current['turnaround'] = finish - current['arrival']
        current['waiting'] = current['turnaround'] - current['burst']
        schedule.append({'pid': current['pid'], 'start': start, 'finish': finish})
        completed.append(current)
        proc_list.remove(current)
        time = finish  #2=2

    return schedule, completed

def simulate_srtf(processes):
    """
    Preemptive Shortest Remaining Time First simulation.
    The internal logic is refactored but the displayed output remains identical.
    """
    proc_list = copy.deepcopy(processes)
    # Initialize remaining times for each process.
    for p in proc_list:
        p['remaining'] = p['burst']
    schedule = []
    time = 0
    current_pid = None
    segment_start = None

    while True:
        # Get all processes that have arrived and still need CPU time.
        ready = [p for p in proc_list if p['arrival'] <= time and p['remaining'] > 0]
        if not ready:
            # End simulation if all processes are finished.
            if all(p['remaining'] <= 0 for p in proc_list):
                break
            time += 1
            continue

        # Choose the process with the smallest remaining burst.
        next_proc = min(ready, key=lambda p: p['remaining'])
        if current_pid != next_proc['pid']:
            if current_pid is not None:
                schedule.append({'pid': current_pid, 'start': segment_start, 'finish': time})
            current_pid = next_proc['pid']
            segment_start = time
        # Run the chosen process for one time unit.
        next_proc['remaining'] -= 1
        time += 1
        if next_proc['remaining'] == 0:
            next_proc['completion'] = time
            next_proc['turnaround'] = time - next_proc['arrival']
            next_proc['waiting'] = next_proc['turnaround'] - next_proc['burst']

    if current_pid is not None:
        schedule.append({'pid': current_pid, 'start': segment_start, 'finish': time})

    # Merge consecutive segments for the same process.
    merged_schedule = []
    for seg in schedule:
        if merged_schedule and merged_schedule[-1]['pid'] == seg['pid'] and merged_schedule[-1]['finish'] == seg['start']:
            merged_schedule[-1]['finish'] = seg['finish']
        else:
            merged_schedule.append(seg)
    return merged_schedule, proc_list
