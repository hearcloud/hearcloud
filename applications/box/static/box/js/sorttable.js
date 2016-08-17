  function sortTable(f,n){
	  var rows = $('#music-collection-table tbody tr').get();

	  rows.sort(function(a, b){
        var A = getVal(a);
		    var B = getVal(b);

		    if(A < B) {
			    return -1*f;
		    }
		    if(A > B) {
			    return 1*f;
		    }
		    return 0;
	  });

	  function getVal(elm){
		  var v = $(elm).children('td').eq(n).text().toUpperCase();
		  if($.isNumeric(v)){
			    v = parseInt(v,10);
		  }
		  return v;
	  }

	  $.each(rows, function(index, row) {
		  $('#music-collection-table').children('tbody').append(row);
	  });
  }

  function changeArrow(col, trigger){
      // Descending
      if(trigger === 1){
          if($("#music-collection-table").find(".glyphicon-arrow-down"))
              $("#music-collection-table").find(".glyphicon-arrow-down").removeClass("glyphicon-arrow-down");
          if($("#music-collection-table").find(".glyphicon-arrow-up"))
              $("#music-collection-table").find(".glyphicon-arrow-up").removeClass("glyphicon-arrow-up");

          col.children(".sorting-arrow").addClass("glyphicon-arrow-down");
      }
      // Ascending
      else if(trigger === -1){
          if($("#music-collection-table").find(".glyphicon-arrow-down"))
              $("#music-collection-table").find(".glyphicon-arrow-down").removeClass("glyphicon-arrow-down");
          if($("#music-collection-table").find(".glyphicon-arrow-up"))
              $("#music-collection-table").find(".glyphicon-arrow-up").removeClass("glyphicon-arrow-up");

          col.children(".sorting-arrow").addClass("glyphicon-arrow-up");
      }
  }

  var f_title = 1;
  var f_artist = -1;
  var f_album = -1;
  var f_time = -1;
  var f_ctime = -1;
  var f_mtime = -1;

  $("#col-title").click(function(){
      f_title *= -1;
      var n = $(this).prevAll().length+1;
      sortTable(f_title,n);
      changeArrow($(this), f_title);
  });

  $("#col-artist").click(function(){
      f_artist *= -1;
      var n = $(this).prevAll().length+1;
      sortTable(f_artist,n);
      changeArrow($(this), f_artist);
  });

  $("#col-album").click(function(){
      f_album *= -1;
      var n = $(this).prevAll().length+1;
      sortTable(f_album,n);
      changeArrow($(this), f_album);
  });

  $("#col-time").click(function(){
      f_time *= -1;
      var n = $(this).prevAll().length+1;
      sortTable(f_time,n);
      changeArrow($(this), f_time);
  });

  $("#col-ctime").click(function(){
      f_ctime *= -1;
      var n = $(this).prevAll().length+1;
      sortTable(f_ctime,n);
      changeArrow($(this), f_ctime);
  });

  $("#col-mtime").click(function(){
      f_mtime *= -1;
      var n = $(this).prevAll().length+1;
      sortTable(f_mtime,n);
      changeArrow($(this), f_mtime);
  });
