# TODO
# 1. Clean up interface
# 2. Add file selector

from flask import Flask, render_template, request, redirect, jsonify
import tweet_plot_new as tweet_plot
import os
from werkzeug import secure_filename

UPLOAD_FOLDER = '/'
ALLOWED_EXTENSIONS = set(['txt', 'json'])

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index-template.html')

@app.route('/plot')
def plot_data():
    # if request.method =='POST':
    #     plot_type = request.form['graphselect']
    #     search_list = request.form['search']
    #     filename = 'testdata.json'
    #     if request.form['plottotal'] == 'yestotal':
    #         plot_total = True
    #     else:
    #         plot_total = False
    #     interval = request.form['interval']
    #
    #     print(request.form['plottotal'])
    #     if interval == '':
    #         interval = 15
    #     else:
    #         interval = int(interval)
    #
    #     start_time = request.form['start_time']
    #     end_time = request.form['end_time']
    #
    #     f = tweet_plot.interface(plot_type, search_list, filename, plot_total,
    #             interval, start_time, end_time)
    #     title = 'title'
    plot_type = request.args.get('plot_type')
    search_list = request.args.get('search_list')
    filename = 'testdata.json'
    print(request.args.get('plottotal'))
    if request.args.get('plottotal') == 'true':
        plot_total = True
    else:
        plot_total = False
    interval = request.args.get('interval');

    if interval == '':
        interval = 15
    else:
        interval = int(interval)

    start_time = request.args.get('start_time')
    end_time = request.args.get('end_time')

    f = tweet_plot.interface(plot_type, search_list, filename, plot_total,
            interval, start_time, end_time)
    title = 'title'

    return render_template('plot.html', f=f, title=title)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
