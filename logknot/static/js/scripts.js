function mansionDB_script() {

  this.ready = function(){
    const _this = this;
    _this._SlidePropertyList();
    _this._SlidePropertyDetail();
    _this._SlideIntoPropertyList();
    _this._Wishlist();
    _this._Navigation();
    _this._SearchCondition();
    _this._FixedFooterBottom();
  }

  this._FixedFooterBottom = function ()
  {
    if($('.fixed-bottom').length > 0){
      const height = $('.fixed-bottom').outerHeight();
      $('footer').css('padding-bottom',height+'px');
    }
    $(window).on('resize',function(){
      if($('.fixed-bottom').length > 0){
        const height = $('.fixed-bottom').outerHeight();
        $('footer').css('padding-bottom',height+'px');
      }
    });
  }

  this._SearchCondition = function () {

    const _this = this;

    $('[data-scroll]').on('click', _this.scrollToSection);

    $(".btn_call").click(function(event) {
        event.preventDefault();
        $(".btn_call span").slideToggle("fast");
    });

    $(".btnshowhide").click(function(event) {
        event.preventDefault();
        $(this).toggleClass('show');
        $(".w_box_simulation_result").slideToggle("fast");
    });

    $(".burger").click(function(event) {
        event.preventDefault();
        $('.frm_search_conditions_content').slideToggle("fast");
    });

    const burger = document.querySelector(".burger");
    if(burger){
      burger.addEventListener("click", function () {
        const body = document.body;
        body.classList.toggle("nav_open");

        // if needed to toggle multiple classes
        // const toggleClasses = ["nav-open", "overflow-hidden"];
        // toggleClasses.forEach((toggleClass) => body.classList.toggle(toggleClass));
      });
    }

    $('.plus-to-minus').click( function( event ) {
      $(this).toggleClass('minus');
    });

    $("#ck_01").click(function() {
      $("#collapseOne input[type=checkbox]").prop("checked", $(this).prop("checked"));
    });

    $("#collapseOne input[type=checkbox]").click(function() {
      if (!$(this).prop("checked")) {
        $("#ck_01").prop("checked", false);
      }
    });

  }

  this.scrollToSection = function (event) {
    event.preventDefault();
    var $section = $($(this).attr('href'));
    $('html, body').animate({
      scrollTop: $section.offset().top
    }, 500);
  }

  this._Wishlist = function () {

    $(".btn_wishlist").click(function(event){
       event.preventDefault();
      $(this).toggleClass("on");
    });

  }

  this._SlidePropertyList = function() {
    const swiper = new Swiper('.property_slide_swiper', {
      loop: true,
      pagination: {
        el: ".swiper-pagination",
        type: "fraction",
      },
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
    });
  }

  this._SlideIntoPropertyList = function() {
    const swiper = new Swiper('.property-into_swiper', {
      loop: true,
      slidesPerView: 2.9,
      spaceBetween: 10,
      breakpoints: {
        320: {
          slidesPerView: 2.2,
        },
        575: {
          slidesPerView: 2.9,
        }
      }
    });
  }

  this._SlidePropertyDetail = function() {

    const swiper_thumnail = new Swiper('.property_detail_swiper_thumnail', {
      spaceBetween: 0,
      slidesPerView: 4.8,
      freeMode: true,
      watchSlidesProgress: true,
    });
    const swiper = new Swiper('.property_detail_swiper', {
      loop: true,
      navigation: {
        nextEl: '.swiper-button-next',
        prevEl: '.swiper-button-prev',
      },
      breakpoints: {
        320: {
          slidesPerView: 1,
        },
        767: {
          slidesPerView: 2.2,
        }
      },
      thumbs: {
          swiper: swiper_thumnail,
      },
    });


  }

  this._Navigation = function() {
    const _this = this;

    $(window).on('load resize',function(){
      // On/Off fixed
      if( $(window).width() <= 767 ){
        $('.navigation').removeClass('nav-fixed nav-white');
        $('.navigation').addClass('nav-black');
      } else{
        if( !$('header').hasClass('nav-animation-scroll') ){
          $('.navigation').removeClass('nav-black');
          $('.navigation').addClass('nav-fixed nav-white');
        }
      }
    });

    $(window).scroll(function(e){
      _this.nav_animation_scroll();
    });

  }

  this.nav_animation_scroll = function(){
      const headerHeight = $('header').outerHeight();
      const win = $(window);
      const doc = $(document);
      let winHeight;
      const _header = $('header');
      if( $('body').hasClass('menu-opened') ) return;
      if( win.height() + 2*headerHeight >= doc.height() ) return;
      if( win.scrollTop() + 2 > headerHeight ){
          _header.addClass('nav-animation-scroll');
          $('.navigation').removeClass('nav-fixed nav-white');
          $('.navigation').addClass('nav-black');
      } else {
        _header.removeClass('nav-animation-scroll');
        if ( $(window).width() >= 768 ) {
          $('.navigation').removeClass('nav-black');
          $('.navigation').addClass('nav-fixed nav-white');
        }
      }
  }

}

const run_mansionDB_script = new mansionDB_script();
$(document).ready(function(){
  run_mansionDB_script.ready();
});

