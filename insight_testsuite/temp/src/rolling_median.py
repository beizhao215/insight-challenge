###### This is the solution to the 2016 Insight Data Engineer Challenge
###### Authur: Bei Zhao
###### Date: 7/8/2016

from igraph import *
import json
import time
from datetime import datetime as dt
from time import mktime
import datetime
import itertools
import sys

# truncate function referenced from stackoverflow answer to truncate the number
def truncate(f, n):
    # Truncates/pads a float f to n decimal places without rounding
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])


# add persons in a payment
def add_persons(persons, payment_time_dt):
    for person in persons:
        try:
            # if the person already exists in the graph (and not expired)
            update_person_vs = g.vs.find(name=person)

            # update vertex attribute if current payment time is later than current vertex's modified time
            person_current_modified_time = update_person_vs['modified_time']

            if person_current_modified_time < payment_time_dt:
                update_person_vs.update_attributes(modified_time=payment_time_dt)
        except:
            g.add_vertex(name = person, modified_time=payment_time_dt)

    if g.are_connected(persons[0], persons[1]):
        eid = g.get_eid(persons[0], persons[1])
        g.delete_edges(eid)
    g.add_edge(persons[0], persons[1], modified_time=payment_time_dt)


def persons_are_valid(persons):
    return len(persons) == 2 and persons[0].strip() and persons[1].strip() and persons[0] != persons[1]


def calculate_median(g):
    degree_list = g.degree()
    n = len(degree_list)
    if n % 2 == 1:
        med = float(quickselect(degree_list, n/2))
    else:
        med = float(quickselect(degree_list, n/2-1) + float(quickselect(degree_list, n/2)))/2
    med = truncate(med, 2)
    return med


# Select nth greatest number, referenced from online source
def quickselect(arr, n):
    pivot = arr[0]
    below = [x for x in arr if x < pivot]
    above = [x for x in arr if x > pivot]

    num_less = len(below)
    num_lessoreq = len(arr) - len(above)

    if n < num_less:
        return quickselect(below, n)
    elif n >= num_lessoreq:
        return quickselect(above, n-num_lessoreq)
    else:
        return pivot

if __name__ == "__main__":
    # initiate a graph
    g = Graph()
    start_time = time.time()

    # Keep track of the time of the latest payment. Initially set to some time before the era of venmo...
    latest_time = time.strptime("2001-01-1T01:00:00Z", "%Y-%m-%dT%H:%M:%SZ")

    # Transform time.strptime to datetime
    latest_time_dt = dt.fromtimestamp(mktime(latest_time))

    # Define path for input and output.txt files.
    in_filename = sys.argv[1]
    out_filename = sys.argv[2]

    # in_filename = '../venmo_input/venmo-trans.txt'
    # out_filename = '../venmo_output/output2.txt'
    file_out = open(out_filename, 'a')

    with open(in_filename) as data_file:
        for line in data_file:
            # reads the payment as json
            payment = json.loads(line)

            # filter out the lines that are invalid payment
            if 'actor' not in payment or 'target' not in payment:
                continue

            # get create_time of the payment
            payment_time = time.strptime(payment['created_time'], "%Y-%m-%dT%H:%M:%SZ")
            payment_time_dt = dt.fromtimestamp(mktime(payment_time))

            persons = [payment['actor'], payment['target']]


            # check time range
            # if older than 1 minute of latest payment, do nothing to the graph
            if payment_time_dt <= latest_time_dt - datetime.timedelta(minutes=1):
                pass

            # if fall into the 1 minute window, add the persons
            elif latest_time_dt >= payment_time_dt > latest_time_dt - datetime.timedelta(minutes=1):
                if persons_are_valid:
                    add_persons(persons, payment_time_dt)

            # if the payment is the newest
            else:
                latest_time_dt = payment_time_dt

                # get all vertices in the graph
                vs = VertexSeq(g)

                # prepare a list for expired vertices
                del_names = []
                # iterate through the vertices, delete the ones that's older than 1 minutes of this tweet
                for each_vertex in vs:
                    if each_vertex['modified_time'] <= latest_time_dt - datetime.timedelta(minutes=1):
                        del_names.append(each_vertex['name'])

                for v_name in del_names:
                    to_be_del_vs = g.vs.find(name=v_name)
                    g.delete_vertices(to_be_del_vs)

                es = EdgeSeq(g)
                for each_edge in es:
                    if each_edge['modified_time'] <= latest_time_dt - datetime.timedelta(minutes=1):
                        g.delete_edges(each_edge)

                if persons_are_valid:
                    add_persons(persons, payment_time_dt)

            num_vertices = float(g.vcount())

            # if graph is still empty
            if num_vertices == 0:
                file_out.write("0.00")
                file_out.write('\n')
            else:
                median = calculate_median(g)
                #file_out.write(str(sorted(g.degree())))

                file_out.write(str(median))
                file_out.write('\n')

file_out.close()

print("--- %s seconds ---" % (time.time() - start_time))   # 0.32 second

