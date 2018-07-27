import sys
import os
NUM_COFLOWS = int(sys.argv[1]);
ALPHA = (sys.argv[2]); #alpha value for code
NUM_INP_PORTS = 150;
LOAD_FACTOR = float(sys.argv[3]);
ACCESS_LINK_BANDWIDTH = (1024*2)/8; #1024*2 MBPS = 2GBPS, 2/8GBPS = 2Gbps

if(ALPHA=='FB-UP'):
    FILE = str(NUM_COFLOWS)+'-'+str(LOAD_FACTOR)+'-'+'FB-UP'
else:
    ALPHA = int(ALPHA)
    INTRA_COFLOW_CONTENTION = float(sys.argv[4]); #c discussed in the code, belongs to [0,1], the traffic is one to ir for c = 0 and all to all for c = 1
    SOURCE_NUM_DIST = sys.argv[5]#'U' for uniform, 'Z' for zipf, 'FB' for trace
    DESTINATION_DATA_DIST = sys.argv[6] #'U' for uniform, 'Z' for zipf
    FILE = str(NUM_COFLOWS)+'-'+str(LOAD_FACTOR)+'-'+str(ALPHA)+'-'+str(INTRA_COFLOW_CONTENTION*100)+'-'+str(SOURCE_NUM_DIST)+'-'+str(DESTINATION_DATA_DIST)
if not os.path.exists('size_dir'):
    os.mkdir('size_dir');
if not os.path.exists('max_min_ratio_dir'):
    os.mkdir('max_min_ratio_dir');
if not os.path.exists('width_dir'):
    os.mkdir('width_dir');
if not os.path.exists('load_dir'):
    os.mkdir('load_dir');
if not os.path.exists('inter_arrival_time_dir'):
    os.mkdir('inter_arrival_time_dir');
if not os.path.exists('numsources_dir'):
    os.mkdir('numsources_dir');
if not os.path.exists('numdestinations_dir'):
    os.mkdir('numdestinations_dir');
if not os.path.exists('irs_dir'):
    os.mkdir('irs_dir');
INP_PICKLE_FILE = 'pickles/' + FILE + '.pkl'
SIZE_FILE = 'size_dir/size-' + FILE + '.txt'
MAX_MIN_RATIO_FILE = 'max_min_ratio_dir/max_min_ratio-' + FILE + '.txt'
WIDTH_FILE = 'width_dir/width-' + FILE + '.txt'
LOAD_FILE = 'load_dir/load-' + FILE + '.txt'
MAX_LOAD_FILE = 'load_dir/max_load-' + FILE + '.txt'
MIN_LOAD_FILE = 'load_dir/min_load-' + FILE + '.txt'
MIN_LOAD_FILE_2 = 'load_dir/min_load-2-' + FILE + '.txt'
PLOT_FILE = 'load_dir/load_plot-' + FILE + '.eps'
INTER_ARRIVAL_TIME_FILE = 'inter_arrival_time_dir/inter_arrival-' + FILE + '.txt'
NUM_SOURCES_FILE = 'numsources_dir/numsources-' + FILE + '.txt'
NUM_DESTINATIONS_FILE =  'numdestinations_dir/numdestinations-' + FILE + '.txt'
IRS_FILE = 'irs_dir/irs-' + FILE + '.txt'
# MAX_DEST_PER_SOURCE_FILE = 'irs_cdfs/max-dest-' + FILE + '.txt'
# DEST_PER_SOURCE_FILE = 'irs_cdfs/dest-' + FILE + '.txt'
import pickle

import operator
import numpy as np
import matplotlib.pyplot as plt

# inp_file_name = sys.argv[1];
inp_file_name = INP_PICKLE_FILE;
inp_file = open(inp_file_name,'rb');
size_out_file = open(SIZE_FILE,'w');
max_min_ratio_out_file = open(MAX_MIN_RATIO_FILE,'w');
width_out_file = open(WIDTH_FILE,'w');
load_out_file = open(LOAD_FILE,'w');
max_load_out_file = open(MAX_LOAD_FILE,'w');
min_load_out_file = open(MIN_LOAD_FILE,'w');
min2_load_out_file = open(MIN_LOAD_FILE_2,'w');
inter_arrival_time_out_file = open(INTER_ARRIVAL_TIME_FILE,'w');
numsources_out_file = open(NUM_SOURCES_FILE,'w');
numdestinations_out_file = open(NUM_DESTINATIONS_FILE,'w');
irs_out_file = open(IRS_FILE,'w');
# max_dest_per_source_out_file = open(MAX_DEST_PER_SOURCE_FILE,'w');
# dest_per_source_out_file = open(DEST_PER_SOURCE_FILE,'w');
coflows = pickle.load(inp_file);

size_coflows = [];
max_min_ratio_coflows = [];
width_coflows = [];
arrival_time_coflows = [];
inter_arrival_time_coflows = [];
for C in coflows:
    size = 0;
    min_size = sys.maxint;
    max_size = -1;
    # destinations_per_source = {};
    # for i in range(NUM_INP_PORTS):
    #     destinations_per_source[i] = [];
    for F in C['Flows']:
        # destinations_per_source[F['Source_ID']].append(F['Destination_ID']);
        size = size + F['Size'];
        if(F['Size'] > max_size):
            max_size = F['Size'];
        if(F['Size'] < min_size):
            min_size = F['Size'];
    size_coflows.append(size);
    size_out_file.write(str(size)+'\n');

    max_min_ratio_coflows.append(float(max_size)/float(min_size));
    max_min_ratio_out_file.write(str(float(max_size)/float(min_size))+'\n');

    width_coflows.append(min(C['Num_sources'],C['Num_destinations']));
    width_out_file.write(str(min(C['Num_sources'],C['Num_destinations']))+'\n');

    numsources_out_file.write(str(C['Num_sources'])+'\n');

    numdestinations_out_file.write(str(C['Num_destinations'])+'\n');

    irs_out_file.write(str(float(C['Num_destinations'])/float(C['Num_sources']))+'\n');

    # max_num_destinations_per_source = -1;
    # for i in range(NUM_INP_PORTS):
    #     if(len(destinations_per_source[i]) > 0):
    #         dest_per_source_out_file.write(str(destinations_per_source[i])+'\n');
    #     if(len(destinations_per_source[i]) > max_num_destinations_per_source):
    #         max_num_destinations_per_source = len(destinations_per_source[i]);
    # max_dest_per_source_out_file.write(str(max_num_destinations_per_source)+'\n');
    # print(max_size);
    # print(min_size);


coflows.sort(key=operator.itemgetter('Arrival_Time'));
for C in coflows:
    arrival_time_coflows.append(C['Arrival_Time']);
# print(arrival_time_coflows[150]);
for i in range(1,len(arrival_time_coflows)):
    inter_arrival_time_coflows.append(arrival_time_coflows[i]-arrival_time_coflows[i-1]);
    inter_arrival_time_out_file.write(str(arrival_time_coflows[i]-arrival_time_coflows[i-1])+'\n');
loads_100_ms = [];
max_loads_100_ms = [];
min_loads_100_ms = [];
min2_loads_100_ms = [];
# while(i < len(coflows)):
#     coflows_within_time = [];

i = 0;
time = 100;
data_100_ms_sources = [];
for k in range(NUM_INP_PORTS):
    data_100_ms_sources.append(0);

while(time >= 0):
    coflows_within_time = [];


    while(i < len(coflows) and coflows[i]['Arrival_Time']<time):
        coflows_within_time.append(coflows[i]);
        i = i+1;


    # if(time==100000):
    #     print(time);
    #     print(len(coflows_within_time));
    for C in coflows_within_time:
        for F in C['Flows']:
            data_100_ms_sources[F['Source_ID']] = data_100_ms_sources[F['Source_ID']] + F['Size'];

    max_load_sources = float(max(data_100_ms_sources))*1000/(time*(1024*2)/8);
    min_load_sources = float(min(data_100_ms_sources))*1000/(time*(1024*2)/8);
    avg_load_sources = (float(sum(data_100_ms_sources))/NUM_INP_PORTS)*1000/(time*(1024*2)/8);
    data_100_ms_sources_array = np.array(data_100_ms_sources);
    k = 5;
    k_smallest = np.partition(data_100_ms_sources_array, k)[:k].tolist();
    min_2_load_sources = (float(sum(k_smallest))/k)*1000/(time*(1024*2)/8);
    loads_100_ms.append(avg_load_sources);
    load_out_file.write(str(avg_load_sources)+'\n');
    max_loads_100_ms.append(max_load_sources);
    max_load_out_file.write(str(max_load_sources)+'\n');
    min_loads_100_ms.append(min_load_sources);
    min_load_out_file.write(str(min_load_sources)+'\n');
    min2_loads_100_ms.append(min_2_load_sources);
    min2_load_out_file.write(str(min_2_load_sources)+'\n');




    time = time + 100;
    if(i == len(coflows)):
        break;
# print(loads_100_ms[-1]);
# print(max_loads_100_ms[-1]);
# print(min_loads_100_ms[-1]);
plt.figure(1);
plt.subplot(411);
plt.plot(loads_100_ms);
plt.yscale('log');
plt.grid(True);
plt.title('avg loads across all sources at 100ms intervals');
plt.subplot(412);
plt.plot(max_loads_100_ms);
plt.yscale('log');
plt.grid(True);
plt.title('max loads across all sources at 100ms intervals');
plt.subplot(413);
plt.plot(min_loads_100_ms);
plt.yscale('log');
plt.grid(True);
plt.title('min loads across all sources at 100ms intervals');
plt.subplot(414);
plt.yscale('log');
plt.grid(True);
plt.title('avg(min 5 loads) across all sources at 100ms intervals');
plt.savefig(PLOT_FILE, format='eps', dpi=1000);
# plt.show();
