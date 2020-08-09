function EditLibrary(elm) {
	localStorage.setItem('editLibraryId',$(elm).attr('data-id'));
	$.ajax({
		url : '../getLibraryById',
		data : {id:$(elm).attr('data-id')},
		type : 'POST',
		success: function(res){
			var data = JSON.parse(res);
			$('#editPath').val(data['Path']);
			$('#editClass').val(data['Media Class']);
			$('#editLibraryModal').modal();
		},
		error: function(error){
			console.log(error);
		}
	});
}

$(function() {
	$('#btnLibraryUpdate').click(function() {
	    $.ajax({
		url: '../updateLibrary',
		data: {
		    new_path: $('#editPath').val(),
		    new_class: $('#editClass').val(),
		    id: localStorage.getItem('editLibraryId')
		},
		type: 'POST',
		success: function(res) {
		    $('#editLibraryModal').modal('hide');
		    // Re populate the grid
		},
		error: function(error) {
		    console.log(error);
		}
	    });
	});
});

function EditShare(elm) {
	localStorage.setItem('editShareId',$(elm).attr('data-id'));
	$.ajax({
		url : '../getShareById',
		data : {id:$(elm).attr('data-id')},
		type : 'POST',
		success: function(res){
			var data = JSON.parse(res);
			$('#editShareType').val(data['Type']);
			$('#editShareUser').val(data['User']);
			$('#editSharePassword').val(data['Password']);
			$('#editShareServer').val(data['Server']);
			$('#editSharePath').val(data['Path']);
			$('#editShareModal').modal();
		},
		error: function(error){
			console.log(error);
		}
	});
}

$(function() {
	$('#btnShareUpdate').click(function() {
	    $.ajax({
		url: '../updateShare',
		data: {
		    new_share_type: $('#editShareType').val(),
		    new_share_user: $('#editShareUser').val(),
		    new_share_password: $('#editSharePassword').val(),
		    new_share_server: $('#editShareServer').val(),
		    new_share_path: $('#editSharePath').val(),
		    id: localStorage.getItem('editShareId')
		},
		type: 'POST',
		success: function(res) {
		    $('#editShareModal').modal('hide');
		    // Re populate the grid
		},
		error: function(error) {
		    console.log(error);
		}
	    });
	});
});

function EditTransmission(elm) {
	localStorage.setItem('editId',$(elm).attr('data-id'));
	$.ajax({
		url : '../transmission_edit',
		data : {id:$(elm).attr('data-id')},
		type : 'POST',
		success: function(res){
			var data = JSON.parse(res);
			$('#editTitle').val(data['Title']);
			$('#editDescription').val(data['Description']);
			$('#editTransmissionModal').modal();
		},
		error: function(error){
			console.log(error);
		}
	});
}

function EditChromecast(elm) {
	localStorage.setItem('editChromecastId',$(elm).attr('data-id'));
	$.ajax({
		url : '../getChromecastById',
		data : {id:$(elm).attr('data-id')},
		type : 'POST',
		success: function(res){
			var data = JSON.parse(res);
			$('#editName').val(data['Name']);
			$('#editIP').val(data['IP']);
			$('#editChromecastModal').modal();
		},
		error: function(error){
			console.log(error);
		}
	});
}

$(function() {
	$('#btnChromecastUpdate').click(function() {
	    $.ajax({
		url: '../updateChromecast',
		data: {
		    new_name: $('#editName').val(),
		    new_ip: $('#editIP').val(),
		    id: localStorage.getItem('editChromecastId')
		},
		type: 'POST',
		success: function(res) {
		    $('#editChromecastModal').modal('hide');
		    // Re populate the grid
		},
		error: function(error) {
		    console.log(error);
		}
	    });
	});
});
