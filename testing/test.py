
"""
Note: Will switch redundant code to helper functions in iteration 3. Ran out of time for clean up.
"""

import unittest
import os
import testLib

class TestTALink(testLib.AccountTestCase):

	###
	### THESE ARE THE ACTUAL TESTS
	###
	
	def testCreateStudent1(self):
		"""
		Test creating a student account
		"""
		respCreate = self.makeRequest("/api/account/student", method="POST",
                                    data = { 'user_type' : 'Student',
											 'wsu_id' : '112233445',
                                             'space' : self.accountSpace,
                                             'first_name' : 'John',
											 'last_name' : 'Doe',
											 'wsu_email' : 'john.doe@wsu.edu',
											 'password' : 'test',
											 'secondary_email' : "",
											 'phone_number' : '111-222-3333',
											 #---student-specific stuff below
											 'major' : 'BS Computer Science',
											 'gpa' : 3.6,
											 'expected_grad' : 'Fall 2020',
											 'ta_before' : False
                                             })
		self.assertSuccessResponse(respCreate)
		self.assertEqual(3.6, respCreate['user']['gpa'])	#confirming the returned result contained correct data
		self.assertEqual('John', respCreate['user']['first_name'])
		
		respGet = self.getAccounts()
		self.assertSuccessResponse(respGet)
		self.assertEqual(1, len(respGet['all_accounts']))	#Ensuring only one account was made
		self.assertEqual(respCreate['user']['account_id'], respGet['all_accounts'][0]['account_id'])
			#Making sure the account created was populated with the correct account id (1)
			
			
	def testCreateInstructor1(self):
		"""
		Test creating a instructor account
		"""
		respCreate = self.makeRequest("/api/account/instructor", method="POST",
                                    data = { 'user_type' : 'Instructor',
											 'wsu_id' : '1234567890',
                                             'space' : self.accountSpace,
                                             'first_name' : 'Johnny',
											 'last_name' : 'Doey',
											 'wsu_email' : 'johnny.doey@wsu.edu',
											 'password' : 'test2',
											 'secondary_email' : "",
											 'phone_number' : '112-223-3334'
                                             })
		self.assertSuccessResponse(respCreate)
		self.assertEqual('112-223-3334', respCreate['user']['phone_number'])	#confirming the returned result contained correct data
		self.assertEqual('Johnny', respCreate['user']['first_name'])
		
		respGet = self.getAccounts()
		self.assertSuccessResponse(respGet)
		self.assertEqual(1, len(respGet['all_accounts']))	#Ensuring only one account was made
		self.assertEqual(respCreate['user']['account_id'], respGet['all_accounts'][0]['account_id'])
			#Making sure the account created was populated with the correct account id

			
	def testLoginInstructor1(self):
		"""
		Test logging into an instructor account
		"""
		respCreate = self.makeRequest("/api/account/instructor", method="POST",
                                    data = { 'user_type' : 'Instructor',
											 'wsu_id' : '1234567890',
                                             'space' : self.accountSpace,
                                             'first_name' : 'Johnny',
											 'last_name' : 'Doey',
											 'wsu_email' : 'johnny.doey@wsu.edu',
											 'password' : 'test2',
											 'secondary_email' : "",
											 'phone_number' : '112-223-3334'
                                             })
											 
		self.assertSuccessResponse(respCreate)
		self.assertEqual('112-223-3334', respCreate['user']['phone_number'])	#confirming the returned result contained correct data
		self.assertEqual('Johnny', respCreate['user']['first_name'])
		
		#Now we will login, and confirm if the recieved data is the account we just made
		#Note: we must hard-code the password because respCreate contains the encrypted password, while the login func expects decrypted
		#This is intentional. Also note that this only holds true for logging in.
		tUrl = "/api/account?space="+self.accountSpace+"&username="+respCreate['user']['wsu_email']+"&password=test2"
		respGet = self.makeRequest(tUrl, method="GET")
		self.assertSuccessResponse(respGet)
		self.assertEqual('112-223-3334', respGet['person']['phone_number'])	#confirming the returned result contained correct data
		self.assertEqual('Johnny', respGet['person']['first_name'])
		
	def testLoginStudent1(self):
		"""
		Test logging into a student account
		"""
		respCreate = self.makeRequest("/api/account/student", method="POST",
                                    data = { 'user_type' : 'Student',
											 'wsu_id' : '112233445',
                                             'space' : self.accountSpace,
                                             'first_name' : 'John',
											 'last_name' : 'Doe',
											 'wsu_email' : 'john.doe@wsu.edu',
											 'password' : 'test',
											 'secondary_email' : "",
											 'phone_number' : '111-222-3333',
											 #---student-specific stuff below
											 'major' : 'BS Computer Science',
											 'gpa' : 3.6,
											 'expected_grad' : 'Fall 2020',
											 'ta_before' : False
                                             })
		self.assertSuccessResponse(respCreate)
		self.assertEqual(3.6, respCreate['user']['gpa'])	#confirming the returned result contained correct data
		self.assertEqual('John', respCreate['user']['first_name'])
		
		#Now we will login, and confirm if the recieved data is the account we just made
		#Note: we must hard-code the password because respCreate contains the encrypted password, while the login func expects decrypted
		#This is intentional.
		tUrl = "/api/account?space="+self.accountSpace+"&username="+respCreate['user']['wsu_email']+"&password=test"
		respGet = self.makeRequest(tUrl, method="GET")
		self.assertSuccessResponse(respGet)
		self.assertEqual(3.6, respGet['person']['gpa'])	#confirming the returned result contained correct data
		self.assertEqual('John', respGet['person']['first_name'])
		
	def testAddCoursePreference(self):
		"""
		Test adding a course preference to a student account
		"""
		respCreate = self.makeRequest("/api/account/student", method="POST",
                                    data = { 'user_type' : 'Student',
											 'wsu_id' : '112233445',
                                             'space' : self.accountSpace,
                                             'first_name' : 'John',
											 'last_name' : 'Doe',
											 'wsu_email' : 'john.doe@wsu.edu',
											 'password' : 'test',
											 'secondary_email' : "",
											 'phone_number' : '111-222-3333',
											 #---student-specific stuff below
											 'major' : 'BS Computer Science',
											 'gpa' : 3.6,
											 'expected_grad' : 'Fall 2020',
											 'ta_before' : False
                                             })
		self.assertSuccessResponse(respCreate)
		self.assertEqual(3.6, respCreate['user']['gpa'])	#confirming the returned result contained correct data
		self.assertEqual('John', respCreate['user']['first_name'])
		
		#Now we will test adding a course preference
		tUrl = "/api/account/student/addCourse?username="+respCreate['user']['wsu_email']+"&password="+respCreate['user']['password']
		respPref = self.makeRequest(tUrl, method="POST",
									data = { 'course_name' : 'CptS 322',
											 'grade_earned' : 'A',
											 'date_taken' : 'Fall 2019',
											 'ta_before' : False
											})
		self.assertEqual('CptS 322', respPref['course']['course_name'])
		self.assertEqual(False, respPref['course']['ta_before'])
		
		#Now we make sure the course preference was added to the student's account
		tUrl = "api/account/student/coursePreferences?username="+respCreate['user']['wsu_email']
		respGet = self.makeRequest(tUrl, method="GET")
		self.assertEqual('CptS 322', respGet['student'][0]['course_name'])
		self.assertEqual(False, respGet['student'][0]['ta_before'])
		
	def testAddInstructorCourse(self):
		"""
		Test adding an InstructorCourse to an Instructor's account
		"""
		respCreate = self.makeRequest("/api/account/instructor", method="POST",
                                    data = { 'user_type' : 'Instructor',
											 'wsu_id' : '1234567890',
                                             'space' : self.accountSpace,
                                             'first_name' : 'Johnny',
											 'last_name' : 'Doey',
											 'wsu_email' : 'johnny.doey@wsu.edu',
											 'password' : 'test2',
											 'secondary_email' : "",
											 'phone_number' : '112-223-3334'
                                             })
											 
		self.assertSuccessResponse(respCreate)
		self.assertEqual('112-223-3334', respCreate['user']['phone_number'])	#confirming the returned result contained correct data
		self.assertEqual('Johnny', respCreate['user']['first_name'])
		
		#Now we will test adding an instructor course
		tUrl = "/api/account/instructor/addCourse?username="+respCreate['user']['wsu_email']+"&password="+respCreate['user']['password']
		respPref = self.makeRequest(tUrl, method="POST",
									data = { 'course_name' : 'CptS_322',
											 'section_name' : '01 Lab',
											 'semester' : 'Fall',
										  	 'days_lecture': 'N/A',
										  	 'time_lecture': 'N/A'
											})
		self.assertEqual('CptS_322', respPref['course']['course_name'])
		self.assertEqual('Fall', respPref['course']['semester'])
		
		#Now we make sure the instructor course was added to the instructors's account
		tUrl = "api/account/instructor/courses?username="+respCreate['user']['wsu_email']
		respGet = self.makeRequest(tUrl, method="GET")
		self.assertEqual('CptS_322', respGet['instructor'][0]['course_name'])
		self.assertEqual('Fall', respGet['instructor'][0]['semester'])

		
	def testUpdateInfoInstructor(self):
		"""
		Test updating an Instructor's information
		"""
		respCreate = self.makeRequest("/api/account/instructor", method="POST",
                                    data = { 'user_type' : 'Instructor',
											 'wsu_id' : '1234567890',
                                             'space' : self.accountSpace,
                                             'first_name' : 'Johnny',
											 'last_name' : 'Doey',
											 'wsu_email' : 'johnny.doey@wsu.edu',
											 'password' : 'test2',
											 'secondary_email' : "",
											 'phone_number' : '112-223-3334'
                                             })
											 
		self.assertSuccessResponse(respCreate)
		self.assertEqual('112-223-3334', respCreate['user']['phone_number'])	#confirming the returned result contained correct data
		self.assertEqual('Johnny', respCreate['user']['first_name'])
		
		#Now we'll update the information	
		respUpdate = self.makeRequest("/api/account/instructor/editProfile?username="+respCreate['user']['wsu_email']+"&password="+respCreate['user']['password'], method="POST",
                                    data = { 'user_type' : 'Instructor',
											 'wsu_id' : '1111111111',
                                             'first_name' : 'Johnny2',
											 'last_name' : 'Doey2',
											 'wsu_email' : 'johnny.doey@wsu.edu',
											 'password' : 'test3',
											 'secondary_email' : "HelloWorld@gmail.com",
											 'phone_number' : '111-111-1111'
                                             })
		self.assertSuccessResponse(respUpdate)
		self.assertEqual('111-111-1111', respUpdate['instructor']['phone_number'])	#confirming the returned result contained correct data
		self.assertEqual('HelloWorld@gmail.com', respUpdate['instructor']['secondary_email'])
		
		#Next, make sure that the information was correctly updated in the database by logging in
		tUrl = "/api/account?space="+self.accountSpace+"&username="+respCreate['user']['wsu_email']+"&password=test3"
		respGet = self.makeRequest(tUrl, method="GET")
		self.assertSuccessResponse(respGet)
		self.assertEqual('111-111-1111', respGet['person']['phone_number'])	#confirming the returned result contained correct data
		self.assertEqual('HelloWorld@gmail.com', respGet['person']['secondary_email'])
		
		
	def testUpdateInfoStudent(self):
		"""
		Test updating an Student's information
		"""
		respCreate = self.makeRequest("/api/account/student", method="POST",
                                    data = { 'user_type' : 'Student',
											 'wsu_id' : '112233445',
                                             'space' : self.accountSpace,
                                             'first_name' : 'John',
											 'last_name' : 'Doe',
											 'wsu_email' : 'john.doe@wsu.edu',
											 'password' : 'test',
											 'secondary_email' : "",
											 'phone_number' : '111-222-3333',
											 #---student-specific stuff below
											 'major' : 'BS Computer Science',
											 'gpa' : 3.6,
											 'expected_grad' : 'Fall 2020',
											 'ta_before' : False
                                             })
		self.assertSuccessResponse(respCreate)
		self.assertEqual(3.6, respCreate['user']['gpa'])	#confirming the returned result contained correct data
		self.assertEqual('John', respCreate['user']['first_name'])
		
		#Now we'll update the information	
		respUpdate = self.makeRequest("/api/account/student/editProfile?username="+respCreate['user']['wsu_email']+"&password="+respCreate['user']['password'], method="POST",
                                    data = { 'user_type' : 'Student',
											 'wsu_id' : '1111111111',
                                             'first_name' : 'Johnny2',
											 'last_name' : 'Doey2',
											 'wsu_email' : 'john.doe@wsu.edu',
											 'password' : 'test3',
											 'secondary_email' : "HelloWorld@gmail.com",
											 'phone_number' : '111-111-1111',
											 'major' : 'BA Computer Science',
											 'gpa' : 3.4,
											 'expected_grad' : 'Fall 2021',
											 'ta_before' : True
                                             })
		self.assertSuccessResponse(respUpdate)
		self.assertEqual(3.4, respUpdate['student']['gpa'])	#confirming the returned result contained correct data
		self.assertEqual(True, respUpdate['student']['ta_before'])
		
		#Next, make sure that the information was correctly updated in the database by logging in
		tUrl = "/api/account?space="+self.accountSpace+"&username="+respCreate['user']['wsu_email']+"&password=test3"
		respGet = self.makeRequest(tUrl, method="GET")
		self.assertSuccessResponse(respGet)
		self.assertEqual(3.4, respGet['person']['gpa'])	#confirming the returned result contained correct data
		self.assertEqual(True, respGet['person']['ta_before'])

	
	def testRemoveCoursePreference(self):
		"""
		Test removing a course preference to a student account
		"""
		respCreate = self.makeRequest("/api/account/student", method="POST",
                                    data = { 'user_type' : 'Student',
											 'wsu_id' : '112233445',
                                             'space' : self.accountSpace,
                                             'first_name' : 'John',
											 'last_name' : 'Doe',
											 'wsu_email' : 'john.doe@wsu.edu',
											 'password' : 'test',
											 'secondary_email' : "",
											 'phone_number' : '111-222-3333',
											 #---student-specific stuff below
											 'major' : 'BS Computer Science',
											 'gpa' : 3.6,
											 'expected_grad' : 'Fall 2020',
											 'ta_before' : False
                                             })
		self.assertSuccessResponse(respCreate)
		self.assertEqual(3.6, respCreate['user']['gpa'])	#confirming the returned result contained correct data
		self.assertEqual('John', respCreate['user']['first_name'])
		
		#Now we will test adding a course preference
		tUrl = "/api/account/student/addCourse?username="+respCreate['user']['wsu_email']+"&password="+respCreate['user']['password']
		respPref = self.makeRequest(tUrl, method="POST",
									data = { 'course_name' : 'CptS 322',
											 'grade_earned' : 'A',
											 'date_taken' : 'Fall 2019',
											 'ta_before' : False
											})
		self.assertEqual('CptS 322', respPref['course']['course_name'])
		self.assertEqual(False, respPref['course']['ta_before'])
	
		
		#Now we will test removing the course preference
		tUrl = "/api/account/student/removePreference?username="+respCreate['user']['wsu_email']+"&password="+respCreate['user']['password']+"&pref_id="+str(respPref['course']['pref_id'])
		respRemove = self.makeRequest(tUrl, method="DELETE")
		self.assertSuccessResponse(respRemove)
		#make sure the coursePreference isn't in the student's account
		tUrl = "/api/account/student/coursePreferences?username="+respCreate['user']['wsu_email']
		respGet = self.makeRequest(tUrl, method="GET")
		self.assertSuccessResponse(respGet)
		self.assertEqual([], respGet['student'])
		#make sure the coursePreference isn't in the database still
		tUrl = "/api/account/getAllCoursePref"
		respGet = self.makeRequest(tUrl, method="GET")
		self.assertSuccessResponse(respGet)
		self.assertEqual([], respGet['all_CoursePref'])
		
		

	def testRemoveInstructorCourse(self):
		"""
		Test removing an InstructorCourse to an Instructor's account
		"""
		respCreate = self.makeRequest("/api/account/instructor", method="POST",
                                    data = { 'user_type' : 'Instructor',
											 'wsu_id' : '1234567890',
                                             'space' : self.accountSpace,
                                             'first_name' : 'Johnny',
											 'last_name' : 'Doey',
											 'wsu_email' : 'johnny.doey@wsu.edu',
											 'password' : 'test2',
											 'secondary_email' : "",
											 'phone_number' : '112-223-3334'
                                             })
											 
		self.assertSuccessResponse(respCreate)
		self.assertEqual('112-223-3334', respCreate['user']['phone_number'])	#confirming the returned result contained correct data
		self.assertEqual('Johnny', respCreate['user']['first_name'])
		
		#Now we will test adding an instructor course
		tUrl = "/api/account/instructor/addCourse?username="+respCreate['user']['wsu_email']+"&password="+respCreate['user']['password']
		respPref = self.makeRequest(tUrl, method="POST",
									data = { 'course_name' : 'CptS_322',
											 'section_name' : '01 Lab',
											 'semester' : 'Fall',
										  	 'days_lecture': 'N/A',
										  	 'time_lecture': 'N/A'
											})
		self.assertEqual('CptS_322', respPref['course']['course_name'])
		self.assertEqual('Fall', respPref['course']['semester'])
		
		#Now we will test removing the InstructorCourse
		tUrl = "/api/account/instructor/removeCourse?username="+respCreate['user']['wsu_email']+"&password="+respCreate['user']['password']+"&course_id="+str(respPref['course']['course_id'])
		respRemove = self.makeRequest(tUrl, method="DELETE")
		self.assertSuccessResponse(respRemove)
		#make sure the instructorcourse isn't in the instructor account
		tUrl = "/api/account/instructor/courses?username="+respCreate['user']['wsu_email']
		respGet = self.makeRequest(tUrl, method="GET")
		self.assertSuccessResponse(respGet)
		self.assertEqual([], respGet['instructor'])
		#make sure the instructorcourse isn't in the database still
		tUrl = "/api/account/getAllInstructorCourses"
		respGet = self.makeRequest(tUrl, method="GET")
		self.assertSuccessResponse(respGet)
		self.assertEqual([], respGet['all_InstructorCourses'])

	def testTAApplications(self):
		"""
		Test adding TA Applications, removing them, setting a TA and removing a TA
		"""
		# First, we create an instructor and a student account to work with
		respCreateI = self.makeRequest("/api/account/instructor", method="POST",
									  data={'user_type': 'Instructor',
											'wsu_id': '1234567890',
											'space': self.accountSpace,
											'first_name': 'Johnny',
											'last_name': 'Doey',
											'wsu_email': 'johnny.doey@wsu.edu',
											'password': 'test2',
											'secondary_email': "",
											'phone_number': '112-223-3334'
											})

		self.assertSuccessResponse(respCreateI)
		self.assertEqual('112-223-3334',
						 respCreateI['user']['phone_number'])  # confirming the returned result contained correct data
		self.assertEqual('Johnny', respCreateI['user']['first_name'])

		respCreateS = self.makeRequest("/api/account/student", method="POST",
									   data={'user_type': 'Student',
											 'wsu_id': '112233445',
											 'space': self.accountSpace,
											 'first_name': 'Bob',
											 'last_name': 'Pop',
											 'wsu_email': 'john.doe@wsu.edu',
											 'password': 'test',
											 'secondary_email': "",
											 'phone_number': '115-225-3335',
											 # ---student-specific stuff below
											 'major': 'BS Computer Science',
											 'gpa': 3.6,
											 'expected_grad': 'Fall 2020',
											 'ta_before': False
											 })

		self.assertSuccessResponse(respCreateS)
		self.assertEqual('115-225-3335',
						 respCreateS['user']['phone_number'])  # confirming the returned result contained correct data
		self.assertEqual('Bob', respCreateS['user']['first_name'])

		# Now we will test adding an instructor course
		tUrl = "/api/account/instructor/addCourse?username=" + respCreateI['user']['wsu_email'] + "&password=" + \
			   respCreateI['user']['password']
		respCourse= self.makeRequest(tUrl, method="POST",
									data={'course_name': 'CptS_322',
										  'semester': 'Fall',
										  'days_lecture': 'N/A',
										  'time_lecture': 'N/A'
										  })
		self.assertEqual('CptS_322', respCourse['course']['course_name'])
		self.assertEqual('Fall', respCourse['course']['semester'])

		# Now we have the student apply to the course
		tUrl = "/api/account/student/addApp?username=" + respCreateS['user']['wsu_email'] + "&password=" + \
		   respCreateS['user']['password'] + "&course_ids=1"
		respApp= self.makeRequest(tUrl, method="POST",
									data={'student_name': 'Bob Pop',
										  'wsu_sid': '112233445',
										  'grade_earned': 'A',
										  'date_taken': 'Fall 2017',
										  'ta_before': False
										  })
		self.assertEqual('Bob Pop', respApp['application']['student_name'])
		self.assertEqual('A', respApp['application']['grade_earned'])

		# Next, we make sure both the student account and instructorCourse have this application
		tUrl = "/api/account/instructor/courses/applications?course_id=1"
		respInstCourse= self.makeRequest(tUrl, method="GET")
		tUrl = "/api/account/student/applications?username=" + respCreateS['user']['wsu_email']
		respStudent= self.makeRequest(tUrl, method="GET")
		self.assertEqual('Bob Pop', respInstCourse['applications'][0]['student_name'])
		self.assertEqual('Bob Pop', respStudent['applications'][0]['student_name'])

		# Next, we have the Instructor accept TAship, and then test if the course and the student were updated
		tUrl = "/api/account/instructor/course/chooseTA?username=" + respCreateS['user']['wsu_email'] + "&password=" + \
		   respCreateS['user']['password'] + "&app_id=1"
		respTA = self.makeRequest(tUrl, method="POST")
		tUrl = "/api/account/getAllInstructorCourses"
		respInstCourse= self.makeRequest(tUrl, method="GET")
		tUrl = "/api/account/getAll?space=" + self.accountSpace
		respStudent= self.makeRequest(tUrl, method="GET")
		self.assertEqual(True, respStudent['all_accounts'][0]['assigned_ta'])
		self.assertEqual('Bob Pop', respInstCourse['all_InstructorCourses'][0]['ta_name'])

		# Next, we test removing the student from TAship
		tUrl = "/api/account/instructor/course/removeTA?username=" + respCreateS['user']['wsu_email'] + "&password=" + \
			   respCreateS['user']['password'] + "&course_id=1"
		respRemoveTA = self.makeRequest(tUrl, method="POST")
		tUrl = "/api/account/getAllInstructorCourses"
		respInstCourse= self.makeRequest(tUrl, method="GET")
		tUrl = "/api/account/getAll?space=" + self.accountSpace
		respStudent= self.makeRequest(tUrl, method="GET")
		self.assertEqual(False, respStudent['all_accounts'][0]['assigned_ta'])
		self.assertEqual('No TA Chosen.', respInstCourse['all_InstructorCourses'][0]['ta_name'])

		# Finally, we test removing the ta application
		tUrl = "/api/account/student/removeApp?username=" + respCreateS['user']['wsu_email'] + "&password=" + \
			   respCreateS['user']['password'] + "&app_id=1"
		respRemoveApp = self.makeRequest(tUrl, method="DELETE")
		tUrl = "/api/account/getAllTAApplications"
		respGet= self.makeRequest(tUrl, method="GET")
		self.assertEqual([], respGet['all_TAApplications'])




if __name__ == '__main__':
	unittest.main()