function ConfirmCronRun(elem) {
    localStorage.setItem('runId', $(elem).attr('data-id'));
    $('#run_cron').modal();
}

function Cron_Run() {
    $.ajax({
        url: '../cron_run',
        data: {
            id: localStorage.getItem('runId')
        },
        type: 'POST',
        success: function(res) {
            var result = JSON.parse(res);
            if (result.status == 'OK') {
                $('#run_cron').modal('hide');
                window.location = '../cron';
            } else {
                alert(result.status);
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}
