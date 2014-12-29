//filter item collecti	on
var filter_items=[];
var sorting_items=[];
var price='10000_40000';

function get_filter_ads_sort(sort_value,ad_parameters)
{
	sorting_items=$.grep(sorting_items,function(element,index){
		return element.filter_name!='price_sort';
	});

	sorting_items.push({filter_name:'price_sort',filter_value:sort_value});
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
		url:'/fringe_circle/acceptdata/'+ad_parameters+'/',
		data:{'filter_Data':JSON.stringify(filter_items),'price_data':price,'sorting_items':JSON.stringify(sorting_items)},
		dataType:'text',
		timeout:5000,
	}).done(function(result){
		var location=window.location.href;
		if (location.indexOf("/fringe_circle/product_list/Cars/")!=-1){
			$('#catWrapElement').empty();
			jsonDataArray=JSON.parse(result);
			for (var i=0;i<jsonDataArray.length;i++)
			{
				create_ad_element_list(jsonDataArray[i]);
			}
		}
		else{
			$('#catWrapElement').empty();
			jsonDataArray=JSON.parse(result);
			for (var i=0;i<jsonDataArray.length;i++)
			{
				create_ad_element_grid(jsonDataArray[i]);
			}
		}
	});

}

function get_filter_ads(current_filter,ad_parameters)
{
	if($(current_filter).is(':checked'))
	{
		filter_items.push({filter_id:current_filter.id,filter_name:current_filter.name,filter_value:current_filter.value});
	}
	else
	{
		filter_items=$.grep(filter_items,function(element,index){
			return element.filter_value!=current_filter.value;
		});
	}

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
		url:'/fringe_circle/acceptdata/'+ad_parameters+'/',
		data:{'filter_Data':JSON.stringify(filter_items),'price_data':price,'sorting_items':JSON.stringify(sorting_items)},
		dataType:'text',
		timeout:5000,
	}).done(function(result){
		var location=window.location.href;
		if (location.indexOf("/fringe_circle/product_list/Cars/")!=-1){
			$('#catWrapElement').empty();
			jsonDataArray=JSON.parse(result);
			for (var i=0;i<jsonDataArray.length;i++)
			{
				create_ad_element_list(jsonDataArray[i]);
			}
		}
		else
		{
			$('#catWrapElement').empty();
			jsonDataArray=JSON.parse(result);
			for (var i=0;i<jsonDataArray.length;i++)
			{
				create_ad_element_grid(jsonDataArray[i]);
			}	
		}
		
	});
}

function get_filter_ads_price(price_min,price_max,ad_parameters)
{	

	price=price_min+"_"+price_max;
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
		url:'/fringe_circle/acceptdata/'+ad_parameters+'/',
		data:{'filter_Data':JSON.stringify(filter_items),'price_data':price,'sorting_items':JSON.stringify(sorting_items)},
		dataType:'text',
		timeout:5000,
	}).done(function(result){
		var location=window.location.href;
		if (location.indexOf("/fringe_circle/product_list/Cars/")!=-1){
			$('#catWrapElement').empty();
			jsonDataArray=JSON.parse(result);
			for (var i=0;i<jsonDataArray.length;i++)
			{
				create_ad_element_list(jsonDataArray[i]);
			}
		}
		else{

			$('#catWrapElement').empty();
			jsonDataArray=JSON.parse(result);
			for (var i=0;i<jsonDataArray.length;i++)
			{
				create_ad_element_grid(jsonDataArray[i]);
			}
		}
		
	});
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

function get_likes_dislikes(status)
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
		url:'/fringe_circle/acceptdata/',
		data:{'topic':'random_data'},
		dataType:'text'	
	}).done(function(data){
		alert(data);
	});

}

function create_ad_element_list(ad_element)
{
	// main division for the ad element
	var catItemDiv=document.createElement("div");
	
	$(catItemDiv).addClass("catItem");
	//apending main ad div to the cat list item
	$("#catWrapElement").append(catItemDiv);

	// anchor element for containing thumbnail image of the ad
	var imageThumbnailAnchorElement=document.createElement("a");

	$(imageThumbnailAnchorElement).attr('href','/fringe_circle/ad/'+ad_element['id']+'/');

	// appending anchor element to cat item div
	$(catItemDiv).append(imageThumbnailAnchorElement);

	//creating division for thumbnail image of ad
	var divThumbnailAnchorElement=document.createElement("div");

	$(divThumbnailAnchorElement).addClass('itemThumb');

	//appending the thumnail div to the thumbnail anchor
	$(imageThumbnailAnchorElement).append(divThumbnailAnchorElement);

	//creating new/old label division for image thumbnail
	var labelDivThumbnailAnchorElement=document.createElement("div");

	$(labelDivThumbnailAnchorElement).text("used");
	$(labelDivThumbnailAnchorElement).addClass("lbl used");

	//appending new/old label division for image thumbnail to the thumbnail division of anchor element
	$(divThumbnailAnchorElement).append(labelDivThumbnailAnchorElement);

	//creating image element for the thumbnail anchor element
	var thumbImgThumbnailAnchorElement=document.createElement("img");

	$(thumbImgThumbnailAnchorElement).attr('src','/static/fringe_x/images/no_photo_available.png');

	//appending image element for the thumbnail anchor element to the thumbnail division of anchor element
	$(divThumbnailAnchorElement).append(thumbImgThumbnailAnchorElement);

	//creating division containing reply button and date
	var dateReplyBtnDivElement=document.createElement("div");

	$(dateReplyBtnDivElement).attr('id','list_reply');
	$(dateReplyBtnDivElement).addClass('grid-right');

	//appending division contatining reply button and date
	$(catItemDiv).append(dateReplyBtnDivElement);

	//creating span element for containing the date
	var dateSpanElement=document.createElement('span');
	var dateFontElement=document.createElement('Font');
	$(dateSpanElement).addClass('datef');
	$(dateFontElement).addClass('snb_date');
	$(dateFontElement).text(ad_element['duration']);

	//appending span element for containing the date
	$(dateReplyBtnDivElement).append(dateSpanElement);
	$(dateSpanElement).append(dateFontElement);

	// creating href element for reply button 
	var replyHrefElement=document.createElement("a");

	$(replyHrefElement).attr('href','#');
	$(replyHrefElement).text('Reply');

	// appending href element for reply button 
	$(dateReplyBtnDivElement).append(replyHrefElement);

	//creating anchor element for details of the ad
	var adDetailAnchorElement=document.createElement('a');

	$(adDetailAnchorElement).attr('href',document.location);

	//appending anchor element for details of the ad
	$(catItemDiv).append(adDetailAnchorElement);

	//creating div element for details of the ad
	var divDetailElement=document.createElement('div');

	$(divDetailElement).addClass('item-lst');

	//appending div element for details of the ad
	$(adDetailAnchorElement).append(divDetailElement);

	//creating div element for price
	var divPriceElement=document.createElement('div');

	$(divPriceElement).addClass('rs');
	$(divPriceElement).attr('style','text-decoration:none;color:#000;');
	$(divPriceElement).text("Rs"+ad_element['price']);

	//appending div element for price
	$(divDetailElement).append(divPriceElement);

	//creating div element for further details
	var divFurtherDetailElement=document.createElement('div');

	$(divFurtherDetailElement).addClass('detailTxt');

	//appending div element for further elements
	$(divDetailElement).append(divFurtherDetailElement);

	//creating and appending title heading in the further detail element
	$(divFurtherDetailElement).append('<h3 class="proName">'+ad_element['title']+'</h3>');

	//creating and appending description paragraph in the further detail element
	$(divFurtherDetailElement).append('<p>'+ad_element['description']+'</p>');

	//creating div element for location and subcategory
	var subcatLocationDivElement=document.createElement('div');

	$(subcatLocationDivElement).addClass('grid-chicklet');

	//appending div element for location and subcategory
	$(divFurtherDetailElement).append(subcatLocationDivElement);

	//creating and appending subcategory anchor
	$(subcatLocationDivElement).append('<a href="#">'+ad_element['subcategory_name']+'</a>');

	//creatinf and appending locality anchor
	$(subcatLocationDivElement).append('<a href="#">'+ad_element['locality_name']+'</a>');

	//creating and appending city anchor
	$(subcatLocationDivElement).append('<a href="#">'+ad_element['city_name']+'</a>');

	$(subcatLocationDivElement).append('<div class="postTym"></div>');
}


function create_ad_element_grid(ad_element)
{
	//creating main ad grid division
	var adGridItem=document.createElement('div');
	$(adGridItem).addClass('grig-bx active');
	$(adGridItem).attr('id','adGridItem'+index);

	$('#catWrapElement').append(adGridItem);

	//creating and appending title and state element
	$(adGridItem).append('<h3 class="adtitlesnb"><a href="">'+ad_element['title']+'</a> : <a href="#" class="normal">'+ad_element['state_name']+'</a></h3>');

	//creating division for subcategory , locality and city element
	var subcatLocationDivElement=document.createElement('div');

	$(subcatLocationDivElement).addClass('grid-chicklet');

	//appending division for subcategory, locality and city element
	$(adGridItem).append(subcatLocationDivElement);

	//creating and appending subcategory href element
	$(subcatLocationDivElement).append('<a href="#">subcategory</a>');

	//creating and appending locality href element
	$(subcatLocationDivElement).append('<a href="#">locality</a>');

	//creating and appending city href element
	$(subcatLocationDivElement).append('<a href="#">City</a>');

	//creating anchor for thumbnail image
	var thumbnailAnchorElement=document.createElement('a');

	$(thumbnailAnchorElement).attr('href',window.location);

	//appending anchor for thumbnail image 
	$(adGridItem).append(thumbnailAnchorElement);

	//creating 	thumbnail division for image
	var thumbnailDivElement=document.createElement('div');

	$(thumbnailDivElement).addClass('grid_image');

	//appending thumbnail division for image
	$(thumbnailAnchorElement).append(thumbnailDivElement);

	//creating img element for thumbnail image
	var imgThumbnailElement=document.createElement('img');

	$(imgThumbnailElement).attr('src','/static/fringe_x/images/no_photo_available.png');

	//appending img element for thumbnail image
	$(thumbnailDivElement).append(imgThumbnailElement);

	//creating and appending price element

	$(adGridItem).append('<div class="grid-lft"><div class="rs">Rs.123455</div></div>');

	//creating and appending reply and date item
	$(adGridItem).append('<div class="grid-right" style="width:50%;"><span class="datef"><font class="snb_date"> random date </font></span><a href="#">Reply</a></div>');

}