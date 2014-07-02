$(document).ready(function(){


    console.log("form");
    $(".j_filter").change(function(event){
        console.log("submitting form");
        $("form#filter").submit();

//        $("form#filter").submit(function(event){
//            console.log("form submitted");
//        });
    });



    var loading_div;

    var container = document.querySelector('#master-gallery .gallery-container');
    if(container){
        var msnry = new Masonry( container ,
            { columnWidth: 241,gutter: 9, itemSelector: ".gallery-thumb", transitionDuration: 0 }
        );
    }

    
    $(document).on('click', '.gallery-thumb a', function(e) {
        e.preventDefault();
        
        $("main").addClass('black');

        $("#modal").show();
        $(window).scrollTop(0);

        console.log("AJAX load: "+$(this).attr('href'));
        //$("#modal").html('');
        
        $("#modal-container").load($(this).attr('href')+" #modal",function(e){

        });

    });

    $(document).on('click', '.gallery-nav', function(e) {

        e.preventDefault();

        $(window).scrollTop(0);
        console.log("AJAX load: "+$(this).attr('href'));
        $("#modal-container").load($(this).attr('href')+" #modal",function(e){

        });

    });

    $(document).on('click', '#close-modal', function(e) {
        console.log("close modal"); 
        e.preventDefault();
        $("main").removeClass('black');
        $("#modal").hide();
        
    });

    $(document).on('click', '.load-more', function(e) {

        e.preventDefault();

        console.log("AJAX load: "+$(this).attr('href'));

        $("#master-gallery .more-container .load-more").remove();
        
        $("#master-gallery .more-container .status-message").show();
        loading_div = $(); // clear div if it exists
        loading_div = $('<div>'); // create empty div to load new images into

        loading_div.load($(this).attr('href'),function(e){ // load new images into div, and once loaded, add to the masonry instance
            
            $("#master-gallery .gallery-container").append($(loading_div).find(".gallery-container").html());
            msnry.reloadItems(); 
            msnry.layout();
            $("#master-gallery .more-container .status-message").hide();
            $("#master-gallery .more-container").append($(loading_div).find(".more-container").html());
            $(loading_div).remove();

        });


        
    });
});