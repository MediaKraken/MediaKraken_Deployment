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

