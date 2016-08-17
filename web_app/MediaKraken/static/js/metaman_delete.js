function ConfirmLinkDelete(elem) {
    localStorage.setItem('deleteId', $(elem).attr('data-id'));
    $('#delete_link').modal();
}

function Link_Delete() {
    $.ajax({
        url: '../link_delete',
        data: {
            id: localStorage.getItem('deleteId')
        },
        type: 'POST',
        success: function(res) {
            var result = JSON.parse(res);
            if (result.status == 'OK') {
                $('#delete_link').modal('hide');
                window.location = '../link_server';
            } else {
                alert(result.status);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function ConfirmSyncDelete(elem) {
    localStorage.setItem('deleteId', $(elem).attr('data-id'));
    $('#delete_sync').modal();
}

function Sync_Delete() {
    $.ajax({
        url: '../sync_delete',
        data: {
            id: localStorage.getItem('deleteId')
        },
        type: 'POST',
        success: function(res) {
            var result = JSON.parse(res);
            if (result.status == 'OK') {
                $('#delete_sync').modal('hide');
                window.location = '../sync';
            } else {
                alert(result.status);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function ConfirmLibraryDelete(elem) {
    localStorage.setItem('deleteId', $(elem).attr('data-id'));
    $('#delete_library').modal();
}

function Library_Delete() {
    $.ajax({
        url: '../library_delete',
        data: {
            id: localStorage.getItem('deleteId')
        },
        type: 'POST',
        success: function(res) {
            var result = JSON.parse(res);
            if (result.status == 'OK') {
                $('#delete_library').modal('hide');
                window.location = '../library';
            } else {
                alert(result.status);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function ConfirmUserDelete(elem) {
    localStorage.setItem('deleteId', $(elem).attr('data-id'));
    $('#delete_user').modal();
}

function User_Delete() {
    $.ajax({
        url: '../user_delete',
        data: {
            id: localStorage.getItem('deleteId')
        },
        type: 'POST',
        success: function(res) {
            var result = JSON.parse(res);
            if (result.status == 'OK') {
                $('#delete_user').modal('hide');
                window.location = '../users';
            } else {
                alert(result.status);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function ConfirmBackupDelete(elem) {
    localStorage.setItem('deleteId', $(elem).attr('data-id'));
    $('#delete_backup').modal();
}

function Backup_Delete() {
    $.ajax({
        url: '../backup_delete',
        data: {
            id: localStorage.getItem('deleteId')
        },
        type: 'POST',
        success: function(res) {
            var result = JSON.parse(res);
            if (result.status == 'OK') {
                $('#delete_backup').modal('hide');
                window.location = '../backup';
            } else {
                alert(result.status);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function ConfirmTransmissionDelete(elem) {
    localStorage.setItem('deleteId', $(elem).attr('data-id'));
    $('#delete_transmission').modal();
}

function Transmission_Delete() {
    $.ajax({
        url: '../transmission_delete',
        data: {
            id: localStorage.getItem('deleteId')
        },
        type: 'POST',
        success: function(res) {
            var result = JSON.parse(res);
            if (result.status == 'OK') {
                $('#delete_transmission').modal('hide');
                window.location = '../transmission';
            } else {
                alert(result.status);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}
