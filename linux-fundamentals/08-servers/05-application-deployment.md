# Application Deployment with Apache Tomcat

## Introduction

After installing and starting Apache Tomcat, the next step was to understand how an application is deployed to the server.

The learning material introduced Java web application deployment using a WAR file.

WAR stands for:

```text
Web Application Archive
```

A WAR file packages the files belonging to a Java web application into a deployable archive.

The general deployment flow is:

```text
Application Source
       |
       v
Create WAR File
       |
       v
Copy WAR to Tomcat webapps
       |
       v
Tomcat Detects WAR
       |
       v
Tomcat Deploys Application
       |
       v
Application Context Becomes Available
       |
       v
Client Sends HTTP Request
```

---

# WAR Files

The learning material demonstrated creating a WAR file using:

```bash
jar -cvf app.war *
```

It also introduced build tools such as:

```bash
mvn package
```

and:

```bash
gradle build
```

These approaches ultimately produce an application artifact that can be deployed.

For the practical lab, I manually created a simple WAR using the `jar` command so that I could see the deployment process directly.

---

# Creating the Application Workspace

I created a workspace for the Tomcat application:

```text
~/tomcat-lab/somto
```

The application initially contained:

```text
index.html
```

The directory therefore looked like:

```text
somto/
└── index.html
```

---

# Application Source

The `index.html` file contained:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Somto Tomcat App</title>
</head>
<body>
    <h1>My First Tomcat Application</h1>
    <p>This application was deployed using a WAR file.</p>
</body>
</html>
```

This was the source content that would be packaged into the WAR.

---

# Creating the WAR

From the application directory, I created:

```text
somto.war
```

using:

```bash
jar -cvf somto.war index.html
```

The command reported that it added a manifest and the HTML file.

The resulting archive was approximately:

```text
566 bytes
```

The application directory then contained:

```text
index.html
somto.war
```

---

# Understanding the jar Command

The command was:

```bash
jar -cvf somto.war index.html
```

The options used were:

```text
c -> create a new archive
v -> verbose output
f -> specify the archive filename
```

The archive filename was:

```text
somto.war
```

and the application file included was:

```text
index.html
```

---

# Inspecting the WAR Before Deployment

Before copying the WAR into Tomcat, I inspected its contents:

```bash
jar -tf somto.war
```

The archive contained:

```text
META-INF/
META-INF/MANIFEST.MF
index.html
```

This confirmed that the WAR contained the expected application file before deployment.

This follows the same general troubleshooting principle used throughout the labs:

```text
Inspect before changing/deploying
```

---

# META-INF

The `jar` command created:

```text
META-INF/
META-INF/MANIFEST.MF
```

inside the archive.

The manifest contains archive metadata.

The important point for this lab was that the WAR was a structured archive rather than simply a renamed HTML file.

---

# Tomcat webapps Directory

Tomcat deploys applications from:

```text
/opt/apache-tomcat-11/webapps
```

Before deploying the custom application, this directory contained Tomcat's default applications:

```text
ROOT
docs
examples
host-manager
manager
```

Conceptually:

```text
/opt/apache-tomcat-11/webapps/
├── ROOT/
├── docs/
├── examples/
├── host-manager/
└── manager/
```

---

# Context Paths

Directories and WAR files under `webapps` are associated with application context paths.

For example:

```text
webapps/docs
```

was reachable through:

```text
/docs/
```

Similarly:

```text
somto.war
```

would be associated with:

```text
/somto/
```

Conceptually:

```text
webapps/somto.war
        |
        v
Application name: somto
        |
        v
Context path: /somto/
```

---

# Establishing the Before State

Before deploying the application, I tested:

```bash
curl -I http://localhost:8080/somto/
```

Tomcat returned:

```text
HTTP/1.1 404 Not Found
```

This was useful because it established that the `/somto/` application was not available before deployment.

Importantly, the `404` also proved that:

```text
Tomcat was reachable
        |
        v
HTTP request reached the server
        |
        v
/somto/ did not exist yet
```

This was not a connection failure.

---

# Deploying the WAR

I copied the WAR into Tomcat's deployment directory:

```bash
sudo cp somto.war /opt/apache-tomcat-11/webapps/
```

The deployment location became:

```text
/opt/apache-tomcat-11/webapps/somto.war
```

Tomcat was already running.

I did not manually restart Tomcat after copying the WAR.

---

# Automatic Deployment

Tomcat detected the WAR and automatically deployed it.

After deployment, the `webapps` directory contained both:

```text
somto.war
```

and an expanded directory:

```text
somto/
```

Conceptually:

```text
somto.war
    |
    | Tomcat detects archive
    v
somto/
    |
    v
Application deployed
```

This demonstrated Tomcat's automatic deployment behaviour for the running server configuration used in the lab.

---

# Expanded Application

Tomcat expanded the WAR into a directory under:

```text
/opt/apache-tomcat-11/webapps/somto/
```

Therefore, the deployment directory contained:

```text
somto.war
somto/
```

The WAR was the deployment artifact, while the expanded directory represented the deployed application files.

---

# Verifying Deployment Through Logs

Instead of assuming that copying the WAR meant deployment had succeeded, I checked Tomcat's logs.

I inspected:

```text
/opt/apache-tomcat-11/logs/catalina.out
```

The log contained a message similar to:

```text
Deploying web application archive [/opt/apache-tomcat-11/webapps/somto.war]
```

followed by:

```text
Deployment of web application archive [/opt/apache-tomcat-11/webapps/somto.war] has finished
```

The deployment completed in approximately:

```text
32 ms
```

This provided server-side evidence that Tomcat had detected and deployed the WAR.

---

# Verifying Deployment with HTTP

After the deployment completed, I tested:

```bash
curl -I http://localhost:8080/somto/
```

The response was:

```text
HTTP/1.1 200
```

The response also reported:

```text
Content-Length: 197
```

The original `index.html` file was:

```text
197 bytes
```

This connected the deployed application's HTTP response back to the source file.

---

# Retrieving the Application

I then requested the full page:

```bash
curl http://localhost:8080/somto/
```

Tomcat returned:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Somto Tomcat App</title>
</head>
<body>
    <h1>My First Tomcat Application</h1>
    <p>This application was deployed using a WAR file.</p>
</body>
</html>
```

This confirmed the complete deployment chain:

```text
index.html
     |
     v
somto.war
     |
     v
Tomcat webapps/
     |
     v
Automatic deployment
     |
     v
/somto/
     |
     v
HTTP 200
     |
     v
Expected HTML content
```

---

# Before vs After Deployment

Before deployment:

```text
GET /somto/
     |
     v
HTTP 404
```

After deployment:

```text
GET /somto/
     |
     v
HTTP 200
```

This comparison was useful because it demonstrated that the deployment changed application availability without changing the server itself.

Tomcat was reachable in both cases.

The difference was:

```text
Before -> application absent
After  -> application deployed
```

---

# Deployment Did Not Require a Tomcat Restart

For this lab, Tomcat was already running when:

```text
somto.war
```

was copied into:

```text
webapps/
```

Tomcat detected and deployed the application automatically.

Therefore:

```text
Copy WAR
   |
   v
Tomcat detects archive
   |
   v
Tomcat deploys application
   |
   v
Application becomes available
```

No manual restart was required for this deployment.

This is different from the later `server.xml` connector-port change, where Tomcat had to be stopped and started for the new port configuration to take effect.

---

# Deployment vs Server Configuration

The labs demonstrated an important difference between deploying an application and changing Tomcat's server configuration.

## Deploying a WAR

```text
Copy somto.war into webapps
        |
        v
Tomcat detects deployment
        |
        v
Application becomes available
```

In this lab, no server restart was required.

## Changing server.xml

```text
Edit Connector port
        |
        v
Configuration file changes
        |
        v
Existing process still uses old configuration
        |
        v
Restart Tomcat
        |
        v
New configuration becomes active
```

Understanding whether a change affects application content/deployment or server configuration helps determine what action is required afterward.

---

# Testing the Application After the Port Change

Later, Tomcat's HTTP connector was changed from:

```text
8080
```

to:

```text
9090
```

The deployed application remained available through the new server port.

I tested:

```bash
curl -I http://localhost:9090/somto/
```

and received:

```text
HTTP/1.1 200
```

The application's context path remained:

```text
/somto/
```

Only the server's listening port changed.

Therefore:

```text
Before:
http://localhost:8080/somto/

After connector change:
http://localhost:9090/somto/
```

This demonstrates that the URL contains multiple independent pieces:

```text
http://localhost:9090/somto/
       |         |      |
       |         |      +--> application context
       |         |
       |         +---------> server port
       |
       +-------------------> server address
```

---

# WAR Build Tools in the Learning Material

The learning material also introduced other ways that WAR files may be generated.

Examples included:

```bash
mvn package
```

for Maven and:

```bash
gradle build
```

for Gradle.

These build tools were shown as ways to produce application artifacts.

In my practical lab, I used the simpler manual command:

```bash
jar -cvf somto.war index.html
```

This allowed me to focus specifically on understanding:

```text
source
  ->
WAR
  ->
webapps
  ->
deployment
  ->
context path
  ->
HTTP response
```

---

# Why the WAR Is Not Stored in This Git Lab

The repository preserves the source file:

```text
lab/tomcat-app/index.html
```

but does not need to store:

```text
somto.war
```

because the WAR can be recreated from the source.

The repository's `.gitignore` therefore includes:

```gitignore
*.war
```

To recreate the artifact:

```bash
cd lab/tomcat-app
jar -cvf somto.war index.html
```

This keeps the repository focused on source files while documenting how the deployment artifact is generated.

---

# Reproducing the Deployment

From the Git lab directory:

```bash
cd lab/tomcat-app
```

Create the WAR:

```bash
jar -cvf somto.war index.html
```

Inspect it:

```bash
jar -tf somto.war
```

Deploy it:

```bash
sudo cp somto.war /opt/apache-tomcat-11/webapps/
```

Inspect the deployment directory:

```bash
ls -lh /opt/apache-tomcat-11/webapps/
```

Check the Tomcat deployment log:

```bash
sudo tail -n 30 /opt/apache-tomcat-11/logs/catalina.out
```

Test the application on the configured Tomcat port:

```bash
curl -I http://localhost:9090/somto/
```

Retrieve the page:

```bash
curl http://localhost:9090/somto/
```

---

# Deployment Troubleshooting

If a deployed application does not work, I can inspect the deployment systematically.

```text
Does the WAR exist?
       |
       v
Does jar -tf show the expected files?
       |
       v
Was the WAR copied into webapps?
       |
       v
Did Tomcat detect the WAR?
       |
       v
What does catalina.out report?
       |
       v
Is Tomcat running?
       |
       v
Is the expected Tomcat port listening?
       |
       v
Is the correct context path being requested?
       |
       v
What HTTP status is returned?
```

Useful commands include:

```bash
jar -tf somto.war
ls -lh /opt/apache-tomcat-11/webapps/
pgrep -af 'org.apache.catalina.startup.Bootstrap'
sudo ss -lntp | grep ':9090'
sudo tail -n 30 /opt/apache-tomcat-11/logs/catalina.out
curl -I http://localhost:9090/somto/
```

---

# Understanding Different Failure States

## Connection Failure

If:

```bash
curl http://localhost:8080/somto/
```

returns:

```text
curl: (7) Failed to connect
```

after Tomcat has moved to port 9090, the problem occurs before an HTTP response is received.

The first question should be whether anything is listening on port 8080.

---

## HTTP 404

If Tomcat returns:

```text
HTTP/1.1 404 Not Found
```

then:

```text
Tomcat is reachable
HTTP is working
The requested application/resource was not found
```

The investigation should move toward:

```text
context path
deployment
webapps directory
deployment logs
```

rather than treating the server as completely unreachable.

---

## HTTP 200

If the request returns:

```text
HTTP/1.1 200
```

and the expected application content is returned, the deployment has been verified from the client perspective.

---

# Key Takeaways

- Java web applications can be packaged as WAR files.
- The learning material demonstrated WAR creation with `jar` and also introduced Maven and Gradle packaging.
- The practical lab created `somto.war` from `index.html`.
- `jar -tf` can inspect a WAR before deployment.
- Tomcat deploys applications from its `webapps` directory.
- `somto.war` became available through the `/somto/` context path.
- The application returned `404` before deployment and `200` after deployment.
- Tomcat automatically expanded the WAR into a `somto/` directory.
- `catalina.out` provided evidence that the WAR had been detected and deployed.
- The application deployment did not require a manual Tomcat restart in this lab.
- Application deployment and server configuration changes have different lifecycles.
- Changing Tomcat's connector from 8080 to 9090 changed the server port but did not change the `/somto/` application context.
- Generated WAR files do not need to be committed when they can be recreated from source.
- Deployment should be verified through the artifact, deployment directory, logs, listening socket, HTTP status, and returned content.
