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
    $('#interval_div').hide();
    $('#total_div').hide();
    $('#start_div').hide();
    $('#end_div').hide();

    $('#graphselect').change(hideoptions);

    $('#submit').click(function() {

        // TODO: rewrite this to use real form validation via jquery.validate
        // ALSO! write a basic validator for start_time and end_time
        if ($('#interval').is('visible')) {
            if (Number($('#interval').val()) < 1 ||
                Number($('#interval').val()) > 60) {
                    alert('Must be interval between 1 minute and 60 minutes!');
                    return;
            }
        }
        if ($('#search').val().length === 0) {
            alert('Must include at least one search term!');
            return;
        }

        $.getJSON('/plot',
        {plot_type: $('#graphselect').val(),
        search_list: $('#search').val(),
        plottotal: $('#plottotal').is('checked'),
        interval: $('#interval').val(),
        start_time: $('#start_time').val(),
        end_time: $('#end_time').val()});
        $('#graph').removeAttr('src');
        $('#graph').attr('src', '/static/image.png?timestamp=' + new Date().getTime());
    });

    $('#help-dialog').dialog({
        resizable: false,
        autoOpen: false,
        modal: true,
        title: "HELP",
        height: 500,
        width: 800,
    });

    $('#help').click(function() {
        $('#help-dialog').dialog('open');
    });
});
