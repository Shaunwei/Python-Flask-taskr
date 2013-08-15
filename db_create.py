#db_create.py

from flasktaskr import db
from flasktaskr.models import FTasks
from datetime import date

#create the database and the db table
db.create_all()

#insert data
db.session.add(FTasks("Finish this turorial", date(2013,8,15),10,1))
db.session.add(FTasks("Finish my book", date(2013,3,13),10,1))

#commit the changes
db.session.commit()