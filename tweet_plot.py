import matplotlib
matplotlib.use('Agg')  # Needed to run properly on Ubuntu on AWS
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy
import math
import datetime
import json
import os
from collections import OrderedDict

#####
# plotting functions
#####

# IMPORTANT! The style settings are not available on Ubuntu on EC2!

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
image_dest = os.path.join(SITE_ROOT, 'static', 'image.png')


def interface(plot_type, search_list, filename, plot_total, interval=15,
              start_time=0, end_time=0):
    """
    To simplify things, this is an interface function. It prepares the
    data for processing and picks the correct plot, returning the image file
    path for Flask to render.
    """

    # prep the dictionaries.
    search_list = search_list.split()
    sl = search_list  # because time_lineplot requires a list of search terms
    search_list = {term: 0 for term in search_list}
    print(plot_total)
    # we don't need an else since things can't really go off the rails here.
    if plot_type == 'bar_plot':
        dictionary = tweetsearch(search_list, filename)
        return bar_plot(dictionary)

    elif plot_type == 'time_lineplot':
        dictionary = time_to_tweets(filename, search_list, interval)
        return time_lineplot(sl, dictionary, interval, plot_total)

    elif plot_type == 'pie_plot':
        dictionary = tweetsearch(search_list, filename)
        return pie_plot(search_list)

    elif plot_type == 'time_truncate':
        dictionary = time_to_tweets(filename, search_list, interval)
        dictionary = time_truncate(dictionary, start_time, end_time)
        return time_lineplot(sl, dictionary, interval, plot_total)


def bar_plot(dictionary):
    """
    Plot the data from a dictionary as a bar chart.
    """
    # plt.style.use('fivethirtyeight')

    labels = list(dictionary.keys())
    counts = list(dictionary.values())

    y_axis = numpy.arange(len(dictionary.keys()))

    plt.barh(y_axis, counts, align='center', alpha=0.4)
    plt.yticks(y_axis, labels)
    plt.xlabel('Tweet Counts')

    plt.savefig(image_dest, bbox_inches='tight', dpi=100)
    plt.close()
    return 'static/image.png'


def pie_plot(search_list):
    """
    Self-explanatory. Makes a pie chart.
    """
    # plt.style.use('fivethirtyeight')

    labels = list(search_list.keys())
    counts = list(search_list.values())
    plt.pie(counts, labels=labels, autopct='%1.1f%%')

    plt.axis('equal')
    plt.savefig(image_dest)
    plt.close()
    return 'static/image.png'


def time_lineplot(search_list, time_dictionary, interval=15,
                  plot_total=True):
    """
    Makes a line plot from a search_list. We pass the search_list in since
    it's easy to do; we could retrieve the list from the time_dictionary,
    or restructure things so that none of this is necessary, but this is a
    cheap solution that keeps the plotting code away from the parsing code.
    """
    # plt.style.use('fivethirtyeight')

    if plot_total is True:
        x_axis = []
        y_axis = []
        for key in time_dictionary:
            is_empty = False
            for count in time_dictionary[key]:
                if time_dictionary[key][count] == 0:
                    is_empty = True
                else:
                    is_empty = False
            if is_empty is True:
                continue
            else:
                x_axis.append(key)
            x = 0
            for item in time_dictionary[key]:
                x += time_dictionary[key][item]
            y_axis.append(x)

        plt.plot_date(x_axis, y_axis, 'b-')

        ax = plt.gca()
        ax.xaxis.set_major_formatter(mdate.DateFormatter('%I:%M %p'))
        plt.gcf().autofmt_xdate()

        plt.savefig(image_dest)
        plt.close()

        return 'static/image.png'

    elif plot_total is False:

        # Here's the list of colors for the lines if we aren't plotting the
        # totals. IT NEEDS TO BE LONGER.
        colors = ['b-', 'g-', 'r-', 'y-', 'm-']

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
        plt.legend(search_list, loc='upper center',
                   bbox_to_anchor=(0.5, -0.15),
                   ncol=5, fancybox=True, shadow=True)

        plt.savefig(image_dest)
        plt.close()

        return 'static/image.png'

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

    # this is set to zero because of the way initialization works later
    curr_time = 0
    for line in nonblank_lines(fi):
        jdata = json.loads(line)
        for term in search_list:
            if term in jdata['text'].lower():

                timestamp = datetime.datetime.strptime(jdata['created_at'], '%a %b %d \
                    %H:%M:%S %z %Y')
                timename = mdate.date2num(timestamp)

                # initializes the dictionary. This is true only once, but we do
                # it here, rather than earlier, since it lets us initialize it
                # for the first timename (which we won't know until we've
                # started searching the JSON file).
                if time_dictionary == {}:
                    time_dictionary[timename] = dict(search_list)
                    time_dictionary[timename][term] += 1
                    curr_time = timename

                # the conditional below should NOT be an elif!
                if timename < curr_time + interval_time:
                    time_dictionary[curr_time][term] += 1
                elif timename > curr_time + interval_time:
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


def time_truncate(dictionary, start_time, end_time):
    """ take a dictionary and reduce it to the desired interval.
    We do this rather than integrate it into time_to_tweets to keep
    time_to_tweets from becoming more complicated; this doesn't add
    any extra time, and requires only slightly more memory. It could be
    abstracted even more and called in time_to_tweets, but this lets us keep
    the logic separate and easier to debug.
    """

    # We need to preprocess times into our desired mdates format.

    zero_time = list(dictionary.keys())[0]
    start_time = start_time.split(':')
    start_time = mdate.hours(float(start_time[0])) + \
        mdate.minutes(float(start_time[1]))
    start_time = start_time + zero_time

    end_time = end_time.split(':')
    end_time = mdate.hours(float(end_time[0])) + \
        mdate.minutes(float(end_time[1]))
    end_time = zero_time + end_time

    # we need a new dictionary. It costs a bit of memory.
    new_dict = OrderedDict({})

    for time in dictionary:
        if time < start_time:
            continue
        elif time > start_time and time < end_time:
            new_dict[time] = dictionary[time]
        elif time > end_time:
            break
        else:
            break

    return new_dict


def nonblank_lines(fi):
    """
    lets us ignore all blank lines since the Twitter data comes in with line
    breaks between each tweet JSON.
    """
    for l in fi:
        line = l.rstrip()
        if line:
            yield line

if __name__ == '__main__':
    """
    This is some old testing code. It's old and obsolete, built before the
    web interface (or even the interface function) was. Here be dragons!

    TODO: build some command line options so tweet_plot can be called from the
    command line
    """
    interval = 15
    timedict = {}
    for i in range(0, 24):
        for j in range(0, math.ceil(60 / interval)):
            timedict[str(i).zfill(2) + ':' + str(j * interval).zfill(2)] = 0
    test_list = ['trump', 'obama', 'cruz']

    l = OrderedDict(time_to_tweets(timedict, 'testdata.json', interval,
                    test_list))

    x_axis = []
    y_axis = []
    print(l)
    for key in l:
        if l[key] == 0:
            continue
        else:
            x_axis.append(mdate.date2num(datetime.datetime.strptime(key,
                          '%H:%M')))
            y_axis.append(l[key])
    x_axis = sorted(x_axis)

    plt.plot(x_axis, y_axis)
    plt.show()
