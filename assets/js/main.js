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
  $("html, body").animate({scrollTop: position}, scroll_time);
}    

var binary_search = function(x, item) {
    low = 0
    high = x.length-1
    while (low<high){
        mid = parseInt((low + high)/2)
        if (x[mid]==item) {
            high = mid        
        } else if (x[mid]>item) {
            high = mid-1                             
        } else {
            low = mid+1
        }
    }  
    if (x[low]>item) return low -1
    return low
}

var  locate_catalog = function(){
  var headers = $('section h2, section h3');
  var catalog = $('nav ul li a');    
  var scroll_height = $(window).scrollTop()+120;
  var positions = [];
  console.log(positions)
  for(let i =0;i<headers.length;i++){
    positions[i] =  $(headers[i]).offset().top
  }
  var index = binary_search(positions, scroll_height) 
  catalog.removeClass('active'); 
  console.log(index, scroll_height)
  if (index >= 0) {
    $(catalog[index]).addClass('active');      
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
    scroll_to_anchor($($(this).attr("href")).offset().top, 200)        
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



