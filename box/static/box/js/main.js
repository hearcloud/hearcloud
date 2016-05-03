$(document).ready(function ($) {
    menuActive();
    EditSong();
    getSong();
});

function menuActive() { // Function to toggle active menu links
    $('.active').removeClass('active'); // Remove "active" class on menu links after an ajax call
    var pgpath = window.location.pathname; // Get the page path
    $(".navbar-nav a").each(function () {
        if ($(this).attr("href") == pgpath || $(this).attr("href") == '') { // Compare url to links
            $(this).parents('li').addClass('active'); // Set "active" class
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

function getSong() { // Function to toggle active menu links
    $('.btn-play-song').click(function(ev) {
        var song_url = $(this).attr("href");
        console.log(song_url);
        
        $.ajax({
            xhr: function(){
                var xhr = new window.XMLHttpRequest();
                //Download progress
                xhr.addEventListener("progress", function(evt){
                    if (evt.lengthComputable) {
                        var percentComplete = evt.loaded / evt.total;
                        //Do something with download progress
                        console.log(percentComplete);
                    }
                }, false);
                return xhr;
            },
            url: song_url,
            type: "GET",
            dataType: 'binary',
            processData: false,
            success: function(data) {
                console.log('Success!', data);
            },
            error: function(e) {
                console.log('Error!', e);
            }

        }); 
    });
}
