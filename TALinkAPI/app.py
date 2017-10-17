from flask import Flask, jsonify, request
from flask_cors import CORS
import flask_sqlalchemy as sqlalchemy
from flask_bcrypt import Bcrypt

import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlalchemy-demo.db'

db = sqlalchemy.SQLAlchemy(app)

#------------------------------------------Don't [remove] anything above this line------------------------------------------

#--------------------------------------------------Classes / Models---------------------------------------------------------

class Student(db.Model):
	__tablename__ = 'Student'
	account_id = db.Column(db.Integer, primary_key=True)	#this is a unique id given to each account
	user_type = db.Column(db.String(16))	#Should be Student, Instructor, or Admin; can add more later if needed
	wsu_id = db.Column(db.String(16))
	space = db.Column(db.String(128))		#the account space; not sure if needed
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	wsu_email = db.Column(db.String(128))		#this doubles as a user's username
	password = db.Column(db.String(128))
	secondary_email = db.Column(db.String(128), default="N/A")		#the UI prototype allowed for an alternate email; optional?
	phone_number = db.Column(db.String(16), default="N/A")
	#-----student-unique information-----
	major = db.Column(db.String(32))	#	*******need to add functionality to support multiple majors*******
	gpa = db.Column(db.Float)			#their cumulative gpa
	expected_grad = db.Column(db.String(16))	#will be Fall XXXX or Spring XXXX, the X's being a year
	ta_before = db.Column(db.Boolean, default=False)	#if the student has been a TA before, Yes/No
	
	
class Instructor(db.Model):
	__tablename__ = 'Instructor'
	account_id = db.Column(db.Integer, primary_key=True)
	user_type = db.Column(db.String(16))
	wsu_id = db.Column(db.String(16))
	space = db.Column(db.String(128))
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	wsu_email = db.Column(db.String(128))
	password = db.Column(db.String(128))
	secondary_email = db.Column(db.String(128), default="N/A")
	phone_number = db.Column(db.String(16), default="N/A")
	#-----instructor-unique information-----
	
	
class Admin(db.Model):
	__tablename__ = 'Admin'
	account_id = db.Column(db.Integer, primary_key=True)
	user_type = db.Column(db.String(16))	
	wsu_id = db.Column(db.String(16))
	space = db.Column(db.String(128))
	first_name = db.Column(db.String(64))
	last_name = db.Column(db.String(64))
	wsu_email = db.Column(db.String(128))
	password = db.Column(db.String(128))
	secondary_email = db.Column(db.String(128), default="N/A")
	phone_number = db.Column(db.String(16), default="N/A")
	#-----admin-unique information-----
	
	
#--------------------------------------------------------Main Code----------------------------------------------------------

base_url = '/api/'

# index
# loads an account in the given space that matches the given username
# if the password does not match the password in the given user account, will not return account info
# return JSON
@app.route(base_url + 'account')
def index():
	spaceName = request.args.get('space', None) 
	if spaceName is None:
		return "Must provide space", 500

	username = request.args.get('username', None)
	password = request.args.get('password', None)
	
	if username is None:
		return "Must provide username", 500
		
	if password is None:
		return "Must provide password", 500
	
	#Look for an existing account with the given username; starting with students
	query = Student.query.filter_by(space=spaceName).filter_by(wsu_email=username).first()
	#if no student account exists with that username, search through instructor accounts, then admin accounts, and finally return an error if still no matches
	if query is None:
		query = Instructor.query.filter_by(space=spaceName).filter_by(wsu_email=username).first()
	if query is None:
		query = Admin.query.filter_by(space=spaceName).filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 500
	
	
	#NOTE!!!! After password encryption is set up, decrypt 'password' immediately below this comment before comparing it to query.password
	#^^^ This is only if we decide to do encryption in the .js file instead of here.
	
	#check if the supplied password and the account's password match

	if bcrypt.check_password_hash(query.password, password) == False:
		return "Password does not match", 500
		
		
	#prepare the information as a json file to be sent back to the requester
	result = []
	if query.user_type == "Student":
		result.append(account_to_obj_student(query))
	
	if query.user_type == "Instructor":
		result.append(account_to_obj_instructor(query))

	if query.user_type == "Admin":
		result.append(account_to_obj_admin(query))
		

	return jsonify({"status": 1, "person": result})


# create a student account
# creates an account using the given parameters
@app.route(base_url + 'account/student', methods=['POST'])
def create_student():
	account = Student(**request.json)
	if exists(account.wsu_email):
		return "An account with that username/email already exists", 500
	account.password = bcrypt.generate_password_hash(account.password).decode('utf-8')
	print(account.password)
	db.session.add(account)
	db.session.commit()

	return jsonify({"status": 1, "user": account_to_obj_student(account)}), 200
	
	
# creates an instructor account
# creates an account using the given parameters
@app.route(base_url + 'account/instructor', methods=['POST'])
def create_instructor():
	account = Instructor(**request.json)
	if exists(account.wsu_email):
		return "An account with that username/email already exists", 500
	account.password = bcrypt.generate_password_hash(account.password).decode('utf-8')
	db.session.add(account)
	db.session.commit()
	
	return jsonify({"status": 1, "user": account_to_obj_instructor(account)}), 200
	

# creates an admin account
# creates an account using the given parameters
@app.route(base_url + 'account/admin', methods=['POST'])
def create_admin():
	account = Admin(**request.json)
	if exists(account.wsu_email):
		return "An account with that username/email already exists", 500
	account.password = bcrypt.generate_password_hash(account.password).decode('utf-8')
	db.session.add(account)
	db.session.commit()
	
	return jsonify({"status": 1, "user": account_to_obj_admin(account)}), 200


# checks if a username is already in use by an existing account
# returns true/false depending on whether or not an account with the given username exists
def exists(username):
	
	query = Student.query.filter_by(wsu_email=username).first()
	if query is None:
		query = Instructor.query.filter_by(wsu_email=username).first()
	if query is None:
		query = Admin.query.filter_by(wsu_email=username).first()
	if query is None:
		return False

	return True
	
	
#------------------------------------------[row to object / account to obj] definitions below----------------------------------------
#These definitions convert a Student/Instructor/Admin class' information into a readable json format

def account_to_obj_student(user):
    user = {
			"account_id": user.account_id,
			"user_type": user.user_type,
			"wsu_id": user.wsu_id,
			"space": user.space,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"wsu_email": user.wsu_email,
			"password": user.password,
			"secondary_email": user.secondary_email,
			"phone_number": user.phone_number,
			#---------------Student-unique info------------
			"major": user.major,
			"gpa": user.gpa,
			"expected_grad": user.expected_grad,
			"ta_before": user.ta_before
		}
    return user
	
	
def account_to_obj_instructor(user):
    user = {
			"account_id": user.account_id,
			"user_type": user.user_type,
			"wsu_id": user.wsu_id,
			"space": user.space,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"wsu_email": user.wsu_email,
			"password": user.password,
			"secondary_email": user.secondary_email,
			"phone_number": user.phone_number
			#---------------Instructor-unique info------------
        }
    return user
	
	
def account_to_obj_admin(user):
    user = {
			"user_id": user.user_id,
			"user_type": user.user_type,
			"wsu_id": user.wsu_id,
			"space": user.space,
			"first_name": user.first_name,
			"last_name": user.last_name,
			"wsu_email": user.wsu_email,
			"password": user.password,
			"secondary_email": user.secondary_email,
			"phone_number": user.phone_number
			#---------------Admin-unique info------------
        }
    return user
	
  
#---------------------------------------Don't [edit] anything below this line unless you know what you're doing-------------------------------------
  
  
def main():
    db.create_all() # creates the tables you've provided
    app.run()       # runs the Flask application


if __name__ == '__main__':
    main()
