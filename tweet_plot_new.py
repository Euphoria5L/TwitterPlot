# TODO
# 1. Allow easy saving.
# 2. Better color options.
# 3. Flexible time rendering.
# 4. Multiple file support.

import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy
import math
import datetime
import json
from collections import OrderedDict

#####
# plotting functions
#####

filename = 'testdata.json'

def interface(plot_type, search_list, filename, plot_total=False, interval=15,
        start_time=0, end_time=0):
    """
    To simplify things, this is an interface function. It prepares the
    data for processing and picks the correct plot, returning the image file
    path for Flask to render. Don't mess with the order of options, it will
    break EVERYTHING.
    """

    # prep the dictionaries.
    search_list = search_list.split()
    sl = search_list # because time_lineplot requires a list of search terms
    search_list = {term: 0 for term in search_list}

    if plot_type == 'Bar Graph':
        dictionary = tweetsearch(search_list, filename)
        return bar_plot(dictionary)

    elif plot_type == 'Time-to-Tweets':
        dictionary = time_to_tweets(filename, search_list, interval)
        return time_lineplot(sl, dictionary, interval,
                plot_total)

    elif plot_type == 'Pie Chart':
        dictionary = tweetsearch(search_list, filename)
        return pie_plot(search_list)

    else:
        print('lol')

def bar_plot(dictionary):
    """
    Plot the data from a dictionary as a bar chart.
    """
    labels = list(dictionary.keys())
    counts = list(dictionary.values())

    y_axis = numpy.arange(len(dictionary.keys()))

    plt.barh(y_axis, counts, align='center', alpha=0.4)
    plt.yticks(y_axis, labels)
    plt.xlabel('Tweet Counts')

    plt.savefig('static/image.jpg')
    plt.close()
    return 'static/image.jpg'

def pie_plot(search_list):
    plt.style.use('fivethirtyeight')


    labels = list(search_list.keys())
    counts = list(search_list.values())
    plt.pie(counts, labels=labels, autopct='%1.1f%%')

    plt.axis('equal')
    plt.savefig('static/image.jpg')
    plt.close()
    return 'static/image.jpg'

def time_lineplot(search_list, time_dictionary, interval=15,
        plot_total=True):
    """
    Makes a line plot from a search_list. We have to do a lot of setup work to
    make it all happen, first.
    """
    plt.style.use('fivethirtyeight')

    if plot_total == True:
        x_axis = []
        y_axis = []
        for key in time_dictionary:
            is_empty = False
            for count in time_dictionary[key]:
                if time_dictionary[key][count] == 0:
                    is_empty = True
                else:
                    is_empty = False
            if is_empty == True:
                continue
            else:
                x_axis.append(key)
            x=0
            for item in time_dictionary[key]:
                x += time_dictionary[key][item]
            y_axis.append(x)

        plt.plot_date(x_axis, y_axis, 'b-')

        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%I:%M %p'))
        plt.gcf().autofmt_xdate()

        plt.savefig('static/image.jpg')
        plt.close()

        return 'static/image.jpg'

    elif plot_total == False:


        # Here's the list of colors for the lines if we aren't plotting the
        # totals. IT NEEDS TO BE LONGER.
        colors = ['b-', 'g-', 'r-', 'y-']

        for term in search_list:
            x_axis = []
            y_axis = []
            for key in time_dictionary:
                x_axis.append(key)
                y_axis.append(time_dictionary[key][term])
            plt.plot_date(x_axis, y_axis, colors[search_list.index(term)])

        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%I:%M %p'))
        plt.gcf().autofmt_xdate()
        plt.legend(search_list, loc='upper center', bbox_to_anchor=(0.5, -0.15),
            ncol=5, fancybox=True, shadow=True)

        plt.savefig('static/image.jpg')
        plt.close()

        return 'static/image.jpg'

#####
# processing functions
#####

def time_to_tweets(filename, search_list, interval=15):
    """
    Takes a filename for data (if there are multiple files it should
    be handled elsewhere; use the update function on the dictionary returned),
    a time interval to determine how to bucket the times and a search list.
    """
    fi = open(filename, 'r', encoding='utf_8')

    time_dictionary = OrderedDict({})

    interval_time = mdate.minutes(int(interval))

    curr_time = 0
    for line in nonblank_lines(fi):
        jdata = json.loads(line)
        for term in search_list:
            if term in jdata['text'].lower():

                timestamp = datetime.datetime.strptime(jdata['created_at'], '%a %b %d \
                    %H:%M:%S %z %Y')
                timename = mdate.date2num(timestamp)

                # because this function is adequately general, this is just
                # a way for determining what KIND of dictionary is being fed
                # into the function, so the right thing gets incremented

                if time_dictionary == {}:
                    time_dictionary[timename] = dict(search_list)
                    time_dictionary[timename][term] += 1
                    curr_time = timename
                if timename < curr_time + interval_time:
                    time_dictionary[curr_time][term] += 1
                if timename > curr_time + interval_time:
                    curr_time = timename
                    time_dictionary[curr_time] = dict(search_list)
                    time_dictionary[curr_time][term] += 1

    fi.close()
    return time_dictionary

def tweetsearch(term_dictionary, filename):
    fi = open(filename, 'r', encoding='utf_8')
    for line in nonblank_lines(fi):
        jdata = json.loads(line)
        for term, count in term_dictionary.items():
            if term in jdata['text'].lower():
                term_dictionary[term] += 1
    fi.close()
    return term_dictionary

def nonblank_lines(fi):
    for l in fi:
        line = l.rstrip()
        if line:
            yield line

if __name__ == '__main__':
    interval=15
    timedict={}
    for i in range(0, 24):
        for j in range (0, math.ceil(60/interval)):
            timedict[str(i).zfill(2) + ':' + str(j * interval).zfill(2)]=0
    test_list = ['trump', 'obama', 'cruz']

    l = OrderedDict(time_to_tweets(timedict, filename, interval, test_list))

    x_axis = []
    y_axis = []
    print(l)
    for key in l:
        if l[key] == 0:
            continue
        else:
            x_axis.append(mdate.date2num(datetime.datetime.strptime(key, '%H:%M')))
            y_axis.append(l[key])
    x_axis = sorted(x_axis)


    plt.plot(x_axis, y_axis)
    plt.show()
