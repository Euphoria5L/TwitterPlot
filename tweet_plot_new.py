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

def bar_plot(dictionary):
    """
    Plot the data from a dictionary as a bar chart.
    """
    l = dictionary.split()
    l = {term: 0 for term in l}
    labels = list(l.keys())
    terms = tweetsearch(l, 'testdata.json')
    counts = list(l.values())

    y_axis = numpy.arange(len(l.keys()))

    plt.barh(y_axis, counts, align='center', alpha=0.4)
    plt.yticks(y_axis, labels)
    plt.xlabel('Tweet Counts')

    plt.savefig('static/image.jpg')
    plt.close()
    return 'static/image.jpg'

def pie_plot(search_list):
    plt.style.use('fivethirtyeight')

    l = search_list.split()
    l = {term: 0 for term in l}
    labels = list(l.keys())
    terms = tweetsearch(l, 'testdata.json')
    counts = list(l.values())
    plt.pie(counts, labels=labels, autopct='%1.1f%%')

    plt.axis('equal')
    plt.savefig('static/image.jpg')
    plt.close()
    return 'static/image.jpg'

def time_lineplot(search_list, interval=15, plot_total=True):
    """
    Makes a line plot from a search_list. We have to do a lot of setup work to
    make it all happen, first.
    """
    plt.style.use('fivethirtyeight')

    time_dictionary = time_to_tweets('testdata.json', search_list, interval)
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
        search_list = search_list.split()

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
    search_list = search_list.split()
    search_dict={x: 0 for x in search_list}

    interval_time = mdate.minutes(interval)

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
                    time_dictionary[timename] = dict(search_dict)
                    time_dictionary[timename][term] += 1
                    curr_time = timename
                if timename < curr_time + interval_time:
                    time_dictionary[curr_time][term] += 1
                if timename > curr_time + interval_time:
                    curr_time = timename
                    time_dictionary[curr_time] = dict(search_dict)
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

    l = OrderedDict(time_to_tweets(timedict, 'testdata.json', interval, test_list))

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
