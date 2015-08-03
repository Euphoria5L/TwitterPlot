import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy
import math
from datetime import datetime
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

def time_lineplot(search_list, interval=15):
    """
    Makes a line plot from a search_list. We have to do a lot of setup work to
    make it all happen, first.
    """
    time_dictionary = time_dict_gen(interval, search_list)
    time_dictionary = time_to_tweets(time_dictionary, 'testdata.json', interval,
        search_list)

    print(time_dictionary)
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
            x_axis.append(mdate.date2num(datetime.strptime(key, '%H:%M')))
        x=0
        for item in time_dictionary[key]:
            x += time_dictionary[key][item]
        y_axis.append(x)

    plt.plot_date(x_axis, y_axis, 'b-')
    plt.gcf().autofmt_xdate()

    plt.savefig('static/image.jpg')
    plt.close()
    return 'static/image.jpg'

#####
# processing functions
#####

def time_to_tweets(time_dictionary, filename, interval, search_list):
    """
    Takes a dictionary of times (this must be prepared prior using
    time_dict_gen), a filename for data (if there are multiple files it should
    be handled elsewhere; use the update function on the dictionary returned),
    a time interval to determine how to bucket the times (this must be the same
    variable passed to time_dict_gen), and a search list.

    The search list could be extracted from the time_dictionary if present,
    but if time_dict_gen is used to build the dictionary, it will already exist
    and be easily accessible.
    """
    fi = open(filename, 'r', encoding='utf_8')
    search_list = search_list.split()

    for line in nonblank_lines(fi):
        jdata = json.loads(line)
        for term in search_list:
            if term in jdata['text'].lower():

                # extracting the timestamp and putting it into a usable
                # format for the dictionary.
                # QUESTION: could I just use raw datetime objects? -- generation
                # would be a big pain, so while it'd be faster, this is adequate
                # for now.
                timestamp = datetime.strptime(jdata['created_at'], '%a %b %d \
                    %H:%M:%S %z %Y')
                timename = str(timestamp.hour).zfill(2) + ':' + \
                    str(math.floor(timestamp.minute/interval) * interval).zfill(2)

                # because this function is adequately general, this is just
                # a way for determining what KIND of dictionary is being fed
                # into the function, so the right thing gets incremented
                if type(time_dictionary[timename]) is int:
                    time_dictionary[timename] += 1
                else:
                    # print(time_dictionary)
                    time_dictionary[timename][term] += 1

    fi.close()
    return time_dictionary

def time_dict_gen(interval, search_list=None):
    """
    Build the dictionary for searching. Search list is optional; it makes a
    different sort of dictionary, where the values are dictionaries.
    time_to_tweets takes these time_dicts as arguments.

    This is easier to read than any dictionary comprehension you could use.
    """
    timedict=OrderedDict([])

    if search_list == None:
        for i in range(0, 24):
            for j in range (0, math.ceil(60/interval)):
                timedict[str(i).zfill(2) + ':' + str(j * interval).zfill(2)]=0

    else:
        # build the search_dict!
        search_list = search_list.split()
        search_dict={x: 0 for x in search_list}

        for i in range(0, 24):
            for j in range (0, math.ceil(60/interval)):
                timedict[str(i).zfill(2) + ':' + str(j *
                interval).zfill(2)] = dict(search_dict)

    return timedict

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
            x_axis.append(mdate.date2num(datetime.strptime(key, '%H:%M')))
            y_axis.append(l[key])
    x_axis = sorted(x_axis)


    plt.plot(x_axis, y_axis)
    plt.show()
