$(function(){
    $('#the-node').contextMenu({
        selector: 'div',
        callback: function(key, options) {
            var m = "clicked: " + key + " on " + $(this).attr('data-id');
		$.ajax({
		        url: '../movie_detail/' + $(this).attr('data-id') + '/movie/' + key,
		        type: 'POST',
		        success: function(res) {
		            var result = JSON.parse(res);
		            if (result.status == 'OK') {
		                window.location = '../movie_detail/' + $(this).attr('data-id') + '/movie/' + key;
		            } else {
		                alert(result.status);
		            }
		        },
		        error: function(error) {
		            console.log(error);
		        }
		    });
            window.console && console.log(m) || alert(m);
        },
        items: {
            "watched": {name: "Set Watched", icon: "/static/images/microscope.png"},
            "sync": {name: "Sync Media", icon: "/static/images/synced.jpg"},
            "sep1": "---------",
            "favorite": {name: "Set Favorite", icon: "/static/images/piggy.png"},
            "poo": {name: "Set Downvote", icon: "/static/images/poo-icon.png"},
            "sep2": "---------",
            "mismatch": {name: "Set Mismatch", icon: "/static/images/exclamation-circle-frame.png"},
        }
    });
});
