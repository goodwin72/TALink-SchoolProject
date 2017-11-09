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


#------------------------------------------------- Classes / Models --------------------------------------------------------
#	Here we define the classes/models needed for the software
#---------------------------------------------------------------------------------------------------------------------------

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
	course_preferences = db.relationship('CoursePreference', backref='student') # should be a list of CoursePreferences
	#assigned_ta = db.Column(db.Boolean, default=False) #whether or not the student is already a TA
	
class CoursePreference(db.Model):
	pref_id = db.Column(db.Integer, primary_key=True)
	person_id = db.Column(db.Integer, db.ForeignKey('Student.account_id'))	# this is the id of the user an instance of this class belongs to
	course_name = db.Column(db.String(8))	# this refers to the course prefix + number, so 'Cpt_S 322' as example
	grade_earned = db.Column(db.String(4))
	date_taken = db.Column(db.String(16)) # will be Fall XXXX, Spring XXXX, or Summer XXXX; the X's being a year
	#date_applyfor = db.Column(db.String(16))	# the semester+year that is being applied for
	ta_before = db.Column(db.Boolean, default=False)	# whether or not the student has TA'd for THIS class before
	
	
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
	courses_taught = db.relationship('InstructorCourse', backref='instructor')
	
class InstructorCourse(db.Model):
	course_id = db.Column(db.Integer, primary_key=True)
	person_id = db.Column(db.Integer, db.ForeignKey('Instructor.account_id'))	# this is the id of the user an instance of this class belongs to
	course_name = db.Column(db.String(8))	# this refers to the course prefix + number, so 'Cpt_S 322' as example
	semester = db.Column(db.String(16)) # the semester and year the course is offered
	course_sections = db.relationship('CourseSection', backref='course') # a list of CourseSections
	
class CourseSection(db.Model):
	section_id = db.Column(db.Integer, primary_key=True)
	course_id = db.Column(db.Integer, db.ForeignKey('instructor_course.course_id'))	# this is the id of the user an instance of this class belongs to
	section_name = db.Column(db.String(16))	# this refers to the full name of this instance of the course, ie. 'Cpt_S 122-LAB01'
	days_lecture = db.Column(db.String(8)) # this is any combo of MTWTFSS; the first letter of the days of the week; the days the course occurs
	time_lecture = db.Column(db.String(32)) #this is the time the course occurs at; ie. 8:00 - 14:00; we'll try to maintain class-signup format
	ta_chosen = db.Column(db.Boolean, default=False) # whether or not a TA has been chosen for this course section
	#ta_apps = db.relationship('TAApplications', backref='section')
	#ta_username =
	#ta_name = 
	
	#note, to get the course's instructor, you should be able to use [CourseSectionObject].course.instructor.first_name, etc.
	# as such, I don't see the need for a specific "instructor name" field. Though, you can add one if the above doesn't work.
	# just remember that the functions for creating one need to be updated too.
	
	# ***Note: Wondering why the CourseSection's db.ForeignKey()'s class name is lower case and has underscores?
	# ***		it's because SQLAlchemy auto-converts camelcase class names (ie, InstructorCourse) into that format. 
	# ***		If you try write it as camelcase, you'll get an error.
	
class TAApplications(db.Model):
	app_id = db.Column(db.Integer, primary_key=True)
	#section_id = db.Column(db.Integer, db.ForeignKey('course_section.section_id'))
	student_name = db.Column(db.String(64))
	student_id = db.Column(db.Integer)
	grade_earned = db.Column(db.String(4))
	date_taken = db.Column(db.String(16)) # will be Fall XXXX, Spring XXXX, or Summer XXXX; the X's being a year
	ta_before = db.Column(db.Boolean, default=False)

	
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
	
	
#------------------------------------------------------- Main Code ---------------------------------------------------------
#	This section contains most of functions that are related to Post/Get requests
#---------------------------------------------------------------------------------------------------------------------------

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
	
	#check if the supplied password and the account's password match

	if bcrypt.check_password_hash(query.password, password) == False:
		return "Password does not match", 500
		
		
	#prepare the information as a json file to be sent back to the requester
	#result = []
	if query.user_type == "Student":
		result = account_to_obj_student(query)
		###for c in query.course_preferences:
		###	  result.append(preference_to_obj(c))
	
	if query.user_type == "Instructor":
		result = account_to_obj_instructor(query)
		###for c in query.courses_taught:
		###	  result.append(instructorCourse_to_obj(c))
		###	  for d in c.course_sections:
		###		  result.append(courseSection_to_obj(d))

	if query.user_type == "Admin":
		result = account_to_obj_admin(query)
		

	return jsonify({"status": 1, "person": result})


# create a student account
# creates an account using the given parameters
@app.route(base_url + 'account/student', methods=['POST'])
def create_student():
	account = Student(**request.json)
	if validateNewAccount(account) is False:
		return "One or more required fields contained invalid values", 500
	if exists(account.wsu_email):
		return "An account with that username/email already exists", 500
	account.password = bcrypt.generate_password_hash(account.password).decode('utf-8')
	#print(account.password)
	db.session.add(account)
	db.session.commit()
	db.session.refresh(account)

	return jsonify({"status": 1, "user": account_to_obj_student(account)}), 200
	
	
# creates an instructor account
# creates an account using the given parameters
@app.route(base_url + 'account/instructor', methods=['POST'])
def create_instructor():
	account = Instructor(**request.json)
	if validateNewAccount(account) is False:
		return "One or more required fields contained invalid values", 500
	if exists(account.wsu_email):
		return "An account with that username/email already exists", 500
	account.password = bcrypt.generate_password_hash(account.password).decode('utf-8')
	db.session.add(account)
	db.session.commit()
	db.session.refresh(account)
	
	return jsonify({"status": 1, "user": account_to_obj_instructor(account)}), 200
	

# creates an admin account
# creates an account using the given parameters
@app.route(base_url + 'account/admin', methods=['POST'])
def create_admin():
	account = Admin(**request.json)
	if validateNewAccount(account) is False:
		return "One or more required fields contained invalid values", 500
	if exists(account.wsu_email):
		return "An account with that username/email already exists", 500
	account.password = bcrypt.generate_password_hash(account.password).decode('utf-8')
	db.session.add(account)
	db.session.commit()
	db.session.refresh(account)
	
	return jsonify({"status": 1, "user": account_to_obj_admin(account)}), 200
	
	
# creates a new CoursePreference and adds it to the Student Account associated with the username provided
@app.route(base_url + 'account/student/addCourse', methods=['POST'])
def addCoursePreference():
	course = CoursePreference(**request.json)
	if coursePreferenceValidation(course) is False:
		return "One or more of the required fields were invalid", 500
	username = request.args.get('username', None)
	password = request.args.get('password', None)
	if username is None:
		return "Must provide username", 500
	if password is None:
		return "Must provide password", 500
		
	query = Student.query.filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 500
	prefQuery = CoursePreference.query.filter_by(person_id=query.account_id).filter_by(course_name=course.course_name).first()
	if prefQuery is not None:
		return "A preference for that course already exists", 500
	if (validatePassword(username, password)) is False:
		return "The username or password is incorrect", 500
	
	course.person_id = query.account_id 		#might auto-work due to foreignKey
	query.course_preferences.append(course)	#add this course preference to the student's course_preferences list
	db.session.add(course)
	db.session.commit()
	db.session.refresh(course)
	
	return jsonify({"status": 1, "course": preference_to_obj(course)}), 200
	
	
# given a course preference id, delete it from the database and the Students's preference list
@app.route(base_url + 'account/student/removePreference', methods=['DELETE'])
def removeCoursePreference():
	id = request.args.get('pref_id', None)
	if id is None:
		return "Must provide pref_id", 500
	username = request.args.get('username', None)
	password = request.args.get('password', None)
	if (validatePassword(username, password)) is False:
		return "The username or password is incorrect", 500
	
	pref = CoursePreference.query.filter_by(pref_id=id).first() #obtain the CoursePreference we want to delete
	
	# making sure this CoursePreference will be removed from the Student's list
	for c in pref.student.course_preferences:
		if c.pref_id == id:
			pref.student.course_preferences.remove(c)

	db.session.delete(pref) # remove the CoursePreference from the database
	db.session.commit()
	# do we need a refresh line?

	return jsonify({"status": 1}), 200

	
# creates a new InstructorCourse and adds it to the Instructor account associated with the username provided
@app.route(base_url + 'account/instructor/addCourse', methods=['POST'])
def addInstructorCourse():
	course = InstructorCourse(**request.json)
	if courseValidation(course) is False:
		return "One or more of the required fields were invalid", 500
	username = request.args.get('username', None)
	password = request.args.get('password', None)
	if username is None:
		return "Must provide username", 500
	if password is None:
		return "Must provide password", 500
		
	query = Instructor.query.filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 500
	courseQuery = InstructorCourse.query.filter_by(course_id=query.account_id).filter_by(course_name=course.course_name).first()
	if courseQuery is not None:
		return "An InstructorCourse for that course already exists", 500
	if (validatePassword(username, password)) is False:
		return "The username or password is incorrect", 500
	
	course.person_id = query.account_id
	query.courses_taught.append(course)
	db.session.add(course)
	db.session.commit()
	db.session.refresh(course)
	
	return jsonify({"status": 1, "course": instructorCourse_to_obj(course)}), 200
	
	
# given a course id, delete it from the database and the instructor's courselist
@app.route(base_url + 'account/instructor/removeCourse', methods=['DELETE'])	
def removeInstructorCourse():
	id = request.args.get('course_id', None)
	if id is None:
		return "Must provide course_id", 500
	username = request.args.get('username', None)
	password = request.args.get('password', None)

	if (validatePassword(username, password)) is False:
		return "The username or password is incorrect", 500
	
	course = InstructorCourse.query.filter_by(course_id=id).first() #obtain the InstructorCourse we want to delete
	
	# making sure this InstructorCourse will be removed from the Instructor's list
	for c in course.instructor.courses_taught:
		if c.course_id == id:
			section.course.course_sections.remove(c)
	
	# next we need to remove all course sections from the database that are in this course
	for d in course.course_sections:
		course.course_sections.remove(d)

	db.session.delete(course) # remove the CourseSection from the database
	db.session.commit()
	# do we need a refresh line?

	return jsonify({"status": 1}), 200
	
	
# creates a new CourseSection and adds it to the InstructorCourse class associated with the username provided
@app.route(base_url + 'account/instructor/addCourse/addSection', methods=['POST'])
def addCourseSection():
	section = CourseSection(**request.json)
	if courseSectionValidation(section) is False:
		return "One or more of the required fields were invalid", 507
	username = request.args.get('username', None)
	password = request.args.get('password', None)
	courseName = request.args.get('course', None)
	# all of this 'is None' checking stuff could probably be grouped into another function
	if username is None:
		return "Must provide username", 506
	if password is None:
		return "Must provide password", 505
	if courseName is None:
		return "Must provide a course name (ie. Cpt_S 121)", 504
	query = Instructor.query.filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 503
	
	metaCourse = None
	for c in query.courses_taught:		# this will give us the InstructorCourse that this course section will join to
		if c.course_name == courseName:
			metaCourse = c
			break
	if metaCourse is None:
		return "No course exists with that course name", 502
	
	if (validatePassword(username, password)) is False:
		return "The username or password is incorrect", 501
	
	section.course_id = metaCourse.course_id
	metaCourse.course_sections.append(section)
	db.session.add(section)
	db.session.commit()
	db.session.refresh(section)
	
	return jsonify({"status": 1, "course": courseSection_to_obj(section)}), 200
	
	
# given a course section id, delete it from the database and the InstructorCourse's section list
@app.route(base_url + 'account/instructor/removeCourse/removeSection', methods=['DELETE'])
def removeCourseSection():
	id = request.args.get('section_id', None)
	if id is None:
		return "Must provide section_id", 500
	username = request.args.get('username', None)
	password = request.args.get('password', None)
	#if username is None:
	#	return "Must provide username", 500
	#if password is None:
	#	return "Must provide password", 500
	if (validatePassword(username, password)) is False:
		return "The username or password is incorrect", 500
	
	section = CourseSection.query.filter_by(section_id=id).first() #obtain the CourseSection we want to delete
	
	# making sure this CourseSection will be removed from the InstructorCourse's list
	for c in section.course.course_sections:
		if c.section_id == id:
			section.course.course_sections.remove(c)

	db.session.delete(section) # remove the CourseSection from the database
	db.session.commit()
	# do we need a refresh line?

	return jsonify({"status": 1}), 200
	
	
# updates student profile information with new information
# note, these update functions expect every field to contain a value. The frontend should default each field with the original value
@app.route(base_url + 'account/student/editProfile', methods=['POST'])
def updateStudentInfo():
	info = request.json
	if updateInfoValidation(info, "Student") is False:
		return "One or more of the required fields were invalid", 500
	username = request.args.get('username', None)
	password = request.args.get('password', None)
	if username is None:
		return "Must provide username", 500
	if password is None:
		return "Must provide password", 500
		
	query = Student.query.filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 500
	if (validatePassword(username, password)) is False:
		return "The username or password is incorrect", 500
	
	#---------- begin updating info ------------
	query.wsu_email = info["wsu_email"]
	query.wsu_id = info["wsu_id"]
	query.first_name = info["first_name"]
	query.last_name = info["last_name"]
	query.password = bcrypt.generate_password_hash(info["password"]).decode('utf-8')
	query.secondary_email = info["secondary_email"]
	query.phone_number = info["phone_number"]
	#--
	query.major = info["major"]
	query.gpa = info["gpa"]
	query.expected_grad = info["expected_grad"]
	query.ta_before = info["ta_before"]
	#---------- end updating info ------------
	
	db.session.add(query)
	db.session.commit()
	db.session.refresh(query)
	
	return jsonify({"status": 1, "student": account_to_obj_student(query) }), 200

	
# updates instructor profile information with new information
# note, these update functions expect every field to contain a value. The frontend should default each field with the original value
@app.route(base_url + 'account/instructor/editProfile', methods=['POST'])
def updateInstructorInfo():
	info = request.json
	if updateInfoValidation(info, "Instructor") is False:
		return "One or more of the required fields were invalid", 500
	username = request.args.get('username', None)
	password = request.args.get('password', None)
	if username is None:
		return "Must provide username", 500
	if password is None:
		return "Must provide password", 500
		
	query = Instructor.query.filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 500
	if (validatePassword(username, password)) is False:
		return "The username or password is incorrect", 500
	
	#---------- begin updating info ------------
	query.wsu_email = info["wsu_email"]
	query.wsu_id = info["wsu_id"]
	query.first_name = info["first_name"]
	query.last_name = info["last_name"]
	query.password = bcrypt.generate_password_hash(info["password"]).decode('utf-8')
	query.secondary_email = info["secondary_email"]
	query.phone_number = info["phone_number"]
	#--
	#---------- end updating info ------------
	
	db.session.add(query)
	db.session.commit()
	db.session.refresh(query)
	
	return jsonify({"status": 1, "instructor": account_to_obj_instructor(query) }), 200
	
	
# returns all of a given student's course preferences
@app.route(base_url + 'account/student/coursePreferences', methods=['GET'])
def getCoursePreferences():
	username = request.args.get('username', None)
	if username is None:
		return "Must provide username", 500
	query = Student.query.filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 500
	
	result = []
	for c in query.course_preferences:
		result.append(preference_to_obj(c))
		
	return jsonify({"status": 1, "student": result})
		
		
# returns all of a given instructor's course preferences
@app.route(base_url + 'account/instructor/courses', methods=['GET'])
def getCoursesTaught():
	username = request.args.get('username', None)
	if username is None:
		return "Must provide username", 500
	query = Instructor.query.filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 500
	
	result = []
	for c in query.courses_taught:
		result.append(instructorCourse_to_obj(c))
		#for d in c.course_sections:
		#	result.append(courseSection_to_obj(d))
		
	return jsonify({"status": 1, "instructor": result})
	

	
		
	
#---------- lower priority -----------------	

def applyForTA():	# function for adding a TAApplication to a course section
	pass
	
	
	
#--------------------------------------------- Testing Functions ----------------------------------------------
#	These are functions that are used for the automated testing; they can be used if needed, but were created for
#	the intent of testing. 
#-----------------------------------------------------------------------------------------------------------------
	

# This is a function created for testing purposes, used to see what accounts currently exist in the database.
@app.route(base_url + 'account/getAll', methods=['GET'])
def getAllAccounts():
	space = request.args.get('space', None)
	if space is None:
		return "Must provide space", 500
	students = Student.query.filter_by(space=space).all()
	instructors = Instructor.query.filter_by(space=space).all()
	admins = Admin.query.filter_by(space=space).all()
	
	result = []
	for s in students:
		result.append(account_to_obj_student(s))
	for i in instructors:
		result.append(account_to_obj_instructor(i))
	for a in admins:
		result.append(account_to_obj_admin(a))
	
	return jsonify({"status": 1, "all accounts": result})
	
	
#Purely for use in testing. REMEMBER to comment it out when released. Deletes all accounts in a given space.
@app.route(base_url + 'account', methods=['DELETE'])
def deleteAllAccounts():
	space = request.args.get('space', None) 
	if space is None:
		return "Must provide space", 500

	Student.query.filter_by(space=space).delete()
	Instructor.query.filter_by(space=space).delete()
	Admin.query.filter_by(space=space).delete()
	InstructorCourse.query.delete()
	CoursePreference.query.delete()
	CourseSection.query.delete()
	
	db.session.commit()
	
	return jsonify({"status": 1}), 200
	
	
@app.route(base_url + 'account/getAllCoursePref', methods=['GET'])
def getAllCoursePref():
	preferences = CoursePreference.query.all()
	
	result = []
	for c in preferences:
		result.append(preference_to_obj(c))
	
	return jsonify({"status": 1, "all_CoursePref": result})
	
	
@app.route(base_url + 'account/getAllInstructorCourses', methods=['GET'])
def getAllInstructorCourses():
	courses = InstructorCourse.query.all()
	
	result = []
	for c in courses:
		result.append(instructorCourse_to_obj(c))
	
	return jsonify({"status": 1, "all_InstructorCourses": result})
	
	
@app.route(base_url + 'account/getAllCourseSections', methods=['GET'])
def getAllCourseSections():
	sections = CourseSection.query.all()
	
	result = []
	for c in sections:
		result.append(courseSection_to_obj(c))
	
	return jsonify({"status": 1, "all_CourseSections": result})
	
#--------------------------------------------- Validation Functions ----------------------------------------------
#	These are functions that are used for validating information; checking if something exists, is null, 
#	making sure all fields are filled out correctly, checking the password (outside of logging in), etc.
#-----------------------------------------------------------------------------------------------------------------
	
	
# a commonly-called function that takes a username and password and confirms if they are correct; should be called before 
# changing anything in a user's account.
#
# 	NOTE: because the password stored in the database is the encrypted one, this compares a passed-in password with the encrypted password.
#	However, upon login, userData in the taLink.js file stores the encrypted password; that is what should be sent into any function that
#	calls this one. If all is done correctly, the passwords should match. I can't test this perfectly until the .js functions are done, though.
def validatePassword(username, password):	
	if username is None:
		return False
	if password is None:
		return False
	query = Student.query.filter_by(wsu_email=username).first()
	if query is None:
		query = Instructor.query.filter_by(wsu_email=username).first()
	if query is None:
		query = Admin.query.filter_by(wsu_email=username).first()
	if query is None:
		return False	# account does not exist
		
	if query.password != password:
		return False	# passwords do not match	
#	if bcrypt.check_password_hash(query.password, password) == False:
#		return False

	return True
	
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
	

# makes sure the updated info for each Student field won't cause problems when overwriting
# the original values. Returns False if there is a problem, True otherwise.
# for right now, it only makes sure each field has a value.
def updateStudentInfoValidation(data):

	if data["major"] is None or data["major"] == "":
		return False
	if data["gpa"] is None or data["gpa"] == "":
		return False
	if data["expected_grad"] is None or data["expected_grad"] == "":
		return False
	if data["ta_before"] is None or data["ta_before"] == "":
		return False
	return True

	
# makes sure the updated info for each shared Student/Instructor/Admin field won't cause
# problems when overwriting the original values. Returns False if there is a problem, True otherwise.
# for right now, it only makes sure each field has a value.
def updateInfoValidation(data, userType):
	
	#if exists(data["wsu_email"]) is True:	#checking if the new username already exists
	#	return False
	if data["wsu_email"] is None or data["wsu_email"] == "":
		return False
	if data["wsu_id"] is None or data["wsu_id"] == "":
		return False
	if data["first_name"] is None or data["first_name"] == "":
		return False
	if data["last_name"] is None or data["last_name"] == "":
		return False
	if data["password"] is None or data["password"] == "":
		return False
	if data["phone_number"] is None or data["phone_number"] == "":	# is phone number required? If not, go ahead and delete this one
		return False
	if userType == "Student":
		return updateStudentInfoValidation(data)	# if we are updating Student info, call that function and return its value
													# because it's the end of this function, it can just return the return value
	return True
	

# validates a given CourseSection to ensure each required field has a valid value.
def courseSectionValidation(data):

	if data.section_name is None or data.section_name == "":
		return False
	if data.days_lecture is None or data.days_lecture == "":
		return False
	if data.time_lecture is None or data.time_lecture == "":
		return False
	#if data.ta_chosen != True and data.section_name != False:
	#	return False
	return True
	
# validates a given InstructorCourse to ensure each required field has a valid value.
def courseValidation(data):
	
	if data.course_name is None or data.course_name == "":
		return False
	if data.semester is None or data.semester == "":
		return False
	return True
	
# validates a given CoursePreference to ensure each required field has a valid value.	
def coursePreferenceValidation(data):
	
	if data.course_name is None or data.course_name == "":
		return False
	if data.grade_earned is None or data.grade_earned == "":
		return False
	if data.date_taken is None or data.date_taken == "":
		return False
	if data.ta_before != False and data.ta_before != True:
		return False
	return True
	
	
def validateNewAccount(account):
	
	if account.user_type is None or account.user_type == "":
		return False
	if account.wsu_id is None or account.wsu_id == "":
		return False
	if account.space is None or account.space == "":
		return False
	if account.first_name is None or account.first_name == "":
		return False
	if account.last_name is None or account.last_name == "":
		return False
	if account.wsu_email is None or account.wsu_email == "":
		return False
	if account.password is None or account.password == "":
		return False
	if account.phone_number is None or account.phone_number == "":
		return False
	if account.user_type == "Student":
		return validateNewStudent(account)
	return True
	
def validateNewStudent(account):
	if account.major is None or account.major == "":
		return False
	if account.gpa is None or account.gpa == "":
		return False
	if account.expected_grad is None or account.expected_grad == "":
		return False
	if account.ta_before is None or account.ta_before == "":
		return False
	return True

#----------------------------------------- [row to object / account to obj] definitions --------------------------
#	These definitions convert a class' information into a readable json format
#-----------------------------------------------------------------------------------------------------------------

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
	
	
def preference_to_obj(course):
    course = {
			"pref_id": course.pref_id,
			"person_id": course.person_id,
			"course_name": course.course_name,
			"grade_earned": course.grade_earned,
			"date_taken": course.date_taken,
			"ta_before": course.ta_before
        }
    return course
	
def instructorCourse_to_obj(course):
	sections = []
	for c in course.course_sections:
		sections.append(courseSection_to_obj(c))
	
	course = {
			"course_id": course.course_id,
			"first_name": course.instructor.first_name,
			"last_name": course.instructor.last_name,
			"person_id": course.person_id,
			"course_name": course.course_name,
			"semester": course.semester,
			"course_sections": sections
		}
	return course
	
def courseSection_to_obj(section):
    section = {
			"section_id": section.section_id,
			"course_id": section.course_id,
			"section_name": section.section_name,
			"days_lecture": section.days_lecture,
			"time_lecture": section.time_lecture,
			"ta_chosen": section.ta_chosen
        }
    return section
	

#---------------------------------------Don't [edit] anything below this line unless you know what you're doing-------------------------------------
  
  
def main():
    db.create_all() # creates the tables you've provided
    app.run()       # runs the Flask application


if __name__ == '__main__':
    main()
