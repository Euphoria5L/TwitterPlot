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

        current_image_max = 1;
        localStorage.setItem('current_image_max', current_image_max);
        $('#previous-img').prop('disabled', true);

    } else {
        userid = localStorage.getItem('userid');
        current_image_max = localStorage.getItem('current_image_max');
        if (current_image_max <= 2) {
            $('#previous-img').prop('disabled', true);
        }
    }

    $('#graph').attr('src', image_url + userid +
        '/1.png').error(function() {
            $('#graph').removeAttr('src');
            $('#graph').attr('src', image_url + 'twitterplot.jpg');
        });

    var current_image = 1;
    $('#next-img').prop('disabled', true);
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
        if ($('#search').val().split(' ').length >= 5 &&
            ($('#graphselect').val() === 'time_lineplot' ||
            $('#graphselect').val() === 'time_truncate')) {
            alert('Must use fewer than six search terms!');
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
        data_file: $('#data_select').val(),
        userid: userid}).done(function(data) {
            setTimeout(function () {
                $('#graph').removeAttr('src');
                $('#graph').attr('src', data.image_url + '1.png' + '?timestamp=' + new Date().getTime());
                current_image = 1;
                if (current_image_max < 10) {
                    current_image_max++;
                    localStorage.setItem('current_image_max',
                        current_image_max);
                        $('#next-img').prop('disabled', true);
                        $('#previous-img').prop('disabled', false);
                }
            }, 100);
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

    /* The code below is a little strange. TwitterPlot saves the files with the
    most recent one as 1.png, and increments any other image files up by 1 until
    10.png, which is always overwritten; there are a max of 10 image files kept
    at a time per userid (basically, per browser). So this code counts
    backwards; previous-img increments the counter, and next-image decrements
    it.
    */

    $('#previous-img').click(function() {
        if (current_image === 10) {
            return;
        }
        else {
            current_image++;
            $.ajax({
                url: image_url + userid + '/' + current_image + '.png',
                type: "HEAD",
                error: function () {
                    current_image--;
                },
                success: function () {
                    $('#graph').attr('src', image_url + userid + '/' +  current_image + '.png');
                }
            });
            if (current_image === Number(current_image_max)) {
                $('#previous-img').prop('disabled', true);
            }
            $('#next-img').prop('disabled', false);
        }
    });

    $('#next-img').click(function() {
        if (current_image === 1) {
            return;
        }
        else {
            current_image--;
            $('#graph').attr('src', image_url + userid + '/'+  current_image + '.png');
            $('#previous-img').prop('disabled', false);
            if (current_image === 1) {
                $('#next-img').prop('disabled', true);

            }
        }
    });

});
