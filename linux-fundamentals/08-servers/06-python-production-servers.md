# Python Web Applications and Gunicorn

## Introduction

The server learning material introduced a Python Flask application and demonstrated the difference between running the Flask development server and using a production WSGI server such as Gunicorn.

The practical lab covered:

- Creating a Flask application
- Creating a Python virtual environment
- Installing dependencies with `pip`
- Using `requirements.txt`
- Running the Flask development server
- Inspecting its process and listening socket
- Installing and running Gunicorn
- Running multiple Gunicorn workers
- Inspecting Gunicorn processes
- Understanding `127.0.0.1` versus `0.0.0.0` binding

---

# Project Structure

The Flask application was created under:

```text
~/server-lab/flask-app
```

The source project contained:

```text
flask-app/
├── main.py
└── requirements.txt
```

A Python virtual environment was also created during the practical lab:

```text
venv/
```

The virtual environment is not stored in Git because it can be recreated from the dependency file.

The Git lab therefore contains:

```text
lab/flask-app/
├── main.py
└── requirements.txt
```

---

# Flask Application

The application in `main.py` was:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Somto's Flask Server Lab"

@app.route("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

The application provides two routes:

```text
/
```

and:

```text
/health
```

---

# Root Route

The root route is:

```python
@app.route("/")
def home():
    return "Somto's Flask Server Lab"
```

A request to:

```text
/
```

returns:

```text
Somto's Flask Server Lab
```

---

# Health Route

The health endpoint is:

```python
@app.route("/health")
def health():
    return {"status": "healthy"}
```

A request to:

```text
/health
```

returns:

```json
{"status":"healthy"}
```

This endpoint was useful throughout the lab because it provided a simple way to verify that the application was responding correctly.

---

# Creating a Python Virtual Environment

I created a virtual environment using:

```bash
python3 -m venv venv
```

Then activated it:

```bash
source venv/bin/activate
```

I verified which Python interpreter was active:

```bash
which python
```

The result pointed to:

```text
/home/somto/server-lab/flask-app/venv/bin/python
```

This confirmed that the shell was using the Python interpreter inside the project's virtual environment.

---

# Why Use a Virtual Environment?

A virtual environment isolates Python packages for a project.

Conceptually:

```text
System Python
     |
     +----------------------+
                            |
                            v
                     Project venv
                            |
                 +----------+----------+
                 |                     |
                 v                     v
               Flask                Gunicorn
```

This avoids relying on globally installed Python packages for the application.

---

# requirements.txt

The learning material demonstrated:

```bash
pip install -r requirements.txt
```

The practical project now records:

```text
Flask==3.1.3
gunicorn==26.2.0
```

in:

```text
requirements.txt
```

These were the versions installed and used during the lab.

The dependencies can therefore be installed with:

```bash
pip install -r requirements.txt
```

---

# Installing Flask Dependencies

After activating the virtual environment, I ran:

```bash
pip install -r requirements.txt
```

I verified Flask with:

```bash
flask --version
```

The environment reported:

```text
Python 3.14.4
Flask 3.1.3
Werkzeug 3.1.9
```

---

# Running the Flask Development Server

I started the application with:

```bash
python main.py
```

Flask reported:

```text
* Serving Flask app 'main'
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://172.23.210.163:5000
```

The warning is important.

The Flask server being used here is intended for development rather than production deployment.

The learning material therefore introduced production server options, including Gunicorn.

---

# Verifying the Flask Listening Socket

While Flask was running, I inspected port 5000:

```bash
sudo ss -lntp | grep ':5000'
```

The output showed the Python process listening on:

```text
0.0.0.0:5000
```

This matched the application configuration:

```python
app.run(host="0.0.0.0", port=5000)
```

---

# Testing the Flask Application

I tested the health endpoint:

```bash
curl http://localhost:5000/health
```

The application returned:

```json
{"status":"healthy"}
```

This established:

```text
Python process running
        |
        v
Port 5000 listening
        |
        v
Flask application responding
        |
        v
/health returns healthy
```

---

# Stopping the Development Server

The Flask development server was running in the foreground.

I stopped it with:

```text
Ctrl+C
```

After stopping it, I checked port 5000 again.

There was no listener.

This connected the foreground process directly with the network socket:

```text
python main.py running
        |
        v
port 5000 listening

Ctrl+C
        |
        v
process stops
        |
        v
port 5000 no longer listening
```

---

# Gunicorn

The learning material introduced Gunicorn as one of the production deployment options for Python web applications.

Before installing it, I checked:

```bash
gunicorn --version
```

The command was not found.

Trying:

```bash
sudo gunicorn --version
```

also did not make the command available.

This demonstrated an important principle:

```text
sudo does not install a missing command
```

If a program is not installed, running the same missing command with elevated privileges does not solve that problem.

---

# Installing Gunicorn

Gunicorn was installed inside the project's active virtual environment:

```bash
pip install gunicorn
```

I then checked:

```bash
which gunicorn
```

The result pointed to:

```text
/home/somto/server-lab/flask-app/venv/bin/gunicorn
```

This confirmed that Gunicorn belonged to the project's virtual environment.

---

# Understanding main:app

The Flask application was started with Gunicorn using:

```bash
gunicorn main:app
```

The expression:

```text
main:app
```

identifies the application object Gunicorn should load.

In this project:

```text
main
```

refers to:

```text
main.py
```

and:

```text
app
```

refers to:

```python
app = Flask(__name__)
```

Conceptually:

```text
main:app
  |    |
  |    +--> Flask application object
  |
  +-------> Python module main.py
```

---

# Running Gunicorn

I started:

```bash
gunicorn main:app
```

Gunicorn reported:

```text
Starting gunicorn 26.2.0
Listening at: http://127.0.0.1:8000
Using worker: sync
Booting worker with pid: 23173
```

The Gunicorn master process had PID:

```text
23172
```

and the worker had PID:

```text
23173
```

---

# Gunicorn Default Binding

Unlike the Flask application configuration that used:

```text
0.0.0.0:5000
```

the Gunicorn command:

```bash
gunicorn main:app
```

listened by default on:

```text
127.0.0.1:8000
```

This means that the default Gunicorn listener used the loopback interface.

---

# Gunicorn Master and Worker

I inspected Gunicorn with:

```bash
pgrep -af gunicorn
```

The output showed two processes.

Conceptually:

```text
Gunicorn Master
PID 23172
      |
      v
Gunicorn Worker
PID 23173
```

The master manages the worker process.

The worker handles application work.

This was different from simply thinking of the server as one process.

---

# Testing Gunicorn

I tested the same Flask health endpoint through Gunicorn:

```bash
curl http://localhost:8000/health
```

The result was:

```json
{"status":"healthy"}
```

The Flask application code had not changed.

What changed was how the application was being served:

```text
Development:
python main.py
      |
      v
Flask development server
      |
      v
port 5000
```

compared with:

```text
Gunicorn:
gunicorn main:app
      |
      v
Gunicorn
      |
      v
Flask app
      |
      v
port 8000
```

---

# Running Two Gunicorn Workers

The learning material demonstrated increasing the number of workers.

I stopped the first Gunicorn process and ran:

```bash
gunicorn main:app -w 2
```

The option:

```text
-w 2
```

requested two worker processes.

---

# Inspecting the Two-Worker Configuration

I ran:

```bash
pgrep -af gunicorn
```

The output showed three Gunicorn processes:

```text
23207
23208
23209
```

This represented:

```text
1 master
+
2 workers
=
3 processes
```

Conceptually:

```text
        Gunicorn Master
          PID 23207
          /       \
         /         \
        v           v
 Worker 23208    Worker 23209
```

This is why requesting two workers does not mean that only two total Gunicorn processes will exist.

---

# Inspecting Port 8000

I inspected the socket with:

```bash
sudo ss -lntp | grep ':8000'
```

The listener was:

```text
127.0.0.1:8000
```

The socket information was associated with the Gunicorn processes.

This connected:

```text
Gunicorn process model
        |
        v
Listening socket
        |
        v
127.0.0.1:8000
```

---

# Stopping Gunicorn

Gunicorn was stopped with:

```text
Ctrl+C
```

The output included:

```text
Shutting down: Master
```

After shutdown:

```bash
sudo ss -lntp | grep ':8000'
```

returned no matching listener.

This verified that the server had actually stopped.

---

# Flask Binding Experiment

The server material also covered application IP addresses and ports.

I reproduced this using the Flask application.

The machine had:

```text
Loopback:
127.0.0.1

eth0:
172.23.210.163
```

These were inspected using:

```bash
ip addr
```

---

# Binding Flask to 0.0.0.0

The normal application configuration was:

```python
app.run(host="0.0.0.0", port=5000)
```

When started, Flask reported:

```text
Running on all addresses (0.0.0.0)
Running on http://127.0.0.1:5000
Running on http://172.23.210.163:5000
```

I tested both addresses:

```bash
curl http://127.0.0.1:5000/health
curl http://172.23.210.163:5000/health
```

Both returned:

```json
{"status":"healthy"}
```

This demonstrated that the application was accepting IPv4 connections through both the loopback and `eth0` interfaces in this lab.

---

# Binding Flask to 127.0.0.1

I then deliberately changed:

```python
app.run(host="0.0.0.0", port=5000)
```

to:

```python
app.run(host="127.0.0.1", port=5000)
```

After restarting Flask, the startup output changed to:

```text
Running on http://127.0.0.1:5000
```

It no longer reported the `eth0` address.

---

# Testing the Loopback-Only Binding

I tested:

```bash
curl http://127.0.0.1:5000/health
```

and received:

```json
{"status":"healthy"}
```

I then tested:

```bash
curl http://172.23.210.163:5000/health
```

and received:

```text
curl: (7) Failed to connect to 172.23.210.163 port 5000: Could not connect to server
```

This was a useful troubleshooting scenario because the application itself was not down.

The evidence was:

```text
127.0.0.1:5000 works
        |
        v
Application is running

172.23.210.163:5000 fails
        |
        v
Investigate binding/listening address
```

---

# Confirming the Binding with ss

Instead of relying only on the Flask startup message, I checked the operating system:

```bash
sudo ss -lntp | grep ':5000'
```

The result showed:

```text
127.0.0.1:5000
```

with the Python process listening there.

This confirmed why:

```text
127.0.0.1:5000
```

worked while:

```text
172.23.210.163:5000
```

did not.

---

# Restoring the Application

After completing the experiment, I changed `main.py` back to:

```python
app.run(host="0.0.0.0", port=5000)
```

This is the version preserved in:

```text
lab/flask-app/main.py
```

---

# 127.0.0.1 vs 0.0.0.0

The practical difference observed in the lab was:

```text
host="127.0.0.1"
        |
        v
Listen on loopback
        |
        +--> 127.0.0.1:5000 works
        |
        +--> 172.23.210.163:5000 fails
```

Compared with:

```text
host="0.0.0.0"
        |
        v
Listen across available IPv4 interfaces
        |
        +--> 127.0.0.1:5000 works
        |
        +--> 172.23.210.163:5000 works
```

`0.0.0.0` is used here as a listening/binding address.

The client requests in the lab used actual addresses such as:

```text
127.0.0.1
172.23.210.163
```

---

# Development Server vs Gunicorn

The practical lab demonstrated two ways to serve the same Flask application.

## Flask Development Server

Started with:

```bash
python main.py
```

Observed:

```text
Flask development server
Port 5000
Development warning displayed
```

## Gunicorn

Started with:

```bash
gunicorn main:app
```

Observed:

```text
Gunicorn 26.2.0
127.0.0.1:8000
Master/worker process model
```

With two workers:

```bash
gunicorn main:app -w 2
```

Observed:

```text
1 master
2 workers
3 total Gunicorn processes
```

---

# Reproducing the Flask Lab

Move into the lab:

```bash
cd lab/flask-app
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Flask:

```bash
python main.py
```

Test it:

```bash
curl http://127.0.0.1:5000/health
```

Stop Flask with:

```text
Ctrl+C
```

Run with Gunicorn:

```bash
gunicorn main:app
```

Test Gunicorn:

```bash
curl http://127.0.0.1:8000/health
```

Run two workers:

```bash
gunicorn main:app -w 2
```

Inspect the processes:

```bash
pgrep -af gunicorn
```

Inspect the listener:

```bash
sudo ss -lntp | grep ':8000'
```

---

# Git Repository Hygiene

The Python virtual environment is not committed to Git.

The `.gitignore` contains:

```gitignore
venv/
__pycache__/
*.pyc
```

The dependencies required to recreate the environment are recorded in:

```text
requirements.txt
```

Therefore:

```text
venv/
```

is disposable, while:

```text
main.py
requirements.txt
```

are preserved.

---

# Troubleshooting a Python Web Application

A useful investigation sequence is:

```text
Is the virtual environment active?
          |
          v
Are the required packages installed?
          |
          v
Is the Python/Gunicorn process running?
          |
          v
Which address and port is listening?
          |
          v
Does curl connect?
          |
          v
Does the expected route exist?
          |
          v
What response is returned?
```

Useful commands include:

```bash
which python
which gunicorn
pip freeze
pgrep -af gunicorn
sudo ss -lntp
curl http://127.0.0.1:<port>/health
```

---

# Important Troubleshooting Lesson

The binding experiment demonstrated why:

```text
"The application is running"
```

is not enough information.

An application may be running successfully but listening on an address that does not accept the connection being attempted.

For example:

```text
Python process running
        |
        v
127.0.0.1:5000 listening
        |
        +--> request to 127.0.0.1 works
        |
        +--> request to eth0 address fails
```

Therefore, troubleshooting should ask:

```text
Is it running?
```

and then:

```text
Where is it listening?
```

---

# Key Takeaways

- Flask is a Python web framework used to build the application in this lab.
- `requirements.txt` records the Python dependencies needed to recreate the project environment.
- A virtual environment isolates project dependencies.
- `python main.py` ran Flask's development server.
- Flask explicitly warned that the development server should not be used as the production deployment server.
- Gunicorn was used as the production WSGI server introduced in the learning material.
- `gunicorn main:app` loaded the `app` object from `main.py`.
- Gunicorn defaulted to `127.0.0.1:8000` in the practical lab.
- Gunicorn uses a master/worker process model.
- `-w 2` resulted in one master plus two workers.
- `pgrep -af` helped inspect the process model.
- `ss -lntp` showed where the application was actually listening.
- Binding Flask to `127.0.0.1` allowed loopback access but prevented access through the tested `eth0` address.
- Binding to `0.0.0.0` allowed the Flask application to accept connections through both tested IPv4 interfaces.
- A connection failure does not automatically mean that the application process is down.
- Process state, listening address, port, and HTTP response should be investigated separately.
