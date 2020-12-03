var sectionHeight = function() {
  var total    = $(window).height(),
      $section = $('section').css('height','auto');

  if ($section.outerHeight(true) < total) {
    var margin = $section.outerHeight(true) - $section.height();
    $section.height(total - margin - 20);
  } else {
    $section.css('height','auto');
  }
}

var scroll_to_anchor = function(pos, scroll_time){
  var position = pos - 90; 
//   console.log('scroll_to_position:' + position)
  $("html, body").animate({scrollTop: position}, scroll_time);
}    

var  locate_catalog = function(){
  var headers = $('section h2, section h3');
  var catalog = $('nav ul li a');    
  var scroll_height = $(window).scrollTop()+120;
  for(var i =0;i<headers.length;i++){
    var header_height = $(headers[i]).offset().top;    
    if (header_height<scroll_height){  
      catalog.removeClass('active'); 
      $(catalog[i]).addClass('active');
    }
  }
}

$(window).resize(sectionHeight);

$(function() {
  var outline = new Map();
  $("section h2, section h3").each(function(){
    var current_id = $(this).text().toLowerCase().replace(/ /g, '-').replace(/[\+\=\(\),:：\.\{\}\/\$?]/g,'-');
   
    // 对于相同标题的内容，添加递增序号，区别开来   
    if (outline.has(current_id)) {
      var no = outline.get(current_id) + 1;  
      outline.set(current_id, no);   
      current_id = current_id + '_' + no;
    } else {
      outline.set(current_id, 1);        
    }        

    $(this).attr("id", current_id);  
    $("nav ul").append("<li class='tag-" + this.nodeName.toLowerCase() + "'><a href='#" + current_id + "'>" + $(this).text() + "</a></li>");
  });

  $("nav ul li").on("click", "a", function(event) {     
    scroll_to_anchor($($(this).attr("href")).offset().top, 250)  
//     setTimeout(() => {
//       $("nav ul li a").removeClass('active'); 
//       $(this).addClass('active');
//     }, 410);        
    event.preventDefault();
  });

  sectionHeight();

  $('img').on('load', sectionHeight);
    
  $("aside ul li a").on("click", function (e) {
     document.cookie = "scrollTop=" + $("aside").scrollTop() + "; path=/"; 
     return true;
  });    
    
  if(document.cookie.match(/scrollTop=([^;]+)(;|$)/) != null) {
    var arr = document.cookie.match(/scrollTop=([^;]+)(;|$)/); 
    scroll_top = parseInt(arr[1])
    $("aside").animate({scrollTop: scroll_top}, 0);
  }   
    
  /*绑定滚动事件 */   
  $(window).bind('scroll', locate_catalog);   

});



window.onload = function() {
    if (window.location.hash.length>0 ){      
      var position = $("html, body").scrollTop();
      if (position>0) {
          scroll_to_anchor(position, 0);   
          locate_catalog()
      }    
    }  
}



