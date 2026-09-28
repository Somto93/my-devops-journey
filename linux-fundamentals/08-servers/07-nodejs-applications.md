# Node.js Applications and PM2

## Introduction

The server learning material introduced Node.js applications and showed how Node.js dependencies are installed and applications are started.

The material demonstrated:

```bash
npm install
node app.js
npm run start
```

It also introduced PM2 as a production process manager for Node.js applications.

In the practical lab, I created an Express application, inspected its processes and listening port, configured an npm start script, and then managed the application with PM2.

---

# Project Structure

The practical Node.js application was created under:

```text
~/server-lab/node-app
```

The project contained:

```text
node-app/
├── app.js
├── package.json
├── package-lock.json
└── node_modules/
```

The Git lab preserves:

```text
lab/node-app/
├── app.js
├── package.json
└── package-lock.json
```

The `node_modules` directory is excluded because dependencies can be recreated using npm.

---

# Checking Node.js and npm

Before creating the application, I checked Node.js:

```bash
node --version
```

The installed version was:

```text
v22.22.1
```

I also checked npm:

```bash
npm --version
```

The installed version was:

```text
9.2.0
```

This confirmed that both Node.js and npm were available.

---

# Node.js and npm

Node.js provides the runtime used to execute JavaScript on the server.

npm is used to manage packages and project dependencies.

Conceptually:

```text
Node.js
   |
   v
JavaScript Runtime

npm
   |
   v
Package Management
```

The learning material compared:

```bash
npm install
```

with the Python command:

```bash
pip install -r requirements.txt
```

Both are used to install application dependencies, although the project files and package-management systems are different.

---

# Initialising the Project

Inside the project directory, I ran:

```bash
npm init -y
```

This created:

```text
package.json
```

The `-y` option accepted the default values automatically.

---

# package.json

`package.json` describes the Node.js project.

The practical project contained information such as:

```json
{
  "name": "app",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node app.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "dependencies": {
    "express": "^5.2.1"
  }
}
```

Important sections include:

```text
name
version
scripts
dependencies
```

---

# Installing Express

The application used Express.

I installed it with:

```bash
npm install express
```

npm added Express to the project dependencies.

The dependency appeared in `package.json` as:

```json
"express": "^5.2.1"
```

npm also created:

```text
package-lock.json
node_modules/
```

---

# node_modules

The installed package files were stored under:

```text
node_modules/
```

This directory can become large because it contains the project's installed dependency tree.

It does not need to be stored in this Git repository because npm can recreate it from the project's dependency information.

The repository's `.gitignore` therefore contains:

```gitignore
node_modules/
```

---

# package-lock.json

npm also created:

```text
package-lock.json
```

This file records detailed information about the dependency tree resolved by npm.

Unlike `node_modules`, the lock file is preserved in the Git lab.

Therefore:

```text
package.json       -> preserved
package-lock.json  -> preserved
node_modules/      -> ignored
```

---

# Installing Existing Project Dependencies

If the repository is cloned onto another machine, the dependencies can be recreated by running:

```bash
npm install
```

Conceptually:

```text
package.json
package-lock.json
       |
       v
npm install
       |
       v
node_modules/
```

This is why the dependency directory itself does not need to be committed.

---

# Express Application

The application in `app.js` was:

```javascript
const express = require('express');

const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
    res.send('Somto Node.js Server Lab');
});

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

---

# Creating the Express Application

The line:

```javascript
const express = require('express');
```

loads the Express package.

The application is then created with:

```javascript
const app = express();
```

The application port was defined as:

```javascript
const PORT = 3000;
```

---

# Root Route

The root route was:

```javascript
app.get('/', (req, res) => {
    res.send('Somto Node.js Server Lab');
});
```

A request to:

```text
/
```

returns:

```text
Somto Node.js Server Lab
```

---

# Health Route

The health route was:

```javascript
app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});
```

A request to:

```text
/health
```

returns:

```json
{"status":"healthy"}
```

As with the Flask lab, the health endpoint provided a simple way to verify that the application was responding.

---

# Starting the Server

The application starts listening with:

```javascript
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
```

Since:

```javascript
PORT = 3000
```

the application listens on port:

```text
3000
```

---

# Running the Application Directly

I started the application with:

```bash
node app.js
```

The terminal displayed:

```text
Server running on port 3000
```

The Node.js process was running in the foreground.

---

# Inspecting Port 3000

While the application was running, I checked:

```bash
sudo ss -lntp | grep ':3000'
```

The output showed Node.js listening on port 3000.

The Node process had PID:

```text
23303
```

This connected:

```text
node app.js
      |
      v
Node process
PID 23303
      |
      v
TCP port 3000
```

---

# Testing the Node.js Application

I tested the health endpoint:

```bash
curl http://localhost:3000/health
```

The response was:

```json
{"status":"healthy"}
```

This verified:

```text
Node process
     |
     v
Port 3000
     |
     v
Express
     |
     v
/health
     |
     v
Healthy response
```

---

# npm Scripts

The learning material also demonstrated:

```bash
npm run start
```

npm scripts are defined inside the:

```json
"scripts"
```

section of `package.json`.

Initially, the project did not contain a `start` script.

Running:

```bash
npm run start
```

therefore could not start the application through npm.

---

# Adding the Start Script

I edited `package.json` and added:

```json
"start": "node app.js"
```

The scripts section became:

```json
"scripts": {
  "start": "node app.js",
  "test": "echo \"Error: no test specified\" && exit 1"
}
```

This connected the npm command:

```bash
npm run start
```

to:

```bash
node app.js
```

---

# JSON Syntax Matters

While editing `package.json`, I initially omitted a comma between JSON entries.

I noticed the syntax problem before trying to run the application and corrected it.

This was a useful reminder that `package.json` must contain valid JSON.

For example:

```json
{
  "scripts": {
    "start": "node app.js",
    "test": "echo \"test\""
  }
}
```

requires commas between properties.

Configuration and metadata files should be inspected carefully after manual edits.

---

# Inspecting Available npm Scripts

I ran:

```bash
npm run
```

The output showed the available scripts, including:

```text
start
test
```

This verified that npm recognised the new `start` script.

---

# Running with npm

I started the application using:

```bash
npm run start
```

npm displayed:

```text
> app@1.0.0 start
> node app.js
```

followed by:

```text
Server running on port 3000
```

The application again responded successfully on:

```text
http://localhost:3000
```

---

# npm Process Hierarchy

An interesting difference appeared when the application was started with:

```bash
npm run start
```

instead of directly with:

```bash
node app.js
```

I inspected the processes and observed a hierarchy similar to:

```text
npm
 |
 v
shell
 |
 v
node app.js
```

The observed PIDs during the lab were:

```text
npm   -> 23482
shell -> 23493
node  -> 23494
```

This demonstrated that the PID seen for a command launcher may not always be the PID of the final application process.

---

# Parent and Child Processes

The process hierarchy was:

```text
npm process
PID 23482
    |
    v
shell
PID 23493
    |
    v
node app.js
PID 23494
```

This became an important process-troubleshooting lesson.

If an unexpected PID appears, I should not immediately assume that the wrong application is running.

Instead, I can inspect the process relationship.

Useful commands include:

```bash
ps -fp <PID>
```

and:

```bash
ps -ef
```

The parent PID can help trace how the application was launched.

---

# Direct Execution vs npm Script

These two commands ultimately ran the same application:

```bash
node app.js
```

and:

```bash
npm run start
```

However, the process hierarchy was different.

Direct execution:

```text
shell
  |
  v
node app.js
```

npm execution:

```text
shell
  |
  v
npm
  |
  v
shell
  |
  v
node app.js
```

This is why process inspection is useful when troubleshooting applications started through wrappers or process managers.

---

# PM2

The learning material introduced PM2 as a production process manager for Node.js applications.

It described PM2 as providing capabilities such as:

```text
Keeping applications alive
Managing application processes
Reloading applications
Running multiple instances
Built-in load balancing
```

The practical lab focused on starting, inspecting, scaling, testing, and deleting the Express application with PM2.

---

# Checking for PM2

Initially I ran:

```bash
pm2 --version
```

The result was:

```text
command not found
```

This established that PM2 was not yet available on the system.

---

# Installing PM2

For the practical lab, PM2 was installed globally through npm:

```bash
sudo npm install -g pm2
```

This installation step was part of the practical setup.

The source material focused primarily on using PM2 after it was available.

---

# First PM2 Invocation

I checked:

```bash
pm2 --version
```

The first invocation started the PM2 daemon.

The installed version was:

```text
7.0.4
```

PM2 created its working directory under:

```text
/home/somto/.pm2
```

---

# PM2 Daemon

PM2 uses a background daemon to manage applications.

Conceptually:

```text
PM2 CLI
   |
   v
PM2 Daemon
   |
   v
Managed Applications
```

This allows PM2-managed applications to continue being managed independently of the individual command used to start them.

---

# Inspecting PM2

I ran:

```bash
pm2 list
```

An application named:

```text
app
```

appeared in a stopped state.

Instead of assuming what this entry represented, I inspected it:

```bash
pm2 describe app
```

The information showed that it referred to:

```text
/home/somto/server-lab/node-app/app.js
```

with the working directory:

```text
/home/somto/server-lab/node-app
```

This confirmed that the PM2 entry belonged to the Node.js lab application.

---

# Starting the Existing PM2 Application

I started the existing PM2 entry:

```bash
pm2 start app
```

Then:

```bash
pm2 list
```

showed the application as:

```text
online
```

The process had PID:

```text
23952
```

and was running in:

```text
fork
```

mode.

---

# Verifying PM2 Fork Mode

I checked port 3000:

```bash
sudo ss -lntp | grep ':3000'
```

The output showed the Node.js process listening on port 3000.

The PID matched the PM2-managed application:

```text
23952
```

I then tested:

```bash
curl http://localhost:3000/health
```

and received:

```json
{"status":"healthy"}
```

This connected the PM2 process table to the actual network service.

---

# PM2 Fork Mode

In this lab, the single PM2-managed instance used:

```text
fork mode
```

Conceptually:

```text
PM2
 |
 v
Node.js Application
 |
 v
Port 3000
```

The application was online and serving requests normally.

---

# Removing the PM2 Application

Before testing multiple instances, I removed the existing application:

```bash
pm2 delete app
```

Then:

```bash
pm2 list
```

showed an empty application list.

This provided a clean starting state for the cluster-mode experiment.

---

# Starting Four PM2 Instances

The learning material demonstrated:

```bash
pm2 start app.js -i 4
```

I reproduced this command:

```bash
pm2 start app.js -i 4
```

PM2 started four instances of the Express application.

---

# PM2 Cluster Mode

After starting four instances:

```bash
pm2 list
```

showed four applications named:

```text
app
```

All four were:

```text
online
```

and running in:

```text
cluster
```

mode.

The worker PIDs were:

```text
24005
24012
24023
24034
```

Conceptually:

```text
              PM2
               |
      +--------+--------+--------+
      |        |        |        |
      v        v        v        v
   Worker    Worker    Worker    Worker
   24005     24012     24023     24034
```

---

# Why Multiple Instances Can Use One Application Port

All four instances belonged to the same Express application, which uses:

```text
PORT = 3000
```

Yet the application remained available through one service endpoint:

```text
localhost:3000
```

PM2's cluster mode manages the multiple application instances behind the service.

This corresponds to the learning material's introduction of PM2's built-in load-balancing capability.

---

# Inspecting Port 3000 in Cluster Mode

I ran:

```bash
sudo ss -lntp | grep ':3000'
```

This time the result was different from the earlier single-process Node.js lab.

Instead of displaying one of the application worker PIDs as the listener, the socket information showed the PM2 daemon process:

```text
PM2 v7.0.4: God
```

with PID:

```text
23843
```

This was useful because it demonstrated that process/socket relationships can look different when a process manager is involved.

---

# Do Not Assume the Listener PID

Earlier, when I ran:

```bash
node app.js
```

directly, `ss` showed the Node.js process.

In PM2 fork mode, the Node application PID was visible as the listener.

In the four-instance cluster-mode experiment, `ss` showed the PM2 daemon associated with the listening socket.

Therefore, I should inspect the evidence rather than assume:

```text
Port 3000 must always show the same type of PID.
```

The way an application is launched can affect the process/socket view.

---

# Verifying Cluster Mode with HTTP

Even though the process model had changed, the client-facing endpoint remained:

```text
http://localhost:3000
```

I tested:

```bash
curl http://localhost:3000/health
```

and received:

```json
{"status":"healthy"}
```

Therefore:

```text
4 PM2 application instances
          |
          v
Application available on port 3000
          |
          v
/health returns healthy
```

---

# PM2 Logs

The PM2 application information showed log locations under:

```text
~/.pm2/logs/
```

For example, PM2 can maintain output and error logs for managed applications in this directory.

This provides another troubleshooting source when an application is managed by PM2.

---

# Cleaning Up the PM2 Lab

After completing the cluster experiment, I removed the application:

```bash
pm2 delete app
```

Then I checked:

```bash
pm2 list
```

The application list was empty.

I also checked port 3000:

```bash
sudo ss -lntp | grep ':3000'
```

There was no matching listener.

This verified that the managed application had been removed and was no longer serving traffic.

---

# Node.js Application Lifecycle

The practical lab demonstrated several ways of running the same application.

## Direct Node.js

```text
node app.js
      |
      v
Node process
      |
      v
Port 3000
```

## npm Script

```text
npm run start
      |
      v
npm
      |
      v
shell
      |
      v
node app.js
      |
      v
Port 3000
```

## PM2 Fork Mode

```text
PM2
 |
 v
Single application instance
 |
 v
Port 3000
```

## PM2 Cluster Mode

```text
PM2
 |
 +--> Instance 1
 +--> Instance 2
 +--> Instance 3
 +--> Instance 4
 |
 v
Application service on port 3000
```

The application code remained the same.

The process-management method changed.

---

# Reproducing the Node.js Lab

Move into the lab:

```bash
cd lab/node-app
```

Install dependencies:

```bash
npm install
```

Run directly:

```bash
node app.js
```

Test:

```bash
curl http://localhost:3000/health
```

Stop with:

```text
Ctrl+C
```

Run through npm:

```bash
npm run start
```

Inspect processes:

```bash
ps -ef | grep '[n]ode'
```

Stop the application and start it with PM2:

```bash
pm2 start app.js
```

Inspect:

```bash
pm2 list
```

Test:

```bash
curl http://localhost:3000/health
```

For the cluster-mode lab:

```bash
pm2 delete app
pm2 start app.js -i 4
```

Inspect:

```bash
pm2 list
```

Check the listener:

```bash
sudo ss -lntp | grep ':3000'
```

Clean up:

```bash
pm2 delete app
```

---

# Git Repository Hygiene

The Node.js dependency directory is excluded from Git:

```gitignore
node_modules/
```

The repository keeps:

```text
app.js
package.json
package-lock.json
```

This means the environment can be recreated with:

```bash
npm install
```

without storing all downloaded dependency files in Git.

---

# Troubleshooting Node.js Applications

A useful troubleshooting sequence is:

```text
Is Node.js installed?
        |
        v
Do package.json and package-lock.json exist?
        |
        v
Have dependencies been installed?
        |
        v
Does the required npm script exist?
        |
        v
Is the application process running?
        |
        v
Is the expected port listening?
        |
        v
Who owns the listening socket?
        |
        v
Does curl receive a response?
        |
        v
If PM2 is involved, what does pm2 list show?
```

Useful commands include:

```bash
node --version
npm --version
npm run
ps -ef | grep '[n]ode'
pm2 list
pm2 describe app
sudo ss -lntp | grep ':3000'
curl http://localhost:3000/health
```

---

# Important Process Troubleshooting Lesson

One of the most useful lessons from this lab was that the process model depends on how an application is launched.

The same application can appear differently when started using:

```text
node
npm
PM2 fork mode
PM2 cluster mode
```

Therefore, if a PID is unexpected, the correct response is not immediately to kill it.

Instead:

```text
Unexpected PID
     |
     v
Inspect process
     |
     v
Check parent/child relationships
     |
     v
Identify process manager
     |
     v
Connect process to socket
     |
     v
Test application
```

This follows the broader troubleshooting principle:

```text
Inspect first.
Understand the failing layer.
Then make a change.
```

---

# Key Takeaways

- Node.js provides the JavaScript runtime used by the server application.
- npm manages Node.js project dependencies and scripts.
- `npm init -y` creates a basic `package.json`.
- `npm install express` installed Express and recorded it as a dependency.
- `npm install` can recreate the project's dependencies.
- `node app.js` directly starts the application.
- `npm run start` executes the `start` script defined in `package.json`.
- JSON syntax must remain valid when manually editing `package.json`.
- Starting through npm introduces additional processes between the shell and the Node.js application.
- Parent and child process relationships can explain unexpected PIDs.
- PM2 was used to manage the Node.js application.
- PM2 fork mode ran a single application instance in the practical lab.
- `pm2 start app.js -i 4` created four cluster-mode instances.
- All four instances remained available through the application's port 3000 endpoint.
- In the cluster experiment, `ss` showed the PM2 daemon associated with the listening socket rather than one of the worker PIDs.
- `pm2 list` and `pm2 describe` provide process-manager-specific evidence.
- `curl` should still be used to verify that the application responds from the client perspective.
- `node_modules` is excluded from Git while `package.json` and `package-lock.json` are preserved.
