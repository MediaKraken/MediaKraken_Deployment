$(function() {
    var function_media_status = function(media_guid, media_type, media_status) {
        $.ajax({
                url: '../media_status/' + media_guid + '/' + media_type + '/' + media_status,
                data: {
                    id: media_guid
                },
                type: 'POST',
                success: function(res) {
                    var result = JSON.parse(res);
                    if (result.status == 'OK') {
                        window.location = '../media_status/' + media_guid + '/' + media_type + '/' + media_status;
                    } else {
                        alert(result.status);
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });
        };

    $('.media_context_right').contextPopup({
        title: 'Media Option',
        items: [{
                label: 'Set Watched',
                icon: '../../static/images/microscope.png',
                action: function() function_media_status($('.media_context_right').data("id"), 'movie', 'watched')
            }, {
                label: 'Sync Media',
                icon: '../../static/images/synced.jpg',
                action: function() function_media_status($('.media_context_right').data("id"), 'movie', 'sync')
            },
            null, {
                label: 'Set Favorite',
                icon: '../../static/images/piggy.png',
                action: function() function_media_status($('.media_context_right').data("id"), 'movie', 'favorite')
            }, {
                label: 'Set Downvote',
                icon: '../../static/images/poo-icon.png',
                action: function() function_media_status($('.media_context_right').data("id"), 'movie', 'poo')
            },
            null, {
                label: 'Set Mismatch',
                icon: '../../static/images/exclamation-circle-frame.png',
                action: function() function_media_status($('.media_context_right').data("id"), 'move', 'mismatch')
            }
        ]
    });
});
