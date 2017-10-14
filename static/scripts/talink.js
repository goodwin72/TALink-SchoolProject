
var TALink = (function(){
	
	//Attach an event listener to the account type radio that handles making
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
	
	//Without this function, radios will not reset to their default value after
	//	page refresh. This causes an issue where instructor can be selected with
	//	student attributes visible, since those are visible by default.
	var resetRadios = function(){
		$(".account-creation-form").each(function(){
			this.reset();
		});
	};
	
	//Check to see if the password fields are the same. Called by the event 
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
	
	//Attach event listeners to #password and #confirm-password that call the 
	//	confirmPassword() function when a key is released in those fields.
	var attachConfirmPasswordListener = function(){
		$(document).on("keyup", "#password", function(e){
			confirmPassword();
		});
		
		$(document).on("keyup", "#confirm-password", function(e){
			confirmPassword();
		});
	};
	
	//Waits until the page is loaded before running these functions.
	$(document).ready(function(){
		resetRadios();
		attachStudentFieldDisplayListener();
		attachConfirmPasswordListener();
	});
})();