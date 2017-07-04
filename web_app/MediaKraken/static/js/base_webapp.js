$(function(){
    $('#the-movie-node').contextMenu({
        selector: 'div',
        callback: function(key, options) {
            var m = "clicked: " + key + " on " + $(this).attr('data-id');
		$.ajax({
		        url: '/users/movie_status/' + $(this).attr('data-id') + '/' + key,
		        type: 'POST',
		        success: function(res) {
		            var result = JSON.parse(res);
		            if (result.status == 'OK') {
		                continue;
//                        window.location = '/users/movie/All';
		            } else {
		                alert(result.status);
		            }
		        },
		        error: function(error) {
		            console.log(error);
		        }
		    });
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


$(function(){
    $('#the-movie-metadata-node').contextMenu({
        selector: 'div',
        callback: function(key, options) {
            var m = "clicked: " + key + " on " + $(this).attr('data-id');
		$.ajax({
		        url: '/users/movie_metadata_status/' + $(this).attr('data-id') + '/' + key,
		        type: 'POST',
		        success: function(res) {
		            var result = JSON.parse(res);
		            if (result.status == 'OK') {
		                continue;
//		                window.location = '/users/meta_movie_list';
		            } else {
		                alert(result.status);
		            }
		        },
		        error: function(error) {
		            console.log(error);
		        }
		    });
        },
        items: {
            "watched": {name: "Set Watched", icon: "/static/images/microscope.png"},
            "sep1": "---------",
            "favorite": {name: "Set Favorite", icon: "/static/images/piggy.png"},
            "poo": {name: "Set Downvote", icon: "/static/images/poo-icon.png"},
        }
    });
});


$(function(){
    $('#the-tv-node').contextMenu({
        selector: 'div',
        callback: function(key, options) {
            var m = "clicked: " + key + " on " + $(this).attr('data-id');
		$.ajax({
		        url: '/users/tv_status/' + $(this).attr('data-id') + '/' + key,
		        type: 'POST',
		        success: function(res) {
		            var result = JSON.parse(res);
		            if (result.status == 'OK') {
		                continue;
//		                window.location = '/users/tv_status/' + $(this).attr('data-id') + '/' + key;
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
            "watched": {name: "Set Episode Watched", icon: "/static/images/microscope.png"},
            "watched_season": {name: "Set Season Watched", icon: "/static/images/microscope.png"},
            "watched_show": {name: "Set Show Watched", icon: "/static/images/microscope.png"},
            "sync": {name: "Sync Episdoe Media", icon: "/static/images/synced.jpg"},
            "sync_season": {name: "Sync Season Media", icon: "/static/images/synced.jpg"},
            "sync_show": {name: "Sync Show Media", icon: "/static/images/synced.jpg"},
            "sep1": "---------",
            "favorite": {name: "Set Episdoe Favorite", icon: "/static/images/piggy.png"},
            "favorite_season": {name: "Set Season Favorite", icon: "/static/images/piggy.png"},
            "favorite_show": {name: "Set Show Favorite", icon: "/static/images/piggy.png"},
            "poo": {name: "Set Episode Downvote", icon: "/static/images/poo-icon.png"},
            "poo_season": {name: "Set Season Downvote", icon: "/static/images/poo-icon.png"},
            "poo_show": {name: "Set Show Downvote", icon: "/static/images/poo-icon.png"},
            "sep2": "---------",
            "mismatch": {name: "Set Episode Mismatch", icon: "/static/images/exclamation-circle-frame.png"},
            "mismatch_season": {name: "Set Season Mismatch", icon: "/static/images/exclamation-circle-frame.png"},
            "mismatch_show": {name: "Set Show Mismatch", icon: "/static/images/exclamation-circle-frame.png"},
        }
    });
});
