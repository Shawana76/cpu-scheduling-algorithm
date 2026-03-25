# CPU Scheduling Algorithm Simulator

This project is a **CPU Scheduling Algorithm Simulator** designed to help students understand and visualize different CPU scheduling techniques.  
The simulator includes the following algorithms:

- **FCFS (First-Come, First-Served)**  
- **SJF (Shortest Job First)**  
- **Round Robin (RR)**  
- **Priority Scheduling**  
  - Non-preemptive  
  - Preemptive  

---

## Features
- Interactive interface for selecting scheduling algorithms  
- Input multiple processes with **burst time** and **arrival time**  
- Automatically generates **Gantt Charts** for process scheduling  
- Calculates **Waiting Time** and **Turnaround Time** for processes  
- User-friendly and educational for students preparing for exams  

---

## How to Run

### Backend (Python/Django)
1. Clone the repository:  
   ```bash
   git clone <your-repo-link>
   cd <project-folder>

Create a virtual environment:

python -m venv venv
Activate the environment:
Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate

Install required packages:

pip install -r requirements.txt

Run Django server:

python manage.py runserver
Open in browser: http://127.0.0.1:8000/ to access the simulator
