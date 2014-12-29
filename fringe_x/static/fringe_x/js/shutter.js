$(document).ready(function(){

	
	if(!(/webOS|iPhone|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent) )) {
		var windowHeight = $(window).height();
		
		$('.flexslider').css('height',windowHeight-180);
		$('.flex-container .flexslider .slides img').css('height',windowHeight-180);
		
	
		
	}
	
	
	
	
			
});


   $(document).ready(function(){
        $("#nav-mobile").html($("#nav-main").html());
        $("#nav-trigger span").click(function(){
            if ($("nav#nav-mobile ul").hasClass("expanded")) {
                $("nav#nav-mobile ul.expanded").removeClass("expanded").slideUp(250);
                $(this).removeClass("open");
            } else {
                $("nav#nav-mobile ul").addClass("expanded").slideDown(250);
                $(this).addClass("open");
            }
        });
    });
			
 
 
 
	


