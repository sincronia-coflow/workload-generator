# Coflow workload generator

Runs without errors with numpy 1.14.1, scipy 1.0.0 and matplotlib 2.1.2 

trace_producer.py is used to generate coflow traces with desired parameters and distribution_procuer.py can be used to generate distributions of various parameters for the generated trace.

##### python trace_producer.py [Number of coflows] [Alpha (1-MAX_PORT_COUNT)] [Network Load (0.0-1.0)] [C (0.0-1.0)] [Source_Dist (U/Z)] [Destination_Dist (U/Z)] 

Alpha is the maximum number of senders, C is the intra-coflow contention (C = 0 or no contention denotes the case where no two flows within a coflow contend for bandwidth and C=1 corresponds to the maximum contention case of all-to-all connections between each source and destination port), Source_Dist is the distribution of number of senders (Uniform or Zipf), Destination_Dist is the distribution of data among the destinations (Uniform or Zipf). For e.g. to generate a trace with 2000 coflows and 0.9 network load, with each coflow having a maximum of 20 sources, having 0.5 contention and uniform source-destination distributions

##### python trace_producer.py 2000 0.9 20 0.5 U U

Also the supplied Facebook trace consisting of 526 coflows (taken from https://github.com/coflow/coflow-benchmark) can be upsampled using the same generater by specifying FB-UP instead of distribution variables. For e.g. to upsample the 526-coflow trace to 2000 coflows and 0.9 network load

##### python trace_producer.py 2000 FB-UP 0.9 

To analyse the distributions of the generated traces run

##### python distribution_producer.py [Number of coflows] [Alpha] [Load] [C] [Source Dist] [Destination Dist]

or

##### python distribution_producer.py [Number of coflows] FB-UP [Load] 

to generate dataset for distributions of size, width, max/min ratio of size, avg max and min loads, inter arrival time and incast ratio for coflow trace generated. The obtained txt files in respective folder for each characteristic could be used to find mean, median or cdf distribution.
