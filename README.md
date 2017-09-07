# CArisTotle

This is a repository for my computer assisted testing web app.

## Command line interface:
First set up FLASK_APP variable:
    
    export FLASK_APP=CArisTotle/__init__.py

#### Initialize database:
    flask initdb
    
#### Load test data:
    flask testdata

#### Run development server:
    flask run

#### Purge database:
    flask dropall