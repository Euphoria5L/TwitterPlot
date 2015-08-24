from flask import Flask, render_template, request, jsonify
import tweet_plot
import os

twitterplot = Flask(__name__)
# twitterplot.debug = True


@twitterplot.route('/')
def home():
    return render_template('main-template.html')


@twitterplot.route('/plot', methods=['POST', 'GET'])
def plot_data():
    """
    First we check if it's being POSTed. This is an artifact of older code,
    but I'm not removing it just in case it's some day useful for a different
    purpose. Otherwise, we grab the data from JQuery and pass it to the
    plotting function, which generates a new image for JQuery to reload.

    TODO: There is some duplicate code here. I need to clean it.
    """
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    filename = os.path.join(SITE_ROOT, 'testdata.json')
    plot_params = tweet_plot.Parameters()

    if request.method == 'POST':
        plot_params.plot_typehandle(request.args.get('plot_type'))
        plot_params.add_search_list(request.args.get('search_list'))

        if request.args.get('plottotal') == 'true':
            plot_params.plot_total = True
        else:
            plot_params.plot_total = False
        interval = request.args.get('interval')

        if interval == '':
            plot_params.interval = 15
        else:
            plot_params.interval = int(interval)

        plot_params.start_time = request.args.get('start_time')
        plot_params.end_time = request.args.get('end_time')
        plot_params.filename = filename

        tweet_plot.interface(plot_params)

        return jsonify({})

    plot_params.plot_typehandle(request.args.get('plot_type'))
    plot_params.add_search_list(request.args.get('search_list'))

    if request.args.get('plottotal') == 'true':
        plot_params.plot_total = True
    else:
        plot_params.plot_total = False
    interval = request.args.get('interval')

    if interval == '':
        plot_params.interval = 15
    else:
        plot_params.interval = int(interval)

    plot_params.start_time = request.args.get('start_time')
    plot_params.end_time = request.args.get('end_time')
    plot_params.filename = filename

    tweet_plot.interface(plot_params)

    return jsonify({})


@twitterplot.after_request
def add_header(response):
    """
    Old function for making sure new images loaded when /plot was POSTed to
    by sending an HTML header giving a max cache age. Since the
    current version uses JQuery to do things, this largely serves to make sure
    the HTML, JS, and CSS files load whenever changed. It should probably be
    removed on a prodution server.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    # DO NOT EVER RUN THIS AS A MAIN APP ON A SERVER. EVEN COMMENT OUT THE
    # DEBUG LINE JUST TO BE SAFE
    twitterplot.debug = True
    twitterplot.run()
