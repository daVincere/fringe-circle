//$( document ).ready(function() {
//    $('.contact-button').click(function() {
//	$('body').addClass('hidden-body')
//    });
//});



$(document).ready(function(){

	$('#popup').on('click',function(){


		$('body').addClass('hidden-body');
		$('.overley-bg').show();
		$('.find-locate').show()
	});

	$('.close-btn').on('click',function(){
		$('body').removeClass('hidden-body');
		$('.overley-bg').hide();
		$('.find-locate').hide()

	});
	

	$('#popup2').on('click',function(){
		

		$('body').addClass('hidden-body');
		$('.overley-bg').show();
		$('.disc-post').show()
	});

	$('.close-btn').on('click',function(){
		$('body').removeClass('hidden-body');
		$('.overley-bg').hide();
		$('.disc-post').hide()

	});	
	
});



$(document).ready(function(){

	$('#signIn').on('click',function(){

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

function get_likes_dislikes_reply(status,reply_id)
{
	$.ajax({
		url:'/fringe_circle/like_dislike_reply/'+status+'/'+reply_id+'/',
		dataType:'json',
	}).done(function(data){
		var like_data=$("#like_"+reply_id).text();
		var unlike_data=$("#unlike_"+reply_id).text();
		like_data=like_data.trim();
		unlike_data=unlike_data.trim();
		var number_of_likes=parseInt(like_data.substring(0,1));
		var number_of_unlikes=parseInt(unlike_data.substring(0,1));
		//var parsedJSON=jQuery.parseJSON(data);
		//alert(data["unlike"]);
		if(data["unlike"]=="inc" && data["like"]=="dec")
		{
			number_of_unlikes=number_of_unlikes+1;
			if(number_of_likes!=0)
			{
				number_of_likes=number_of_likes-1;
			}
		}
		else if(data["unlike"]=="dec" && data["like"]=="inc")
		{
			number_of_likes=number_of_likes+1;
			if(number_of_unlikes!=0)
			{
				number_of_unlikes=number_of_unlikes-1;
			}
		}
		else if(data["unlike"]=="inc" && data["like"]=="flat")
		{
			number_of_unlikes=number_of_unlikes+1;
		}
		else if(data["unlike"]=="flat" && data["like"]=="inc")
		{
			number_of_likes=number_of_likes+1;
		}
		else
		{
			//do nothing
		}
		$("#like_"+reply_id).text(number_of_likes.toString()+" likes");
		$("#unlike_"+reply_id).text(number_of_unlikes.toString()+" unlikes");
		//alert(data);

	});
}


function get_likes_dislikes(status,discussion_id)
{
	$.ajax({
		url:'/fringe_circle/like_dislike/'+status+'/'+discussion_id+'/',
		dataType:'json',
	}).done(function(data){
		var like_data=$("#like_"+discussion_id).text();
		var unlike_data=$("#unlike_"+discussion_id).text();
		like_data=like_data.trim();
		unlike_data=unlike_data.trim();
		var number_of_likes=parseInt(like_data.substring(0,1));
		var number_of_unlikes=parseInt(unlike_data.substring(0,1));
		//var parsedJSON=jQuery.parseJSON(data);
		//alert(data["unlike"]);
		if(data["unlike"]=="inc" && data["like"]=="dec")
		{
			number_of_unlikes=number_of_unlikes+1;
			if(number_of_likes!=0)
			{
				number_of_likes=number_of_likes-1;
			}
		}
		else if(data["unlike"]=="dec" && data["like"]=="inc")
		{
			number_of_likes=number_of_likes+1;
			if(number_of_unlikes!=0)
			{
				number_of_unlikes=number_of_unlikes-1;
			}
		}
		else if(data["unlike"]=="inc" && data["like"]=="flat")
		{
			number_of_unlikes=number_of_unlikes+1;
		}
		else if(data["unlike"]=="flat" && data["like"]=="inc")
		{
			number_of_likes=number_of_likes+1;
		}
		else
		{
			//do nothing
		}
		$("#like_"+discussion_id).text(number_of_likes.toString()+" likes");
		$("#unlike_"+discussion_id).text(number_of_unlikes.toString()+" unlikes");
		//alert(data);

	});
}

function enable_locations(value)
{
	if(value=='yes')
	{
		$('#state_select_postdisc').prop('disabled',false);
		$('#city_select_postdisc').prop('disabled',false);
		$('#locality_select_postdisc').prop('disabled',false);
	}
	else
	{
		$('#state_select_postdisc').prop('disabled',true);
		$('#city_select_postdisc').prop('disabled',true);
		$('#locality_select_postdisc').prop('disabled',true);
	}
}

function populate_disc_sub_cat_dropdown(prime_cat_name)
{
	lower_prime_cat_name=prime_cat_name.toLowerCase();
	if(lower_prime_cat_name.indexOf("select")==-1)
	{
		$.ajax({
			url:'http://localhost:8000/fringe_circle/get_subcat_names/'+prime_cat_name+'/',
			dataType:'json',
		}).done(function(data){
			$('#post_disc_sub_cat_name').empty();
			$('#post_disc_sub_cat_name').append("<option> Select sub-category</option>");
			for(var i=0;i<data.length;i++)
			{
				$('#post_disc_sub_cat_name').append("<option value='"+data[i]+"'>"+data[i]+"</option>");
			}
		//alert(data.length);
	});
	}
}

function populate_city_postdisc(state_name)
{
	var lower_state_name=state_name.toLowerCase();
	if(lower_state_name.indexOf("select")==-1){
		$.ajax({
			url:'/fringe_circle/fetch_city_names/'+state_name+'/',
			dataType:'json',
		}).done(function(data){
			$('#city_select_postdisc').empty();
			$('#city_select_postdisc').append('<option>Select City</option>');
			for (var i=0;i<data.length;i++)
			{
				$('#city_select_postdisc').append("<option value='"+data[i]+"'>"+data[i]+"</option>");
			}
		});
	}
}

function populate_locality_postdisc(city_name){
	var lower_city_name=city_name.toLowerCase();
	if(lower_city_name.indexOf("select")==-1)
	{
		$.ajax({
			url:'/fringe_circle/fetch_locality_names/'+city_name+'/',
			dataType:'json',
		}).done(function(data){
			$('#locality_select_postdisc').empty();
			$('#locality_select_postdisc').append('<option>Select Locality</option>');
			for(var i=0;i<data.length;i++)
			{
				$('#locality_select_postdisc').append("<option value='"+data[i]+"'>"+data[i]+"</option>");
			}
		});
	}
}
function post_reply(text_id,discussion_id)
{
	var replytext=$('#'+text_id).val();
	if(replytext.length!=0)
	{
		$.ajaxSetup({
			beforeSend:function(xhr,settings){
				if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
             // Only send the token to relative URLs i.e. locally.
             xhr.setRequestHeader("X-CSRFToken", get_cookie('csrftoken'));
         }
     }
 });

		$.ajax({
			type:'POST',
		// contentType: 'application/json; charset=utf-8',
		url:'/fringe_circle/create_discussion_reply/'+discussion_id+'/',
		data:{'reply_text':replytext},
		dataType:'text',
		timeout:5000,
	}).done(function(data){
		var parseData=JSON.parse(data);
		create_reply(parseData);
	});
}
}

function post_board_replies(text_id,discussion_id)
{
	var replytext=$('#'+text_id).val();
	if(replytext.length!=0)
		{
			$("#formno_"+discussion_id).submit();
		}
}

function get_cookie(name)
{
	var cookie_value=null;
	if(document.cookie && document.cookie !='')
	{
		var cookies=document.cookie.split(';');
		for (var i=0;i<cookies.length;i++)
		{
			var cookie=jQuery.trim(cookies[i]);

			//checking if cookie begins with the name we want
			if(cookie.substring(0,name.length+1)==(name+'='))
			{
				cookie_value=decodeURIComponent(cookie.substring(name.length+1,cookie.length));
				break;
			}
		}
	}
	return cookie_value;
}
function test()
{
	create_discussion();
}
// function create_discussion_reply(text_id,discussion_id)
// {
// var reply_data=post_reply(text_id,discussion_id);
// alert(reply_data["reply_user"]);
// }
function create_reply(reply_element){
	var main_disc_div=document.getElementById("disc-div-main");

	var reply_div=document.createElement("div");
	$(reply_div).addClass("disc-name");
	$(main_disc_div).append(reply_div);

	var info_div=document.createElement("div");
	$(info_div).addClass("user-disc-name");
	$(reply_div).append(info_div);

	$(info_div).append('<span class="datef"><font class="snb_date">'+reply_element["reply_date"]+'</font></span>');
	$(info_div).append('<div class="dis-name">'+reply_element["reply_user"]+'</div>');
	$(info_div).append('<div class="dis-rply"><img src="/static/fringe_discussion/images/disc-rply.png"></div>');
	$(info_div).append('<div class="dis-name">'+reply_element["discussion_user"]+'</div>');

	$(reply_div).append("<p>"+reply_element["text"]+"</p>");

	var sprit_div=document.createElement("div");
	$(sprit_div).addClass("sprit-icon");
	$(reply_div).append(sprit_div);
	$(sprit_div).append('<span class="cal">'+reply_element["reply_date"]+'</span>');
	$(sprit_div).append('<span class="like">'+reply_element["likes"]+' Likes</span>');
	$(sprit_div).append('<span class="unlike">'+reply_element["unlikes"]+' Unlikes</span>');

}
function create_discussion(discussion_element){
	var fringeDiscDivElement=document.createElement('div');
	$(fringeDiscDivElement).addClass('fringe-disc');
	$('#catWrap').append(fringeDiscDivElement);

	var fringeDiscRowDivElement=document.createElement('div');
	$(fringeDiscRowDivElement).addClass('fringe-disc-row');
	$(fringeDiscDivElement).append(fringeDiscRowDivElement);

	var fringeUserDivElement=document.createElement('div');
	$(fringeUserDivElement).addClass('fringe-user');
	$(fringeDiscRowDivElement).append(fringeUserDivElement);

	var userIconImgElement=document.createElement('img');
	$(userIconImgElement).attr('src','/static/fringe_discussion/images/fri-user.png');
	$(fringeUserDivElement).append(userIconImgElement);

	var fringeChatDivElement=document.createElement('div');
	$(fringeChatDivElement).addClass('fringe-chat');
	$(fringeDiscRowDivElement).append(fringeChatDivElement);

	var fringeSocialDivElement=document.createElement('div');
	$(fringeSocialDivElement).addClass('fring-social');
	$(fringeChatDivElement).append(fringeSocialDivElement);

	$(fringeSocialDivElement).append('<a href="#" class="fb"></a> <a href="#" class="gt"></a> <a href="#" class="twttr"></a>');

	$(fringeChatDivElement).append('<h2><a href="/fringe_circle/fringe_individual_discussion/{{ discussion.id }}">{{ discussion.title }}</a></h2>');

	$(fringeChatDivElement).append('<div class="fringe-month">{{ discussion.user.name }} asked  -  {{discussion.category.name}}:{{ discussion.subcategory.name }} - {{ discussion.publish_date }}</div>');

	$(fringeChatDivElement).append('<div class="fringe-que">{{ discussion.description }} <a href="/fringe_circle/fringe_individual_discussion/{{ discussion.id }}" class="rdmore">Read more »</a> </div>');

	$(fringeChatDivElement).append('<div class="fringe-ans">Answer this discussion</div>');

	$(fringeChatDivElement).append('<div class="sprit-icon"> <span class="cal">{{ discussion.publish_date }}</span> <span class="ans">12 Answer</span> <span class="rep">Reply</span> <span class="like">2 Like</span> <span class="unlike">0 Unlike</span> <span class="foll">Follow</span> <span class="share">Share</span> </div>');
}