
function populate_city_list(state_name)
{
	$.ajax({
		url:'/fringe_circle/fetch_city_names/'+state_name,
		dataType:'json',
		}).done(function(data){
			$('#location_list').empty();
			var city_list=document.createElement("ul");
			city_list.id="city_list";
			$('#location_list').append(city_list);
			for(var l=0;l<data.length;l++)
			{
				var li_element=document.createElement("li");
				var city_select_anchor=document.createElement("a");
				city_select_anchor.href="/fringe_circle/location_selection/"+state_name+"_"+data[l];
				city_select_anchor.innerHTML=data[l];
				li_element.id="city_li_"+data[l];
				
				$("#city_list").append(li_element);
				$("#city_li_"+data[l]).append(city_select_anchor);				
			}
			});
}

function populate_state_list()
{
$('#location_heading').text("All States");
$.ajax({url:"/fringe_circle/fetch_state_names/",
    dataType:'json',
    }).done(function(data){
    $('#location_list').empty();
    for(var i=0;i<data.length;i++){
    if(i%9==0){
    var list_id="state_list_element_"+i.toString();
    $('#location_list').append('<ul id="'+list_id+'"></ul>');
    var upperBound=0;
    if(data.length-i<9)
    {
    upperBound=data.length-i;
    }
    else{
    upperBound=9;
    }
    for(var j=i;j<i+upperBound;j++)
    {
		/*
    var li_element=document.createElement("li");
    li_element.id="state_li";
    li_element.name="state_li_"+data[j];
    li_element.innerHTML=data[j];
    li_element.addEventListener("click",function(){
		//logic to fetch list of city
		$.ajax({
		url:'/fringe_circle/fetch_city_names/'+data[j],
		dataType:'json',
		}).done(function(data){
			$('#location_list').empty();
			});
		//logic to fetch list of city ends herex
		});*/
    $('#'+list_id).append("<li onclick=\"populate_city_list("+"'"+data[j]+"'"+");\" style='cursor:pointer;'>"+data[j]+" </li>");
     
    }
    }
    }
    });
}
