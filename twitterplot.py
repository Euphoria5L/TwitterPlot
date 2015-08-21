from flask import Flask, render_template, request
import tweet_plot
import os
# from werkzeug import secure_filename

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['txt', 'json'])

twitterplot = Flask(__name__)
# twitterplot.debug = True


@twitterplot.route('/')
def home():
    return render_template('index-template.html')


@twitterplot.route('/plot', methods=['POST', 'GET'])
def plot_data():
    """
    First we check if it's being POSTed. This is an artifact of older code,
    but I'm not removing it just in case it's some day useful for a different
    purpose. Otherwise, we grab the data from JQuery and pass it to the
    plotting function, which generates a new image for JQuery to reload.
    """
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    filename = os.path.join(SITE_ROOT, 'testdata.json')
    # filename = '/var/www/twitterplot/testdata.json'
    plot_params = tweet_plot.Parameters()

    if request.method == 'POST':
        plot_params.plot_typehandle(request.form['graphselect'])
        plot_params.search_list = request.form['search']
        if request.form['plottotal'] == 'yestotal':
            plot_params.plot_total = True
        else:
            plot_params.plot_total = False
        interval = request.form['interval']

        if interval == '':
            plot_params.interval = 15
        else:
            plot_params.interval = int(interval)

        plot_params.start_time = request.form['start_time']
        plot_params.end_time = request.form['end_time']
        plot_params.filename = filename

        f = tweet_plot.interface(plot_params)
        title = 'title'

        return render_template('plot.html', f=f, title=title)

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

    f = tweet_plot.interface(plot_params)
    title = 'title'

    return render_template('plot.html', f=f, title=title)


@twitterplot.after_request
def add_header(response):
    """
    Old function for making sure new images loaded when /plot was POSTed to
    after request by sending an HTML header giving a max cache age. Since the
    current version uses AJAX to do things, this largely serves to make sure
    the HTML, JS, and CSS files load whenever changed. It should be removed
    on a prodution server.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    # TURN THIS OFF ON A PRODUCTION SERVER! FLASK DEBUG LETS YOU RUN ARBITRARY
    # CODE IT IS ASKING FOR DISASTER IF YOU DON'T. THIS IS VERY IMPORTANT!
    twitterplot.debug = True
    twitterplot.run()
