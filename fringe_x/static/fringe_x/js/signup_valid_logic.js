function validate_input()
{
var altEmailElement=$("#altEmail").val();
var workEmailElement=$("#workEmail").val();
var termsConditionsCheckBox=document.getElementById("conditionCheckBox");
if($(termsConditionsCheckBox).is(':checked'))
{
if(altEmailElement=="" || workEmailElement=="")
{
alert("Provide Both email Addresses");
}
else if(altEmailElement==workEmailElement)
{
alert("work and alternate email cannot be same");
}
else{
$( "#signup-confirm" ).dialog({
      resizable: false,
      height:300,
      modal: true,
      buttons: {
        "OK, Got it!": function() {
          //$( this ).dialog( "close" );
          $("#signup_form").submit();
        },
        "Cancel Signup": function() {
          $( this ).dialog( "close" );
        }
      }
    });
//$("#signup_form").submit();
}
//alert('hello');
}
else
{
alert("Please check and agree with the terms and conditions!!");
}
}