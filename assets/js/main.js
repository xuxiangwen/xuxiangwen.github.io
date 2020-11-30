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


$(window).resize(sectionHeight);

$(function() {
  $("section h2, section h3").each(function(){
    $("nav ul").append("<li class='tag-" + this.nodeName.toLowerCase() + "'><a href='#" + $(this).text().toLowerCase().replace(/ /g, '-').replace(/[\+\=\(\),:：\.]/g,'-') + "'>" + $(this).text() + "</a></li>");
    $(this).attr("id",$(this).text().toLowerCase().replace(/ /g, '-').replace(/[\+\=\(\),:：\.]/g,'-'));
    $("nav ul li:first-child a").parent().addClass("active");
  });

  $("nav ul li").on("click", "a", function(event) {
    var position = $($(this).attr("href")).offset().top - 90;
    $("html, body").animate({scrollTop: position}, 400);
    $("nav ul li a").parent().removeClass("active");
    $(this).parent().addClass("active");
    event.preventDefault();
    console.log($(this).text)  
  });

  sectionHeight();

  $('img').on('load', sectionHeight);
});

$(document).ready(function() {
    $("aside ul li a").on("click", function (e) {
       console.log('a click: scrollTop=' +$("aside").scrollTop())
       document.cookie = "scrollTop=" + $("aside").scrollTop() + "; path=/"; 
       return true;
    });    
    if(document.cookie.match(/scrollTop=([^;]+)(;|$)/) != null) {
        var arr = document.cookie.match(/scrollTop=([^;]+)(;|$)/); 
        scroll_top = parseInt(arr[1])
        $("aside").animate({scrollTop: scroll_top}, 0);
        console.log('ready: scrollTop=' + scroll_top )
    }   
})

window.onload = function() {
    if(document.cookie.match(/scrollTop=([^;]+)(;|$)/) != null) {
        var arr = document.cookie.match(/scrollTop=([^;]+)(;|$)/); 
        scroll_top = parseInt(arr[1])
        console.log('onload: scrollTop=' + scroll_top )
    }       
}
