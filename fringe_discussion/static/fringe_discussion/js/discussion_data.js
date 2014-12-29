sorting_items=[]

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

function get_discussions_sort(sort_value)
{
	sorting_items=$.grep(sorting_items,function(element,index){
		return element.filter_name!='discussion_sort';
	});

	sorting_items.push({filter_name:'discussion_sort',filter_value:sort_value});
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
		url:'/fringe_circle/get_filter_discussions/',
		data:{'sorting_items':JSON.stringify(sorting_items)},
		dataType:'text',
		timeout:5000,
	}).done(function(result){
			$('#catWrapElement').empty();
			jsonDataArray=JSON.parse(result);
			for (var i=0;i<jsonDataArray.length;i++)
			{
				create_discussion(jsonDataArray[i]);
			}
		
	});

}

function test()
{
	create_discussion();
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