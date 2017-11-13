
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
		self.assertEqual(1, len(respGet['all accounts']))	#Ensuring only one account was made
		self.assertEqual(respCreate['user']['account_id'], respGet['all accounts'][0]['account_id'])
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
		self.assertEqual(1, len(respGet['all accounts']))	#Ensuring only one account was made
		self.assertEqual(respCreate['user']['account_id'], respGet['all accounts'][0]['account_id'])
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
											 'semester' : 'Fall'
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
											 'semester' : 'Fall'
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
		
		
		

if __name__ == '__main__':
    unittest.main()