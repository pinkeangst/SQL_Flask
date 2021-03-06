import sqlite3
import datetime

def connect_to_db():
	return sqlite3.connect("tipsy.db")
	 
def new_user(db, email, password, name):
	c = db.cursor()
	query = """INSERT INTO Users VALUES	(NULL, ?,?,?)"""
	result = c.execute(query, (email, password, name))
	db.commit()
	return result.lastrowid

#given a username and password, returns a dictionary of a user's fields pulled from the database, and a None if the credentials do not match
def authenticate(db, email, password):
	c = db.cursor()
	query = """SELECT * FROM Users WHERE email=? AND password=?"""
	c.execute(query, (email, password))
	result = c.fetchone() #return ONE single from Users table matching row to the query
	db.commit()
	#Create a dictionary
	if result:
		#fields = ["email", "password"]
		fields = ["id", "email", "password", "email"] #This is the field/column email of the dictionary
		return dict(zip(fields, result)) #This returns a dictionary created from the zip pairing of the 4 text names in fields with the 4 values in result, which came fron the 4 columns in the Users table.
	else:
		return None #Else no email and password given, resulting in None

#Creates a new task, returns the id of theturn the user as a dictionary, like our authenticate method. newly created row. Make sure to populate the created_at field.
def new_task(db, title, user_id): #(db, id, title, created_at, completed_at, user_id):
	c = db.cursor()
	query = """INSERT INTO Tasks VALUES (NULL, ?,?, NULL, ?)"""#(id, title, created_at, completed_at, user_id)"""
	t = datetime.datetime.utcnow() # t = created_at
	result = c.execute(query, (title, t, user_id))
	db.commit()
	return result.lastrowid


def get_user(db, id): #Fetch a user's record based on his id. Return the user as a dictionary, like our authenticate method.
	c = db.cursor()
	query = """SELECT * FROM Users WHERE id=?"""
	c.execute(query,(id))
	result = c.fetchone()
	db.commit()
	#Create a dictionary
	if result:
		fields = ["id", "email", "password", "name"] #Fields is the column name of the dictionary
		return dict(zip(fields, result)) #This returns a dictionary created from the zip pairing of the 4 text names in fields with the 4 values in result, which came fron the 4 columns in the Users table.
	else:
		return None #Else no username and password given, resulting in None

def complete_task(db, id): #Marks a task as being complete, setting the completed_at field.
	c = db.cursor()
	completed_at = datetime.datetime.utcnow() 
	query = """UPDATE Tasks SET completed_at = ? WHERE id=?""" # t = completed_at
	result = c.execute(query,(completed_at, id))
	db.commit()
	return id	

def get_tasks(db, user_id=None): #Gets all the tasks for the given user id. Returns all the tasks in the system if no user_id is given. Returns them as a list of dictionaries.
	c = db.cursor()
	if user_id == None: #Returns all the tasks in the system if no user_id is given.
		query = """SELECT * FROM Tasks"""
		cursor = c.execute(query)
		rows = cursor.fetchall()		
		#return rows
	else: #Gets all the tasks for the given user id.Returns them as a list of dictionaries.
		query = """SELECT * FROM Tasks WHERE user_id=?"""
		cursor = c.execute(query,(user_id, )) # Tuple of
		rows = cursor.fetchall()	
		#return rows

	tasks = []
	for row in rows: #add individual tasks to task list
		task = dict(zip(["id","title", "created_at", "completed_at", "user_id"], row))
		tasks.append(task)
	return tasks


def get_task(db, id): #Get a single task, given its id. Return the task as a dictionary as above in the authenticate method.
	c = db.cursor()
	query = """SELECT * FROM Tasks WHERE id=?"""
	c.execute(query,(id))
	result = c.fetchone()
	db.commit()
	#Create a dictionary
	if result:
		fields = ["id", "title", "created_at", "completed_at", "user_id"] #Fields is the column name of the dictionary
		return dict(zip(fields, result)) #This returns a dictionary created from the zip pairing of the 4 text names in fields with the 4 values in result, which came fron the 4 columns in the Users table.
	else:
		return None #Else no username and password given, resulting in None

# def main():
#     connect_to_db()
#     command = None
#     while command != "quit":
#         input_string = raw_input("HBA Database> ")
#         tokens = input_string.split()
#         command = tokens[0]
#         args = tokens[1:]

#         if command == "new_user":
#             new_user(*args) 
#         elif command == "authenticate":
#             authenticate(*args)
#         elif command == "new_task":
#             new_task(*args)

#     CONN.close()


# if __name__ == "__main__":
#     main()