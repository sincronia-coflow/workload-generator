import sys
import numpy as np
import os

# from sample import *
import scipy.stats
import matplotlib.pyplot as plt
import pickle


NUM_COFLOWS = int(sys.argv[1]);
ALPHA = (sys.argv[2]); #alpha value for code
NUM_INP_PORTS = 150;
LOAD_FACTOR = float(sys.argv[3]);
ACCESS_LINK_BANDWIDTH = (1024*2)/8; #1024*2 MBPS = 2GBPS, 2/8GBPS = 2 Gbps

if(ALPHA=='FB-UP'):
    FILE = str(NUM_COFLOWS)+'-'+str(LOAD_FACTOR)+'-'+'FB-UP'
else:
    ALPHA = int(ALPHA)
    INTRA_COFLOW_CONTENTION = float(sys.argv[4]); #c discussed in the code, belongs to [0,1], the traffic is one to ir for c = 0 and all to all for c = 1
    SOURCE_NUM_DIST = sys.argv[5]#'U' for uniform, 'Z' for zipf, 'FB' for trace
    DESTINATION_DATA_DIST = sys.argv[6] #'U' for uniform, 'Z' for zipf
    FILE = str(NUM_COFLOWS)+'-'+str(LOAD_FACTOR)+'-'+str(ALPHA)+'-'+str(INTRA_COFLOW_CONTENTION*100)+'-'+str(SOURCE_NUM_DIST)+'-'+str(DESTINATION_DATA_DIST)
if not os.path.exists('pickles'):
    os.mkdir('pickles');
if not os.path.exists('traces'):
    os.mkdir('traces');
PICKLE_FILE = 'pickles/' + FILE + '.pkl'
OUTPUT_FILE = 'traces/' + FILE  + '.txt'

fb_trace = 'coflow-benchmark-trace.txt';



irs = [];
#generate irs from tracefile
with open(fb_trace) as f1:
    for line in f1:
        numbers_str = line.split();
        num_senders = int(numbers_str[2]);
        num_receivers = int(numbers_str[3+num_senders]);
        irs.append(float(num_receivers)/float(num_senders));


#create distribution for ir
data_irs = irs;
hist_ir = np.histogram(data_irs,bins='auto');
hist_dist_ir = scipy.stats.rv_histogram(hist_ir);

#generate destination_datas from tracefile
destination_datas = [];
with open(fb_trace) as f1:
    for line in f1:
        numbers_str = line.split();
        num_senders = int(numbers_str[2]);
        num_receivers = int(numbers_str[3+num_senders]);
        for i in range(num_receivers):
            destination_datas.append(float(numbers_str[4+num_senders+i].split(':')[1]));
#generate distribution
data_dd = destination_datas;
hist_dd = np.histogram(data_dd,bins='auto');
hist_dist_dd = scipy.stats.rv_histogram(hist_dd);

#generate num_sources distribution from tracefile
num_sources_trace = [];
with open(fb_trace) as f1:
    for line in f1:
        numbers_str = line.split();
        num_senders = int(numbers_str[2]);
        num_sources_trace.append(num_senders);
#generate distribution
data_num_sources = num_sources_trace;
hist_num_sources = np.histogram(data_num_sources,bins='auto');
hist_dist_num_sources = scipy.stats.rv_histogram(hist_num_sources);

#create list of dictionary for FB upscale
coflow_trace = [];
with open(fb_trace) as f1:
    for line in f1:
        numbers_str = line.split();
        coflow_id = int(numbers_str[0]);
        num_senders = int(numbers_str[2]);
        num_receivers = int(numbers_str[3+num_senders]);
        destination_datas = [];
        for i in range(num_receivers):
            destination_datas.append(int(float(numbers_str[4+num_senders+i].split(':')[1])));
        coflow = {};
        coflow['id'] = coflow_id;
        coflow['num_senders'] = num_senders;
        coflow['num_destinations'] = num_receivers;
        coflow['destination_datas'] = destination_datas;
        coflow_trace.append(coflow);


total_flow_size = 0;
num_flows = 0;
flows = [];
num_sources_list = [];
num_destinations_list = [];
for i in range(NUM_COFLOWS):
    # num_sources = min(np.random.zipf(2),MAX_NUM_SOURCES);
    if(ALPHA=='FB-UP'):
        coflow_id = np.random.choice(526);
        coflow = coflow_trace[coflow_id]; #coflow_trace is a list of dictionary created by the coflow trace
        num_sources = coflow['num_senders'];
        num_destinations = coflow['num_destinations'];
        num_destinations_actual = num_destinations;
        sources = np.random.choice(np.arange(0,NUM_INP_PORTS),num_sources,replace=False);
        sources.sort();
        destinations = np.random.choice(np.arange(0,NUM_INP_PORTS),num_destinations,replace=False);
        destinations.sort();
        destination_datas = coflow['destination_datas'];
        # if(i==0):
        #     print(coflow['id']);
        #     print(num_sources);
        #     print(num_destinations);
        #     print(len(destination_datas));
        for j in range(num_destinations):
            for k in range(num_sources):
                flow_size = destination_datas[j]/num_sources;
                num_flows = num_flows + 1;
                total_flow_size = total_flow_size + flow_size;
                F = {'Coflow_ID': i, 'Source_ID': sources[k], 'Destination_ID': destinations[j], 'Size': flow_size};
                flows.append(F);
    else:
        if(SOURCE_NUM_DIST=='U'):
            MAX_NUM_SOURCES = min(ALPHA,NUM_INP_PORTS);
            # num_sources = min(int(round(np.random.uniform(1,MAX_NUM_SOURCES))),MAX_NUM_SOURCES);
            num_sources = np.random.choice(np.arange(1,MAX_NUM_SOURCES+1));
        elif(SOURCE_NUM_DIST=='Z'):
            MAX_NUM_SOURCES = min(ALPHA,NUM_INP_PORTS);
            num_sources = min(max(1,int(np.random.zipf(2))),MAX_NUM_SOURCES);
        elif(SOURCE_NUM_DIST=='FB'):
            MAX_NUM_SOURCES = 150;
            num_sources = min(MAX_NUM_SOURCES,max(1,int(hist_dist_num_sources.rvs(size=1))));

        sources = np.random.choice(np.arange(0,NUM_INP_PORTS),num_sources,replace=False);
        sources.sort();
        ir = hist_dist_ir.rvs(size=1);
        num_destinations = min(max(int(num_sources*ir),1),NUM_INP_PORTS);
        destinations_set = np.random.choice(np.arange(0,NUM_INP_PORTS),num_destinations,replace=False);
        destinations_set.sort();

        destination_source_dict = {};
        for j in range(NUM_INP_PORTS):
            destination_source_dict[j] = []; #empty list corresponding to each destination

        for s in list(sources):

            num_destinations_s = min(max(1,int((1 + (num_sources - 1)*INTRA_COFLOW_CONTENTION)*ir)),NUM_INP_PORTS);
            # print(num_sources);
            # print(ir);
            # print(num_destinations);
            # print(num_destinations_s);
            destinations_s = np.random.choice(list(destinations_set),num_destinations_s,replace=False);
            destinations_s.sort();
            for k in list(destinations_s):
                destination_source_dict[k].append(s);

        num_destinations_actual = 0;
        for d in list(destinations_set):
            num_sources_d = len(destination_source_dict[d]);
            if(num_sources_d==0):
                continue;
            num_destinations_actual = num_destinations_actual + 1;
            total_data_destination = max(int(hist_dist_dd.rvs(size=1)),1);
            sources_d = destination_source_dict[d];
            sources_d.sort();
            if(DESTINATION_DATA_DIST=='U'):
                data_across_sources_uniform = np.random.uniform(0,1,num_sources_d);
                data_across_sources = data_across_sources_uniform * total_data_destination / float(sum(data_across_sources_uniform));
            elif(DESTINATION_DATA_DIST=='Z'):
                data_across_sources_zipf = np.random.zipf(2,num_sources_d);
                data_across_sources = data_across_sources_zipf * total_data_destination / float(sum(data_across_sources_zipf));
            for l in range(num_sources_d):
                flow_size = max(1,int(data_across_sources[l]));
                num_flows = num_flows + 1;
                total_flow_size = total_flow_size + flow_size;
                F = {'Coflow_ID': i, 'Source_ID': sources_d[l], 'Destination_ID': d, 'Size': flow_size};
                flows.append(F);
    num_sources_list.append(num_sources);
    num_destinations_list.append(num_destinations_actual);

mean_flow_size = total_flow_size/num_flows; #mean flow size is in MB
flow_arrival_rate = float(LOAD_FACTOR * ACCESS_LINK_BANDWIDTH * NUM_INP_PORTS) / mean_flow_size;
flow_arrival_rate_milli_second = flow_arrival_rate/1000;
# flow_arrival_rate_micro_second = flow_arrival_rate/1000000;
beta = 1/flow_arrival_rate_milli_second;
# beta = 1/flow_arrival_rate_micro_second;

start = 0;
for f in flows:
    # inter_arrival = np.random.poisson(L);
    inter_arrival = np.random.exponential(scale=beta); #inter arrival time in micro seconds
    f['Start'] = start + inter_arrival;
    start = start + inter_arrival;

# generate coflow dictionaries
coflows = [];
for i in range(NUM_COFLOWS):
    C = {'Coflow_ID': i, 'Flows': [], 'Num_sources':num_sources_list[i], 'Num_destinations':num_destinations_list[i]};
    coflows.append(C);

for f in flows:
    coflows[f['Coflow_ID']]['Flows'].append(f);

for C in coflows:
    max_arrival_time = -1;
    count_flows = 0;
    for f in C['Flows']:
        count_flows = count_flows + 1;
        if(f['Start'] > max_arrival_time):
            max_arrival_time = f['Start'];
    C['Arrival_Time'] = int(max_arrival_time);
    C['Count_Flows'] = count_flows;

#output trace to file
outfile = OUTPUT_FILE;
out_file = open(outfile,'w');
out_file.write(str(NUM_INP_PORTS)+' '+str(NUM_COFLOWS)+'\n');

for C in coflows:
    l = [];
    l.append(str(C['Coflow_ID']));
    l.append(str(C['Arrival_Time']));
    l.append(str(C['Count_Flows']));
    l.append(str(C['Num_sources']));
    l.append(str(C['Num_destinations']));
    for f in C['Flows']:
        l.append(str(f['Source_ID']));
        l.append(str(f['Destination_ID']));
        l.append(str(f['Size']));
    line_to_print = ' '.join(l);
    out_file.write(line_to_print+'\n');

#enter coflow data to pickle
output_file = open(PICKLE_FILE,'wb');
pickle.dump(coflows,output_file);
output_file.close();
