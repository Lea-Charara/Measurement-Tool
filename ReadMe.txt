You have 4 tables:
Database -> Create a new database, update Database, Remove Database, get Database
DatabaseTest -> This table is for the queries with their own database
Test -> This is the table with the Test name and description and timeout 
Type -> Type table

To put your connection test code you go to Database and then views.py
To put your run test code you go to Test and then views.py

If you want to add any file be sure to put it in the Measurement-Tool folder

To test the server locally you write in the visual code terminal : 
cd Measurement-Tool
python3 manage.py runserver

To open the server you do : 127.0.0.1/admin

When you finish with testing push to the backend-dev branch it will automatically update the heroku server.