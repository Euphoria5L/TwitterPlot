from flask import Flask, render_template, request, redirect
import tweet_plot_new as tweet_plot
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('main-template.html')

@app.route('/plot', methods=['GET','POST'])
def plot_data():
    if request.method =='POST':
        if request.form['graphselect'] == 'Bar Graph':
            f = tweet_plot.bar_plot(request.form['search'])
            title = request.form['title']

        if request.form['graphselect'] == 'Time-to-Tweets':
            if len(request.form['plottotal']) == 2:
                plot_total = True
            else:
                plot_total = False

            if request.form['interval'] == '':
                interval = 15
            elif int(request.form['interval']) > 60:
                print('error code goes here')
            else:
                interval = int(request.form['interval'])

            f = tweet_plot.time_lineplot(request.form['search'],
                interval, plot_total)
            title = request.form['title']

        if request.form['graphselect'] == 'Pie Chart':
            f = tweet_plot.pie_plot(request.form['search'])
            title = request.form['title']
    return render_template('plot.html', f=f, title=title)

@app.after_request
def add_header(response):
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()
