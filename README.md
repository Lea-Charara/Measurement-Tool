# Measurement Tool Backend

The backend runs using Python and Django.

## Database Models

Here's the schema of the models:
![schema](https://i.imgur.com/7Lju2aV.png)
### Tests
Contains all information related to a test.

### Database_tests
Many-to-Many, used to link a query to a test and it's database.

### Databases
They are the databases defined by the user, by type.

### Types
Types of databases available to choose from, defined by an admin.

## Setup

Install the packages and run the server by doing the following commands:

```sh
$ cd Measurement-Tool
$ pip install -r requirements.txt
$ python manage.py runserver
```
You'll be able to access the data by going to http://127.0.0.1/admin and logging in.
