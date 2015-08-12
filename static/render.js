$(document).ready(function() {
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
