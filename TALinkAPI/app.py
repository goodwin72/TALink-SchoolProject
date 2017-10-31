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
	
	#note, to get the course's instructor, you should be able to use [CourseSectionObject].course.instructor.first_name, etc.
	# as such, I don't see the need for a specific "instructor name" field. Though, you can add one if the above doesn't work.
	
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
	result = []
	if query.user_type == "Student":
		result.append(account_to_obj_student(query))
		###for c in query.course_preferences:
		###	  result.append(preference_to_obj(c))
	
	if query.user_type == "Instructor":
		result.append(account_to_obj_instructor(query))
		###for c in query.courses_taught:
		###	  result.append(instructorCourse_to_obj(c))
		###	  for d in c.course_sections:
		###		  result.append(courseSection_to_obj(d))

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
	#print(account.password)
	db.session.add(account)
	db.session.commit()
	db.refresh(account)

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
	db.refresh(account)
	
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
	db.refresh(account)
	
	return jsonify({"status": 1, "user": account_to_obj_admin(account)}), 200
	
	
# creates a new CoursePreference and adds it to the Student Account associated with the username provided
@app.route(base_url + 'account/student/addCourse', methods=['POST'])
def addCoursePreference():
	course = CoursePreference(**request.json)
	#insert coursepref validation testing here
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
	#if (validatePassword(username, password)) is False:
	#	return "The username or password is incorrect", 500
	
	course.person_id = query.account_id 		#might auto-work due to foreignKey
	query.course_preferences.append(course)	#add this course preference to the student's course_preferences list
	db.session.add(course)
	db.session.commit()
	db.session.refresh(course)
	
	return jsonify({"status": 1, "course": preference_to_obj(course)}), 200
	
def removeCoursePreference():
	pass

# creates a new InstructorCourse and adds it to the Instructor account associated with the username provided
@app.route(base_url + 'account/instructor/addCourse', methods=['POST'])
def addInstructorCourse():
	course = InstructorCourse(**request.json)
	#insert instructorcourse validation testing here
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
	#if (validatePassword(username, password)) is False:
	#	return "The username or password is incorrect", 500
	
	course.person_id = query.account_id
	query.courses_taught.append(course)
	db.session.add(course)
	db.session.commit()
	db.session.refresh(course)
	
	return jsonify({"status": 1, "course": instructorCourse_to_obj(course)}), 200
	
def removeInstructorCourse():
	pass
	
# creates a new CourseSection and adds it to the InstructorCourse class associated with the username provided
@app.route(base_url + 'account/instructor/addCourse/addSection', methods=['POST'])
def addCourseSection():
	section = CourseSection(**request.json)
	#insert instructorcourse validation testing here
	username = request.args.get('username', None)
	password = request.args.get('password', None)
	courseName = request.args.get('course', None)
	# all of this 'is None' checking stuff could probably be grouped into another function; consider doing so later
	if username is None:
		return "Must provide username", 500
	if password is None:
		return "Must provide password", 500
	if courseName is None:
		return "Must provide a course name (ie. Cpt_S 121)", 500
	query = Instructor.query.filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 500
	
	metaCourse = None
	for c in query.courses_taught:		# this will give us the InstructorCourse that this course section will join to
		if c.course_name == courseName:
			metaCourse = c
			break
	if metaCourse is None:
		return "No course exists with that course name", 500
	
	#if (validatePassword(username, password)) is False:
	#	return "The username or password is incorrect", 500
	
	section.course_id = metaCourse.course_id
	metaCourse.course_sections.append(section)
	db.session.add(section)
	db.session.commit()
	db.session.refresh(section)
	
	return jsonify({"status": 1, "course": courseSection_to_obj(section)}), 200
	
	
def removeCourseSection():
	pass
	
	
# updates student profile information with new information
# note, these update functions expect every field to contain a value. The frontend should default each field with the original value
@app.route(base_url + 'account/student/editProfile', methods=['POST'])
def updateStudentInfo():
	info = request.json
	#insert validation testing here
	username = request.args.get('username', None)
	password = request.args.get('password', None)
	if username is None:
		return "Must provide username", 500
	if password is None:
		return "Must provide password", 500
		
	query = Student.query.filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 500
	#if (validatePassword(username, password)) is False:
	#	return "The username or password is incorrect", 500
	
	#---------- begin updating info ------------
	query.wsu_id = info["wsu_id"]
	query.first_name = info["first_name"]
	query.last_name = info["last_name"]
	query.password = info["password"]
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
	#insert validation testing here
	username = request.args.get('username', None)
	password = request.args.get('password', None)
	if username is None:
		return "Must provide username", 500
	if password is None:
		return "Must provide password", 500
		
	query = Instructor.query.filter_by(wsu_email=username).first()
	if query is None:
		return "No account exists with the given username", 500
	#if (validatePassword(username, password)) is False:
	#	return "The username or password is incorrect", 500
	
	#---------- begin updating info ------------
	query.wsu_id = info["wsu_id"]
	query.first_name = info["first_name"]
	query.last_name = info["last_name"]
	query.password = info["password"]
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
def instructorCourseSearch():
	pass

def applyForTA():
	pass
	
def editApplications():
	pass
	
	
	
	
#--------------------------------------------- Validation Functions ----------------------------------------------
#	These are functions that are used for validating information; checking if something exists, is null, 
#	making sure all fields are filled out correctly, checking the password (outside of logging in), etc.
#-----------------------------------------------------------------------------------------------------------------
	
	
# a commonly-called function that takes a username and password and confirms if they are correct; should be called before 
# changing anything in a user's account.
def validatePassword(username, password):	
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
