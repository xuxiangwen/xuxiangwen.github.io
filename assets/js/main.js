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

var scroll_to_anchor = function(pos){
  var position = pos.offset().top - 90;
  console.log("scroll_to_anchor: "+position)  
  $("html, body").animate({scrollTop: position}, 400);
}    

var anchor = window.location.hash;
window.location.hash = "";

$(window).resize(sectionHeight);

$(function() {
  var outline = new Map();
  $("section h2, section h3").each(function(){
    var current_id = $(this).text().toLowerCase().replace(/ /g, '-').replace(/[\+\=\(\),:：\.\{\}\/\$]/g,'-');
   
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
    $("nav ul li:first-child a").parent().addClass("active");
  });

  $("nav ul li").on("click", "a", function(event) {
    scroll_to_anchor($($(this).attr("href")))  
    //$("nav ul li a").parent().removeClass("active");
    //$(this).parent().addClass("active");
    event.preventDefault();
    //console.log($(this).text)  
  });

  sectionHeight();

  $('img').on('load', sectionHeight);
});

$(document).ready(function() {
    $("aside ul li a").on("click", function (e) {
       //console.log('a click: scrollTop=' +$("aside").scrollTop())
       document.cookie = "scrollTop=" + $("aside").scrollTop() + "; path=/"; 
       return true;
    });    
    if(document.cookie.match(/scrollTop=([^;]+)(;|$)/) != null) {
        var arr = document.cookie.match(/scrollTop=([^;]+)(;|$)/); 
        scroll_top = parseInt(arr[1])
        $("aside").animate({scrollTop: scroll_top}, 0);
        //console.log('ready: scrollTop=' + scroll_top )
    }   
})

window.onload = function() {
    if(document.cookie.match(/scrollTop=([^;]+)(;|$)/) != null) {
        var arr = document.cookie.match(/scrollTop=([^;]+)(;|$)/); 
        scroll_top = parseInt(arr[1])
        //console.log('onload: scrollTop=' + scroll_top )
    } 
    if (anchor.length>0 ){
      console.log('anchor='+anchor);
      console.log('anchor.length='+$(anchor).length);  
      if ($(anchor).length>0) {  
        scroll_to_anchor($(anchor));
      }    
      window.location.hash = anchor;  
    }    
}
