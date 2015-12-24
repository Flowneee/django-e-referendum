$(document).ready(function() {
    setButtonsWidth('.vote-button');
    setButtonsWidth('.edit-ref-btn')
});


function setButtonsWidth(btn_class) {
   $(btn_class).width(
        Math.max.apply( 
            Math, 
            $(btn_class).map(function(){
                return $(this).width();
            }).get()
        )
    ); 
};
