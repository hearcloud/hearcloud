$(document).ready(function ($) {
    menuActive();
    EditSong();
});

/* Function to add an "active" tag to the current page menu tag */
function menuActive() { // Function to toggle active menu links
    $('.active').removeClass('active'); // Remove "active" class on menu links
    var pgpath = window.location.pathname; // Get the page path
    $(".navbar-nav a").each(function () {
        if ($(this).attr("href") == pgpath || $(this).attr("href") == '') { // Compare url to links
            $(this).parents('li').each(function () {
                if($(this).parents('.user-nav').length === 0) { // Split active if is the user section
                    $(this).addClass('active'); // Set "active" class
                }
            });
        }
    });
}

/* Song detail view: Edit thing */
function EditSong() {
    $('#btn-edit-song').click(function(ev) {
        $(this).hide();
        $('#btn-submit-song').show();
        $('#btn-cancel-edit-song').show();
        $('#song-details').hide();
        $('#song-details-form').show();
    });

    $('#btn-cancel-edit-song').click(function(ev) {
        $(this).hide();
        $('#btn-submit-song').hide();
        $('#btn-edit-song').show();
        $('#song-details').show();
        $('#song-details-form').hide();
    });

    $('#btn-submit-song').click(function(ev) {
        console.log("Song Submit");
        $('#song-details-form').submit();
    });
}
