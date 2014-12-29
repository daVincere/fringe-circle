//$( document ).ready(function() {
//    $('.contact-button').click(function() {
//	$('body').addClass('hidden-body')
//    });
//});

function populate_first_subfilter_masters_select(subcategory_name)
{
	$.ajax({
		url:'/fringe_circle/fetch_first_subfilter_masters/'+subcategory_name+'/',
		dataType:'json',
	}).done(function(data){
		$('#subfilter_select_alert').empty();
		$('#subfilter_select_alert').append('Select Filter');
		for(var i=0;i<data.length;i++)
		{
			$('#subfilter_select_alert').append("<option value='"+data[i]+"'>"+data[i]+"</option>");
		}
	})
}

function populate_locality_alert(city_name)
{
	lower_city_name=city_name.toLowerCase();
	if(lower_city_name.indexOf("select")==-1)
	{
		$.ajax({
			url:'/fringe_circle/fetch_locality_names/'+city_name+'/',
			dataType:'json',
		}).done(function(data){
			$('#locality_select_alert').empty();
			$('#locality_select_alert').append('<option>Select Locality</option>');
			for(var i=0;i<data.length;i++)
			{
				$('#locality_select_alert').append("<option value='"+data[i]+"'>"+data[i]+"</option>");
			}
		});
	}
}

function populate_city_alert(state_name)
{
	var lower_state_name=state_name.toLowerCase()
	if(lower_state_name.indexOf("select")==-1)
	{
		$.ajax({
			url:'/fringe_circle/fetch_city_names/'+state_name+'/',
			dataType:'json',
		}).done(function(data){
			$('#city_select_alert').empty();
			$('#city_select_alert').append('<option>Select City</option>');
			for (var i=0;i<data.length;i++)
			{
				$('#city_select_alert').append("<option value='"+data[i]+"'>"+data[i]+"</option>");
			}
		});
	}
}

function populate_subcat_alert(prime_category_name)
{
	$.ajax({
		url:'/fringe_circle/fetch_subcategory_names/'+prime_category_name+'/',
		dataType:'json',
	}).done(function(data){
		$('#subcategory_select_alert').empty();
		$('#subcategory_select_alert').append('<option>Select SubCategory</option>');
		for(var i=0;i<data.length;i++)
		{
			$('#subcategory_select_alert').append("<option value='"+data[i]+"' onclick='populate_first_subfilter_masters_select(this.value);'>"+data[i]+"</option>");
		}
	});
}

function populate_subcat(prime_category_name)
{
	$('#subcat_list_all').prop('title',prime_category_name+':All Subcategories');

	$.ajax({
		url:'/fringe_circle/fetch_subcategory_names/'+prime_category_name+'/',
		dataType:'json',
	}).done(function(data){

		for(var i=0;i<data.length;i++)
		{
			var span_element=document.createElement('div');
			var anchor_subcat=document.createElement('a');
			anchor_subcat.href='/fringe_circle/product_list/'+data[i];
			anchor_subcat.innerHTML=data[i];
			span_element.id="subcat_span_"+i.toString();
			anchor_subcat.className='subcat_span';
			$('#subcat_list_all').append(span_element);
			$('#subcat_span_'+i.toString()).append(anchor_subcat);

		}


		$('#subcat_list_all').dialog({
			modal:true,
			close:function(){
				$('#subcat_list_all').empty();
			}
		});
	});


}

$(document).ready(function()
{
	$('#hmLink').on('click',function()
	{
		$('body').addClass('hidden-body');
		$('.overley-bg').show();
		$('.disc-post,.find-locate').show()
	});

	$('.close-btn').on('click',function(){
		$('body').removeClass('hidden-body');
		$('.overley-bg').hide();	
		$('.disc-post,.find-locate').hide()
	});
});



$(document).ready(function()
{
	$('#signIn').on('click',function()
	{
		$('body').addClass('hidden-body');
		$('.overley-bg').show();
		$('.login-popup').show()
	});

	$('.close-btn').on('click',function(){
		$('body').removeClass('hidden-body');
		$('.overley-bg').hide();
		$('.login-popup').hide()
	});
});


$(document).ready(function(){

	$('#regIn').on('click',function(){

		$('body').addClass('hidden-body');
		$('.overley-bg').show();
		$('.register-popup').show()
	});

	$('.close-btn').on('click',function(){
		$('body').removeClass('hidden-body');
		$('.overley-bg').hide();
		$('.register-popup').hide()

	});
});

function validate_user_password()
{
	var first_pass=document.getElementById("firstPass");
	var second_pass=document.getElementById("secondPass");
	if(firstPass.value!=secondPass.value)
	{
		$(first_pass).css("color","red");
		$(second_pass).css("color","red");
		$("#pass_error").text("Password not matching");
	}
	else{
		$(first_pass).css("color","green");
		$(second_pass).css("color","green");
		$("#pass_error").text("");	
	}
}

function validate_submit()
{
	$("#user_registration_form").submit();
}