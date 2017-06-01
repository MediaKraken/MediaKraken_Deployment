$(function() {
    var function_media_status = function(media_type, media_status) {
        $.ajax({
                url: '../media_status/' + $(this).attr('id') + '/' + media_type + '/' + media_status,
                type: 'POST',
                success: function(res) {
                    var result = JSON.parse(res);
                    if (result.status == 'OK') {
                        window.location = '../media_status/' + $(this).attr('id') + '/' + media_type + '/' + media_status;
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
                action: function() function_media_status('movie', 'watched')
            }, {
                label: 'Sync Media',
                icon: '../../static/images/synced.jpg',
                action: function() function_media_status('movie', 'sync')
            },
            null, {
                label: 'Set Favorite',
                icon: '../../static/images/piggy.png',
                action: function() function_media_status('movie', 'favorite')
            }, {
                label: 'Set Downvote',
                icon: '../../static/images/poo-icon.png',
                action: function() function_media_status('movie', 'poo')
            },
            null, {
                label: 'Set Mismatch',
                icon: '../../static/images/exclamation-circle-frame.png',
                action: function() function_media_status('movie', 'mismatch')
            }
        ]
    });
});


$(function(){
    $('#the-node').contextMenu({
        selector: 'div', 
        callback: function(key, options) {
            var m = "clicked: " + key + " on " + $(this).text();
            window.console && console.log(m) || alert(m); 
        },
        items: {
            "edit": {name: "Edit", icon: "edit"},
            "cut": {name: "Cut", icon: "cut"},
            "copy": {name: "Copy", icon: "copy"},
            "paste": {name: "Paste", icon: "paste"},
            "delete": {name: "Delete", icon: "delete"},
            "sep1": "---------",
            "quit": {name: "Quit", icon: function($element, key, item){ return 'context-menu-icon context-menu-icon-quit'; }}
        }
    });
});

