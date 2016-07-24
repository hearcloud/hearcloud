$(function(){
    $('#query').keyup(function(){
        $.ajax({
            type: "POST",
            url: "search/",
            data: {
                'search_text' : $('#query').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });
});

function searchSuccess(data, textStatus, jqXHR){
    //$('#music-collection-table').remove();
    //html(data);
}
