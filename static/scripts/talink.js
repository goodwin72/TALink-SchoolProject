

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
	
	var homeLoadUserData = function(){
		console.log(window.location.pathname);
		
		var pathnameSplit = window.location.pathname.split("/");
		var pathname = pathnameSplit[pathnameSplit.length - 1];
		
		console.log(pathname);
		
		if (pathname == "home.html"){
			console.log("HELLO!");
			$("#user-name").text(localStorage.getItem("first_name") + ' ' + localStorage.getItem("last_name"));
			$("#student-major").text(localStorage.getItem("major"));
			$("#student-graduation-date").text(localStorage.getItem("expected_grad"));
			$("#student-TA-history").text(localStorage.getItem("ta_before"));
		}
	};
	
	var accountLoadUserData = function(){
		console.log(window.location.pathname);
		
		var pathnameSplit = window.location.pathname.split("/");
		var pathname = pathnameSplit[pathnameSplit.length - 1];
		
		console.log(pathname);
		
		if (pathname == "account.html"){
			$("#first-name").val(localStorage.getItem("first_name"));
			$("#last-name").val(localStorage.getItem("last_name"));
			$("#wsu-email").val(localStorage.getItem("username"));
			$("#wsu-id").val(localStorage.getItem("wsu_id"));
			$("#phone").val(localStorage.getItem("phone_number"));
			$("#personal-email").val(localStorage.getItem("secondary_email"));
			$("#major").val(localStorage.getItem("major"));
			$("#gpa").val(localStorage.getItem("gpa"));
		}
		
		//$("user-name").text = userdata.first_name + ' ' + userdata.last_name;
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
		}
		
		else{
			$("#confirm-password")[0].setCustomValidity("Passwords do not match.");
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
		accountInfo.course_preferences = [];
		
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

				window.localStorage.setItem("username", data["person"]["wsu_email"]);
				window.localStorage.setItem("major", data["person"]["major"]);
				window.localStorage.setItem("expected_grad", data["person"]["expected_grad"]);
				window.localStorage.setItem("ta_before", data["person"]["ta_before"]);
				window.localStorage.setItem("first_name", data["person"]["first_name"]);
				window.localStorage.setItem("last_name", data["person"]["last_name"]);
				window.localStorage.setItem("wsu_id", data["person"]["wsu_id"]);
				window.localStorage.setItem("phone_number", data["person"]["phone_number"]);
				window.localStorage.setItem("secondary_email", data["person"]["secondary_email"]);
				window.localStorage.setItem("gpa", data["person"]["gpa"]);
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
	
	var attachPrefixDropdownTextHandler = function(){
		$("#course-prefix-dropdown").on('click', 'li a', function(){
			$("#selected-prefix:first-child").text($(this).text());
			$("#selected-prefix:first-child").val($(this).text());
		});
	};
	
	var attachLogoutListener = function(){
		$("#logout-button").click(function(){
			window.localStorage.clear();
			window.location.href = "index.html";	//if we successfully created an account, go back to the login page
		});
	};
	
	//	Waits until the page is loaded before running these functions.
	$(document).ready(function(){
		resetRadios();
		attachStudentFieldDisplayListener();
		attachConfirmPasswordListener();
		attachCreateAccountHandler();
		attachLoginHandler();
		attachPrefixDropdownTextHandler();
		attachLogoutListener();
		
		homeLoadUserData();
		accountLoadUserData();
		
		
	});
	
})();