var form_fields = document.getElementsByTagName('input')
form_fields[0].placeholder='Username..';
form_fields[1].placeholder='Email..';
form_fields[2].placeholder='Enter password...';
form_fields[3].placeholder='Confirm Password...';


for (var field in form_fields){	
	form_fields[field].className += ' form-control'
}