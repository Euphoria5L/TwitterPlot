function hideoptions() {
    var plot_option = $('#graphselect').val();
    if (plot_option === 'Bar Graph') {
        $('#interval_div').hide();
        $('#total_div').hide();
        $('#start_div').hide();
        $('#end_div').hide();
    }
    else if (plot_option === 'Pie Chart') {
        $('#interval_div').hide();
        $('#total_div').hide();
        $('#start_div').hide();
        $('#end_div').hide();
    }
    else if (plot_option === 'Time-to-Tweets')
    {
        $('#interval_div').show();
        $('#total_div').show();
        $('#start_div').hide();
        $('#end_div').hide();
    }
    else if (plot_option === 'Interval Time') {
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
    
    $('#graphselect').change(function() { hideoptions();});

    $('#submit').click(function() {
    $.getJSON('/plot',
    {plot_type: $('#graphselect').val(),
    search_list: $('#search').val(),
    plottotal: $('#plottotal').is('checked'),
    interval: $('#interval').val(),
    start_time: $('#start_time').val(),
    end_time: $('#end_time').val()});
    $('#graph').removeAttr('src');
    $('#graph').attr('src', '/static/image.jpg?timestamp=' + new Date());
});
});
