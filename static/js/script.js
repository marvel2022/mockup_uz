  //fakeloader
  $(document).ready(function(){
    $.fakeLoader({
      timeToHide:2200,
      bgColor:"#3F4A5C",
      // bgImage: ,
      // spinner:"spinner1",
      //spinner:"spinner2",
      // spinner:"spinner3",
      // spinner:"spinner4",
      //spinner:"spinner5",
      //spinner:"spinner6",
      spinner:"spinner7"
    });
  });




  // Crol to top
  var $btnTop = $(".btn-top");
  $(window).on("scroll",function(){
    if($(window).scrollTop() >= 20)
    {
      $btnTop.fadeIn();
    }
    else{
      $btnTop.fadeOut();
    }
  });
  $btnTop.on("click",function(){
    $("html,body").animate({scrollTop:0},1200)
  });

