# Relative Estimator

Relative Estimator is a simple application that can help am agile team during the task estimation process.
The application builds a list of referential tasks using Jira (by Atlassian) issues completed in previous sprints.

# Installation

## Requirements
* Node.js - to build web application, 
* Python 3.6+ - to start server and generate the referential tasks list.

## Browser App installation
0. Go to root project directory and execute:
    ```
    npm install
    ```
0. After the successful installation, execute the build command:
    ```
    npm run build
    ```
0. React App has been built.

## Server installation
It's highly recommended to use some Python Environment Manager eg. venv.

0. Go to server subdirectory
0. Install python requirements:
    ```
       pip3 install -r requirements.txt
    ```
   
# Configuration
0. make copy of the `config_template.ini` file to `config.ini`
0. open config file and enter the parameters:
-  In the JIRA section put:
    - jira instance host with protocol, 
    - user and password (with access to the tasks)
- In the FILTERS section enter:
    - project_codes - the code names of the projects to search, 
    - max_results - maximum number of tasks in the referential list
    - exclusion_labels - list of labels that exclude the issues from the referential list
    - oldest_results - resolve date of oldest issue, 
    negative value is expected in format -{I}d where {I} is number of days.
- Section OUTPUT leave unchanged

# Start app
0. Generate the referential issue list and call:
    ```
    python3 generate.py
    ```
   for more options call `python3 generate.py -h`
0. Start server:
    ```
    python3 server.py
    ```
0. Open web browser page http://localhost:8080

# Development
See [React App Development](docs/ReactAppDevelopment.md) for basic information about the web app development.