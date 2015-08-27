function hideoptions() {
    // This could be simplified
    var plot_option = $('#graphselect').val();
    if (plot_option === 'bar_plot') {
        $('#interval_div').hide();
        $('#total_div').hide();
        $('#start_div').hide();
        $('#end_div').hide();
    }
    else if (plot_option === 'pie_plot') {
        $('#interval_div').hide();
        $('#total_div').hide();
        $('#start_div').hide();
        $('#end_div').hide();
    }
    else if (plot_option === 'time_lineplot')
    {
        $('#interval_div').show();
        $('#total_div').show();
        $('#start_div').hide();
        $('#end_div').hide();
    }
    else if (plot_option === 'time_truncate') {
        $('#interval_div').show();
        $('#total_div').show();
        $('#start_div').show();
        $('#end_div').show();
    }
}

$(document).ready(function() {
    // creating a userid
    if (localStorage.getItem('userid') === null) {
        timestamp = new Date().getTime();
        localStorage.setItem('userid', timestamp);
        userid = localStorage.getItem('userid');
    } else {
        userid = localStorage.getItem('userid');
    }

    $.get('static/' + userid + '/1.png').fail(function() {
            $('#graph').removeAttr('src');
            $('#graph').setAttr('static/' + userid + '/1.png');
        });

    $('#interval_div').hide();
    $('#total_div').hide();
    $('#start_div').hide();
    $('#end_div').hide();

    $('#graphselect').change(hideoptions);

    $('#submit').click(function() {

        // form validation code; throw an alert when it's bad.
        if ($('#interval').is(':visible')) {
            // Just in case a browser doesn't support input type="number"
            if (!/^\d{1,2}$/.test($('#interval').val())) {
                alert('Must be interval between 1 minute and 60 minutes!');
                return;
            }
        }

        if (Number($('#interval').val()) < 1 ||
            Number($('#interval').val()) > 60) {
                alert('Must be interval between 1 minute and 60 minutes!');
                return;
        }

        if ($('#search').val().length === 0) {
            alert('Must include at least one search term!');
            return;
        }

        if ($('#start_time').is(':visible')) {
            if (/^\d{2}[:]\d{2}$/.test($('#start_time').val()) === false) {
                alert('Times must be in format "NN:NN"');
                return;
            }
        }

        if ($('#end_time').is(':visible')) {
            if (/^\d{2}[:]\d{2}$/.test($('#end_time').val()) === false) {
                alert('Times must be in format "NN:NN"');
                return;
            }
        }

        $.getJSON('/plot',
        {plot_type: $('#graphselect').val(),
        search_list: $('#search').val(),
        plottotal: $('#plottotal').is(':checked'),
        interval: $('#interval').val(),
        start_time: $('#start_time').val(),
        end_time: $('#end_time').val(),
        userid: userid}).done(function(data) {
            setTimeout(function () {
                $('#graph').removeAttr('src');
                $('#graph').attr('src', data.image_url + '?timestamp=' + new Date().getTime());
            }, 3000);
        });
    });
    $('#help-dialog').dialog({
        resizable: false,
        autoOpen: false,
        modal: true,
        title: "HELP",
        height: 550,
        width: 800,
        closeText: 'X'
    });

    $('#help').click(function() {
        $('#help-dialog').dialog('open');
    });

});
