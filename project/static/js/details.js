$(document).ready(function() {
    setVoteButtonsWidth();
});


function setVoteButtonsWidth() {
   $('.vote-button').width(
        Math.max.apply( 
            Math, 
            $('.vote-button').map(function(){
                return $(this).width();
            }).get()
        )
    ); 
};
