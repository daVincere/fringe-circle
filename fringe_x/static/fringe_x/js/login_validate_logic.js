function validate_form()
{
var email=$("#work_email").val();
var pwd=$("#password").val();
if(email=="" || pwd=="")
{
alert("Enter Email and Passowrd");
return false;
}
else
{
return True;
}
}