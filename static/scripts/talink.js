

var TALink = (function(){
	
	//----------------------Place private variables here-----------------------
	
	var apiUrl = 'http://localhost:5000';	//	where the backend is being hosted; right now, it's on your local machine
	
	var accountSpace = 'testingSpace';	//	this is the space in which the accounts we create live; 
										//	a tag to separate them from other sets of accounts.
	
	
	//-------------------------------------------------------------------------
	
	
	//----------------------------Private methods:-----------------------------
	
	/**
    * HTTP GET request 
    * @param  {string}   url       URL path, e.g. "/api/account"
    * @param  {function} onSuccess   callback method to execute upon request success (200 status)
    * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
    * @return {None}
    */
   var makeGetRequest = function(url, onSuccess, onFailure) {
       $.ajax({
           type: 'GET',
           url: apiUrl + url,
           dataType: "json",
           success: onSuccess,
           error: onFailure
       });
   };

     /**
     * HTTP POST request
     * @param  {string}   url       URL path, e.g. "/api/account"
     * @param  {Object}   data      JSON data to send in request body
     * @param  {function} onSuccess   callback method to execute upon request success (200 status)
     * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
     * @return {None}
     */
    var makePostRequest = function(url, data, onSuccess, onFailure) {
        $.ajax({
            type: 'POST',
            url: apiUrl + url,
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: onSuccess,
            error: onFailure
        });
    };
	
		 /**
      * HTTP POST request
      * @param  {string}   url       URL path, e.g. "/api/account"
      * @param  {function} onSuccess   callback method to execute upon request success (200 status)
 +    * @param  {function} onFailure   callback method to execute upon request failure (non-200 status)
 +     * @return {None}
 +     */
     var makeDeleteRequest = function(url, onSuccess, onFailure) {
         $.ajax({
             type: 'DELETE',
             url: apiUrl + url,
             dataType: "json",
             success: onSuccess,
             error: onFailure
         });
     };
	 
	var homeLoadUserData = function(){
		var pathnameSplit = window.location.pathname.split("/");
		var pathname = pathnameSplit[pathnameSplit.length - 1];
		
		if (pathname == "home.html"){
			console.log("confirmed on home.html!");
			
			console.log(localStorage.getItem("user_type"));
			console.log(localStorage.getItem("user_type") == "Instructor");
			
			displayUserTypeClasses();
			
			$("#user-name").text(localStorage.getItem("first_name") + ' ' + localStorage.getItem("last_name"));
			$("#student-major").text(localStorage.getItem("major"));
			$("#student-graduation-date").text(localStorage.getItem("expected_grad"));
			$("#student-TA-history").text(localStorage.getItem("ta_before"));
			$("#student-TA-gpa").text(localStorage.getItem("gpa"));
			$("#student-TA-chosen").css('color','orange');
			if (localStorage.getItem("assigned_ta") == "true"){
				$("#student-TA-chosen").text("You've been chosen as a TA!");
				$("#student-TA-chosen").css('color','green');
			}
			
			if(localStorage.getItem("user_type") == "Instructor"){
				var onSuccess = function(data){
					//if the instructor has no courses
					if(data["instructor"].length == 0){
						//show the html for no classes.
						$(".instructor.class-list").css("display", "none");
						$(".instructor.class-list-empty").css("display", "initial");
					}
					//else if they do
					else{
						//show the html for having classes
						$(".instructor.class-list-empty").css("display", "none");
						$(".instructor.class-list").css("display", "initial");
						
						//fill the list of classes with the professor's added courses.
						
						//alert("hi")
						for(i = 0; i < data["instructor"].length; i++){
							fillCourseData(data, i);
						}
					
					}
				}
				
				var onFailure = function(data){
					alert("Failed to get list of classes.\nThis page probably won't look right.")
				}
				
				makeGetRequest('/api/account/instructor/courses?space=' + accountSpace + '&username=' + localStorage.getItem("username") + '&password=' + localStorage.getItem("password"), onSuccess, onFailure);
			}
			
			else if(localStorage.getItem("user_type") == "Student"){
				var onSuccess = function(data){
					if(data["applications"].length == 0){
						//alert("No apps!");
						$(".student.class-list").css("display", "none");
						$(".student.class-list-empty").css("display", "initial");
					}
					else{
						//alert("Has apps.");						
						$(".student.class-list-empty").css("display", "none");
						$(".student.class-list").css("display", "initial");
						
						for(i = 0; i < data["applications"].length; i++){
							fillStudentApplicationData(data["applications"][i].app_id, data["applications"][i].course_name, data["applications"][i].instructor_name, data["applications"][i].grade_earned, data["applications"][i].date_taken, data["applications"][i].ta_before);
						}
						
					}
				}
				
				var onFailure = function(data){
					alert("Failed to get list of applications.\nThis page probably won't look right.")
				}
				
				makeGetRequest('/api/account/student/applications?username=' + localStorage.getItem("username"), onSuccess, onFailure);
			}
			
			else{
				alert("Error: User not student or instructor?");
			}
		}
	};
	
	var accountLoadUserData = function(){
		var pathnameSplit = window.location.pathname.split("/");
		var pathname = pathnameSplit[pathnameSplit.length - 1];
		
		if (pathname == "account.html"){
			displayUserTypeClasses();
			
			$("#first-name").val(localStorage.getItem("first_name"));
			$("#last-name").val(localStorage.getItem("last_name"));
			$("#wsu-email").val(localStorage.getItem("username"));
			$("#wsu-id").val(localStorage.getItem("wsu_id"));
			$("#phone").val(localStorage.getItem("phone_number"));
			$("#personal-email").val(localStorage.getItem("secondary_email"));
			$("#major").val(localStorage.getItem("major"));
			$("#gpa").val(localStorage.getItem("gpa"));
			
			//Split the "expected_grad" string (example of returned string: "Fall 2017")
			var expectedGradSplitList = localStorage.getItem("expected_grad").split(" ");
			var expectedGradSemester = expectedGradSplitList[0];
			var expectedGradYear = expectedGradSplitList[1];
			
			console.log(expectedGradSemester);
			console.log(expectedGradYear);
			console.log(localStorage.getItem("ta_before"));
			
			//Check the correct radio button for expected grad semester
			if (expectedGradSemester == "Fall"){
				$("input:radio[name=graduation-semester]").filter('[value=fall]').prop('checked', true);
			}
			
			else if (expectedGradSemester == "Spring"){
				$("input:radio[name=graduation-semester]").filter('[value=spring]').prop('checked', true);
			}
			
			//Fill in the expected graduation year field
			$("#graduation-year").val(expectedGradYear);
			
			//Check the correct radio button for TA history
			if (localStorage.getItem("ta_before") == "true"){
				$("input:radio[name=ta-prior]").filter('[value=yes]').prop('checked', true);
			}
			
			else{
				$("input:radio[name=ta-prior]").filter('[value=no]').prop('checked', true);
			}
		}
		
	};
	
	var displayUserTypeClasses = function(){
		if(localStorage.getItem("user_type") == "Instructor"){
			$('.instructor').each(function () {
				this.style.setProperty('display', 'initial', '');
			});
			
			$('.student').each(function () {
				this.style.setProperty('display', 'none', '');
			});
			
			//This doesn't apply to home.html, but we'll just cover everything here.
			$('.form-student').each(function () {
				this.style.setProperty('display', 'none', '');
			});
		}
	};
	
	//	Attach an event listener to the account type radio that handles making
	//	student-specific attributes visible or not.
	//	Also handles making sure that fields not shown are not required for
	//	form submission.
	var attachStudentFieldDisplayListener = function(e){
		$(document).on("click", "input[name=account-type]", function(e){
			if ($("input[name=account-type]:checked").val() == "student"){
				$(".form-student").css("display", "block");
				$(".form-student input").prop("required", true);
			}
			
			else if($("input[name=account-type]:checked").val() == "instructor"){
				$(".form-student").css("display", "none");
				$(".form-student input").prop("required", false);
			}
			
			else{
				alert("Error! Not a student or instructor?");
			}
		});
	};
	
	
	
	//	Without this function, radios will not reset to their default value after
	//	page refresh. This causes an issue where instructor can be selected with
	//	student attributes visible, since those are visible by default.
	var resetRadios = function(){
		$(".account-creation-form").each(function(){
			this.reset();
		});
	};
	
	
	
	//	Check to see if the password fields are the same. Called by the event 
	//	listeners placed on #password and #confirm-password by 
	//	attachConfirmPasswordHandler() below.
	var confirmPassword = function(){
		if($("#password").val() == $("#confirm-password").val()){
			$("#confirm-password")[0].setCustomValidity("");
			
			$("#password").removeClass("error-border");
			$("#confirm-password").removeClass("error-border");
			
			//console.log("Passwords match!");
		}
		
		else{
			$("#confirm-password")[0].setCustomValidity("Passwords do not match.");
			
			$("#password").addClass("error-border");
			$("#confirm-password").addClass("error-border");			
			
			//console.log("Passwords don't match....");
		}
	};
	
	
	
	//	Attach event listeners to #password and #confirm-password that call the 
	//	confirmPassword() function when a key is released in those fields.
	var attachConfirmPasswordListener = function(){
		$(document).on("keyup", "#password", function(e){
			confirmPassword();
		});
		
		$(document).on("keyup", "#confirm-password", function(e){
			confirmPassword();
		});
	};
	
	var createStudentAccount = function(){
		
		//cFirstName = $(".account-creation-form").find('first-name').val();
		//cLastName = $(".account-creation-form").find('last-name').val();
		//cUsername = $(".account-creation-form").find('wsu-email').val();
		
		var accountInfo = {};	//prepare the account object to send to the server
		//And now we fill the object with information from the forms
		accountInfo.user_type = "Student";
		accountInfo.space = accountSpace;
		accountInfo.first_name = $('#first-name').val();
		accountInfo.last_name = $('#last-name').val();
		accountInfo.wsu_id = $('#wsu-id').val();
		accountInfo.wsu_email = $('#wsu-email').val();
		accountInfo.password = $('#password').val();
		accountInfo.phone_number = $('#phone').val();
		accountInfo.secondary_email = $('#personal-email').val();
		accountInfo.major = $('#major').val();
		accountInfo.gpa = $('#gpa').val();
		
		if ($("input[name=ta-prior]:checked").val() == "yes"){
			accountInfo.ta_before = true;
		}
		else{
			accountInfo.ta_before = false;
		}
		
		if ($("input[name=graduation-semester]:checked").val() == "spring"){
			accountInfo.expected_grad = "Spring " + $('#graduation-year').val();
		}
		else{
			accountInfo.expected_grad = "Fall " + $('#graduation-year').val();
		}
		
        var onSuccess = function(data) {  
			window.location.href = "index.html";	//if we successfully created an account, go back to the login page
        };
        var onFailure = function() { 
            console.error('create account failed'); 
        };
		
		//make a post request, supplying the accountInfo object we just filled out
		makePostRequest('/api/account/student', accountInfo, onSuccess, onFailure);
		
		
	};
	
	var createInstructorAccount = function(){
	
		//And now we fill the object with information from the forms
		var accountInfo = {};	//prepare the account object to send to the server
		accountInfo.user_type = "Instructor";
		accountInfo.space = accountSpace;
		accountInfo.first_name = $('#first-name').val();
		accountInfo.last_name = $('#last-name').val();
		accountInfo.wsu_id = $('#wsu-id').val();
		accountInfo.wsu_email = $('#wsu-email').val();
		accountInfo.password = $('#password').val();
		accountInfo.phone_number = $('#phone').val();
		accountInfo.secondary_email = $('#personal-email').val();
		accountInfo.courses_taught = [];
	
	
	    var onSuccess = function(data) {
			window.location.href = "index.html";	//if we successfully created an account, go back to the login page
        };
        var onFailure = function() { 
            console.error('create account failed'); 
        };
		
		//make a post request, supplying the accountInfo object we just filled out
		makePostRequest('/api/account/instructor', accountInfo, onSuccess, onFailure);
	
	};
	
	var attachLoginHandler = function(e){
		
		$(".login-form").on('click', ".login-button", function(e) {
			e.preventDefault ();	// Tell the browser to skip its default click action
		
			var lUsername = $(".login-form").find('.username-input').val();
			var lPassword = $(".login-form").find('.password-input').val();
		
			var onSuccess = function(data) {
				window.location.href = "home.html";	//if we successfully logged into an account, go to the account page
				
				window.localStorage.setItem("user_type", data["person"]["user_type"]);
				window.localStorage.setItem("password", lPassword);	
				window.localStorage.setItem("username", data["person"]["wsu_email"]);
				window.localStorage.setItem("first_name", data["person"]["first_name"]);
				window.localStorage.setItem("last_name", data["person"]["last_name"]);
				window.localStorage.setItem("wsu_id", data["person"]["wsu_id"]);
				window.localStorage.setItem("phone_number", data["person"]["phone_number"]);
				window.localStorage.setItem("secondary_email", data["person"]["secondary_email"]);
				if (data["person"]["user_type"] == "Student"){
					window.localStorage.setItem("gpa", data["person"]["gpa"]);
					window.localStorage.setItem("major", data["person"]["major"]);
					window.localStorage.setItem("expected_grad", data["person"]["expected_grad"]);
					window.localStorage.setItem("ta_before", data["person"]["ta_before"]);
					window.localStorage.setItem("assigned_ta", data["person"]["assigned_ta"])
					//alert(window.localStorage.getItem("assigned_ta"))
				}
			};
			var onFailure = function() { 
				console.error('login failed'); 
			};
			//make a get request, supplying the login info
			makeGetRequest('/api/account?space=' + accountSpace + '&username='+ lUsername + '&password=' + lPassword, onSuccess, onFailure);
		});
	};
	
	
	var attachCreateAccountHandler = function(e){
		
		$(".account-creation-form").on('click', ".signup-button", function(e) {
			
			e.preventDefault ();	// Tell the browser to skip its default click action
			
			if ($("input[name=account-type]:checked").val() == "student"){	//if the radio button's value is 'student', create a student account
				createStudentAccount();
			}
			else if ($("input[name=account-type]:checked").val() == "instructor"){ //if the radio button's value is 'instructor', create an instructor account
				createInstructorAccount();
			}
		});
	};
	
	var attachPrefixDropdownTextHandler = function(e){
		$(".course-prefix-dropdown").on('click', 'li a', function(e){
			//alert($('.selected-prefix').text())
			//console.log($(e.target).text());
			var replaceText = $(e.target).text();
			//alert(replaceText);
			$(".selected-prefix").each(function(e){
				console.log($(this).text());
				$(this).text( replaceText );
				//alert($('.selected-prefix').text())
			})
		
			// $(".selected-prefix-group").each(function(e){
				// console.log($(this));
				// $(this).find(".selected-prefix").text($(e.target).text());
				// $(this).find(".selected-prefix").val($(e.target).text());				
			// })
		});
	};
	
	var attachLogoutListener = function(){
		$("#logout-button").click(function(){
			window.localStorage.clear();
			window.location.href = "index.html";	//if we successfully created an account, go back to the login page
		});
	};
	
	var attachEditAccountListener = function(e){		
		$(".account-edit-button").click(function(e){
			e.preventDefault ();	// Tell the browser to skip its default click action
			
			if($("#password").val() == $("#confirm-password").val()){
				if(localStorage.getItem("user_type") == "Student"){
					var accountInfo = {};	//prepare the account object to send to the server
					//And now we fill the object with information from the forms
					accountInfo.user_type = "Student";
					accountInfo.space = accountSpace;
					accountInfo.first_name = $('#first-name').val();
					accountInfo.last_name = $('#last-name').val();
					accountInfo.wsu_id = $('#wsu-id').val();
					accountInfo.wsu_email = $('#wsu-email').val();
					accountInfo.phone_number = $('#phone').val();
					accountInfo.secondary_email = $('#personal-email').val();
					accountInfo.major = $('#major').val();
					accountInfo.gpa = $('#gpa').val();
					if($("#password").val() != ""){
						accountInfo.password = $('#password').val();
					}
					else{
						accountInfo.password = $('#confirm-current-password').val();
					}
					
					if ($("input[name=ta-prior]:checked").val() == "yes"){
						accountInfo.ta_before = true;
					}
					else{
						accountInfo.ta_before = false;
					}
					
					if ($("input[name=ta-prior]:checked").val() == "spring"){
						accountInfo.expected_grad = "Spring " + $('#graduation-year').val();
					}
					else{
						accountInfo.expected_grad = "Fall " + $('#graduation-year').val();
					}
					
					var onSuccess = function() {  
						window.localStorage.setItem("user_type", accountInfo.user_type);
								
						window.localStorage.setItem("username", accountInfo.wsu_email);
						window.localStorage.setItem("major", accountInfo.major);
						window.localStorage.setItem("expected_grad", accountInfo.expected_grad);
						window.localStorage.setItem("ta_before", accountInfo.ta_before);
						window.localStorage.setItem("first_name", accountInfo.first_name);
						window.localStorage.setItem("last_name", accountInfo.last_name);
						window.localStorage.setItem("wsu_id", accountInfo.wsu_id);
						window.localStorage.setItem("phone_number", accountInfo.phone_number);
						window.localStorage.setItem("secondary_email", accountInfo.secondary_email);
						window.localStorage.setItem("gpa", accountInfo.gpa);					
					
						//alert("Account edit successful!");
						
						window.location.href = "account.html";	//if we successfully created an account, go back to the login page
					};
					var onFailure = function() { 
						alert("Account edit failed.");
						console.error('Edit account failed'); 
					};
			
					//make a post request, supplying the accountInfo object we just filled out
					makePostRequest('/api/account/student/editProfile?space=' + accountSpace + '&username='+ localStorage.getItem("username") + '&password=' + $('#confirm-current-password').val(), accountInfo, onSuccess, onFailure);
				}
				
				else if (localStorage.getItem("user_type") == "Instructor"){
					var accountInfo = {};	//prepare the account object to send to the server
					//And now we fill the object with information from the forms
					accountInfo.user_type = "Instructor";
					accountInfo.space = accountSpace;
					accountInfo.first_name = $('#first-name').val();
					accountInfo.last_name = $('#last-name').val();
					accountInfo.wsu_id = $('#wsu-id').val();
					accountInfo.wsu_email = $('#wsu-email').val();
					accountInfo.phone_number = $('#phone').val();
					accountInfo.secondary_email = $('#personal-email').val();
					if($("#password").val() != ""){
						accountInfo.password = $('#password').val();
					}
					else{
						accountInfo.password = $('#confirm-current-password').val();
					}
					
					var onSuccess = function() {  
						window.localStorage.setItem("user_type", accountInfo.user_type);
								
						window.localStorage.setItem("username", accountInfo.wsu_email);
						window.localStorage.setItem("first_name", accountInfo.first_name);
						window.localStorage.setItem("last_name", accountInfo.last_name);
						window.localStorage.setItem("wsu_id", accountInfo.wsu_id);
						window.localStorage.setItem("phone_number", accountInfo.phone_number);
						window.localStorage.setItem("secondary_email", accountInfo.secondary_email);
					
						//alert("Account edit successful!");
						
						window.location.href = "account.html";	//if we successfully created an account, go back to the login page
					};
					var onFailure = function() { 
						alert("Account edit failed.");
						console.error('Edit account failed'); 
					};
			
					//make a post request, supplying the accountInfo object we just filled out
					makePostRequest('/api/account/instructor/editProfile?space=' + accountSpace + '&username='+ localStorage.getItem("username") + '&password=' + $('#confirm-current-password').val(), accountInfo, onSuccess, onFailure);
				}
				
				else{
					alert("Error! LocalStorage account type is not student or instructor.");
					console.error("LocalStorage account type not student or instructor?")
				}
			}
			
			else{
				alert("Error: Passwords do not match!");
			}
		});
	};
	
	var attachInstructorAddCourseListener = function(e){
		$(".instructor-add-course-button").click(function(){
			var courseInfo = {};
			//alert($('.selected-prefix').text())
			courseInfo.course_name = $('#modal-instructor-add-class .selected-prefix').text() + " " + $('#course-number').val();
			courseInfo.section_name = $('#section-or-lab-number').val();
			
			//Get the semester from the user's radio selection.
 			//Note: The backend requires the year and semester to be sent as a field named "semester" (so, courseInfo.semester)
 			if ($("input[name=course-semester]:checked").val() == "fall"){
 				courseInfo.semester = "Fall " + $('#course-year').val();
 			}
 			else if ($("input[name=course-semester]:checked").val() == "spring"){
 				courseInfo.semester = "Spring " + $('#course-year').val();
 			}
 			else if ($("input[name=course-semester]:checked").val() == "summer"){
 				courseInfo.semester = "Summer " + $('#course-year').val();
 			}
 			courseInfo.days_lecture = $('#course-days').val();
 			courseInfo.time_lecture = $('#course-time').val();
 			
 			//Get whether this class is a lab from the user's radio selection.
 			//	If yes, this will add " Lab" to the beginning of the section name.
 			if ($("input[name=course-is-lab]:checked").val() == "yes"){
 				courseInfo.section_name = "Lab-" + courseInfo.section_name;
 			}
 			else if ($("input[name=course-is-lab]:checked").val() == "no"){
 				//do nothing
 			}
			
			// alert("DEBUG" + "\n" +
					// "----------------" + "\n" +
					// "Course Name: " + courseInfo.course_name + "\n" +
					// "Section: " + courseInfo.section_name + "\n" +
					// "Semester: " + courseInfo.semester + "\n" +
					// "Days: " + courseInfo.days_lecture + "\n" +
					// "Time: " + courseInfo.time_lecture);
					
			var onSuccess = function(){
				//alert("Successfully added course!")
				window.location.href = "home.html"; //if we successfully added a course, reload home.html
			}
			
			var onFailure = function(){
				alert("Failed to add course.");
			}
			
			makePostRequest('/api/account/instructor/addCourse?space=' + accountSpace + '&username=' + localStorage.getItem("username") + '&password=' + localStorage.getItem("password"), courseInfo, onSuccess, onFailure);
		});
	}
	
	//data["instructor"][i].course_id, data["instructor"][i].course_name, data["instructor"][i].section_name, data["instructor"][i].ta_name, data["instructor"][i].app_count
	var fillCourseData = function(data, i){
		$('.class-list2').append($('<div/>')
			.attr("id", data["instructor"][i].course_id.toString())
			.addClass("row")
			.append($('<div/>')
				.addClass("col-xs-10 instructor-class-info")
				.attr("data-toggle", "modal")
				.attr("data-target", "#modal-instructor-class-info")
				.append($('<dl/>')
					.addClass("dl-horizontal")
					.append($('<dt/>').addClass("h3").text(data["instructor"][i].course_name + " " + data["instructor"][i].section_name), $('<dd/>'),
						//$('<dt/>').text("Section number:"), $('<dd/>').text(course_section.toString()),
						$('<dt/>').text("TA Chosen:"), $('<dd/>').text(data["instructor"][i].ta_name),
						$('<dt/>').text("Meeting Days:"), $('<dd/>').text(data["instructor"][i].days_lecture),
						$('<dt/>').text("Meeting Times:"), $('<dd/>').text(data["instructor"][i].time_lecture),
						$('<dt/>').text("Number of applicants:"), $('<dd/>').text(data["instructor"][i].app_count.toString())
					)
				)
				//
				//
				//
			, $('<div/>')
			.addClass("col-xs-2 text-right")
			.append('<p/>')
				.addClass("h3 delete-course")
				.text('x')
			)
		)
	}
	
	
	var fillStudentApplicationData = function(app_id, course_name, instructor_name, grade_earned, date_taken, ta_before){
		$('.class-list2').append($('<div/>')
			.attr("id", app_id.toString())
			.addClass("row")
			.append($('<div/>')
				.addClass("col-xs-10 student-app-info")
				.append($('<dl/>')
					.addClass("dl-horizontal")
					.append($('<dt/>').addClass("h3").text(course_name), $('<dd/>'),
						$('<dt/>').text("Instructor:"), $('<dd/>').text(instructor_name),
						$('<dt/>').text("Grade Earned:"), $('<dd/>').text(grade_earned),
						$('<dt/>').text("Date Class was Taken:"), $('<dd/>').text(date_taken),
						$('<dt/>').text("TA'd this class before:"), $('<dd/>').text(ta_before.toString())
						
					)
				)
			, $('<div/>')
			.addClass("col-xs-2 text-right")
			.append('<p/>')
				.addClass('h3 delete-course')
				.text('x')
			)
		)
	}
	
	var fillApplicantList = function(data, i){
		$('#table-applicants-list').append($('<tr/>')
			.attr("id", data["applications"][i].app_id.toString())
					.append($('<th/>').text(data["applications"][i].student_name),
						$('<td/>').text(data["applications"][i].username),
						$('<td/>').text(data["applications"][i].wsu_sid),
						$('<td/>').text(data["applications"][i].date_taken),
						$('<td/>').text(data["applications"][i].grade_earned),
						$('<td/>').text(data["applications"][i].ta_before)
					)
			)
	}
	
	var attachDeleteCourseListener = function(e){
 		console.log(this);
 		$(".class-list2").on('click', '.delete-course', function(e){
 			var courseListingDocumentElement = (e.target).parentNode;
 			var courseListingId = $((e.target).parentNode).attr('id');
 			
 			//console.log($((e.target).parentNode).attr('id'));
 			
 			var onSuccess = function(){
 				//alert("Successfully deleted course!");
 				window.location.href = "home.html";	//if we successfully deleted a course, reload home.html
			}
 			
 			var onFailure = function(){
 				alert("Failed to delete course.");
 			}
 			
 			if(localStorage.getItem("user_type") == "Instructor"){
 				makeDeleteRequest('/api/account/instructor/removeCourse?space=' + accountSpace + '&username='+ localStorage.getItem("username") + '&password=' + localStorage.getItem("password") + '&course_id=' + courseListingId, onSuccess, onFailure);
 			}
 			
 			else if(localStorage.getItem("user_type") == "Student"){
 				makeDeleteRequest('/api/account/student/removeApp?space=' + accountSpace + '&username='+ localStorage.getItem("username") + '&password=' + localStorage.getItem("password") + '&app_id=' + courseListingId, onSuccess, onFailure);
 			}
 			
 			else{
 				alert("Error: Could not delete course - user not student or instructor?")
 			}
 		});
 	}
	
    var attachStudentCourseSearchListener = function(e){
        var onSuccess = function(data){
		$("#course-search-results-table-body").html("");
		
			for (var i = 0; i < data["found_courses"].length; i++){
				alert(data["found_courses"][i].course_name + "\n" +
					data["found_courses"][i].days_lecture + "\n" +
					"\n");
					
				makeCourseSearchTableEntry(data["found_courses"][i]);

				//console.log(data["found_courses"][i].course_name);
			}
			
			$("#course-search-results").css("display", "table");
        }
        var onFailure = function(){
            window.alert("get request failed @ api/account/student/courseSearch");
        }
        
        $("#course-search-button").click(function(){
			//console.log($("#modal-student-add-class .selected-prefix").text());
			//console.log($("#modal-student-add-class .selected-prefix").text() + ' ' + $("#course-search-number").val());
			makeGetRequest('/api/account/student/courseSearch' + '?search_name=' + $("#modal-student-add-class .selected-prefix").text() + ' ' + $("#course-search-number").val(), onSuccess, onFailure);
        });
    }
	
	var makeCourseSearchTableEntry = function(course){
		var courseNameSplit = course.course_name.split(" ");
		
		$("#course-search-results-table-body").append($('<tr/>').attr('id', course.course_id)
		.append($('<th/>').html("&#x2610"),
			($('<th/>').attr('scope', 'row').attr('id', 'course-name-prefix').text(courseNameSplit[0])),
			($('<td/>').attr('id', 'course-name-number').text(courseNameSplit[1])),
			($('<td/>').text(course.semester)),
			($('<td/>').text(course.days_lecture)),
			($('<td/>').text(course.time_lecture))
		)
	)}
	
    
    var attachInstructorCourseApplicantListener = function(e){
        
        $(".class-list2").on("click", ".instructor-class-info", function(e){
           //console.log(e.target.closest(".row").id);
		    var x = e.target.closest(".row").id;
					
		var onSuccess = function(data){
		    $("#table-applicants-list").html("");
			console.log(data);
			for(i = 0; i < data["applications"].length; i++)
			{
				fillApplicantList(data, i);
			}
            
        }
        var onFailure = function(){
            window.alert("bad");
        }
		   
           makeGetRequest('/api/account/instructor/courses/applications' + '?course_id=' + e.target.closest(".row").id, onSuccess, onFailure);
        });
    }
	
	var attachSelectCourseInResultsListener = function(e){
		$("#course-search-results-table-body").on("click", "tr", function(e){
			alert($(e.target).closest('tr').attr('id'));
			if ($(e.target).closest('tr').hasClass('selected-table-option')){
				$(e.target).closest('tr').removeClass('selected-table-option');
			
			}
			else{
				$(e.target).closest('tr').addClass('selected-table-option');
			}
		})		
	}
	
	var attachStudentAddApplicationsListener = function(e){
		$("#modal-student-add-class").on('click', '#student-add-applications-button', function(e){
			$('.selected-table-option').each(function(e){
				alert($(this).attr('id'));
			})

			//Get the course name from the first entry in the table.
			var courseName = $('#course-search-results-table-body #course-name-prefix').first().text() + " " + $('#course-search-results-table-body #course-name-number').first().text();
			
			//Hide the add class modal.
			$('#modal-student-add-class').modal('hide');
			
			//Fill in the class name.
			$('#application-course-name').text(courseName);
			
			//Show the application info modal.
			$('#modal-student-application-info').modal('show');
		})
	}
	
	var attachStudentSubmitApplicationsListener = function(e){
		$("#student-submit-applications-button").click(function(e){
			alert("submit");
		})
	}
	
	
	var attachSelectAppInResultsListener = function(e){
		$("#table-applicants-list").on("click", "tr", function(e){
			//alert($(e.target).closest('tr').attr('id'));
			if ($(e.target).closest('tr').hasClass('selected-table-option')){
				$(e.target).closest('tr').removeClass('selected-table-option');
			
			}
			else{
				//need to unselect all other options
				$('.selected-table-option').each(function(d){
					$(this).removeClass('selected-table-option')
				})
				$(e.target).closest('tr').addClass('selected-table-option');
			}
		})		
	}
	
	var attachInstructorAddTAListener = function(e){
		$("#modal-instructor-class-info").on('click', '#instructor-add-TA-button', function(e){
			$('.selected-table-option').each(function(e){
				aid = $(this).attr('id')
				//alert($(this).attr('id'));
				
				var onSuccess = function(){
					alert("Successfully set TA!")
					window.location.href = "home.html"; //if we successfully set a TA, reload home.html
				}
				
				var onFailure = function(){
					alert("Failed to set TA.");
				}
				//alert(aid + "HI!")
				makePostRequest('/api/account/instructor/course/chooseTA?username=' + localStorage.getItem("username") + '&password=' + localStorage.getItem("password") + "&app_id=" + aid, {}, onSuccess, onFailure);
			})
			
		})
	}

	
	//	Waits until the page is loaded before running these functions.
	$(document).ready(function(){
		resetRadios();
		attachStudentFieldDisplayListener();
		attachConfirmPasswordListener();
		attachCreateAccountHandler();
		attachLoginHandler();
		attachPrefixDropdownTextHandler();
		attachLogoutListener();
		attachEditAccountListener();
		attachInstructorAddCourseListener();
        attachStudentCourseSearchListener();
		attachInstructorCourseApplicantListener();
		attachDeleteCourseListener();
		homeLoadUserData();
		accountLoadUserData();
		attachSelectCourseInResultsListener();
		attachStudentAddApplicationsListener();
		attachStudentSubmitApplicationsListener();
		attachSelectAppInResultsListener();
		attachInstructorAddTAListener();
		
	});
	
})();