 # Coflow workload generator

Generator to produce coflow traces with varying characteristics using several parameters, as discussed below. 

The following list of coflow properties can be varied using the workload generator:
1. Coflow size -- Sum of sizes of constituent flows
2. Coflow width -- Minimum number of sources/destinations used by the flows of a coflow
3. Incast Ratio -- Ratio of number of destinations to the number of sources of constituent flows
4. Skew -- Ratio fo maximum and minimum flow sizes of a coflow
5. Inter-arrival Time -- Time between arrival of two successive coflows, related to the load on the network.

#### Parameters
The generator uses the following parameters which can affect the properties shown alongside.

 Input Parameter        | Description           | Affected Coflow Property  
 :-------------: |:-------------:| :-----:
 N     | Number of coflows | Scale of the trace 
  a     | Max coflow width      |   Width, Size, Skew and Inter-arrival Time 
 c| Intra-coflow contention      |    Width, Size, Skew and Inter-arrival Time (Mild) 
 D_1| Source Frequency Distribution      |    Width 
 D_2 | Incast Ratio Distribution      |    Incast-ratio and Width 
 D_3 | Total Destination Data Distribution      |    Size and Skew
 D_4 | Intra-Destination Data Distribution      |    Skew 
 L | Network Load      |    Inter-arrival Time 
 BW | Access Link Bandwidth     |    Inter-arrival Time 
 P | Total Number of Sources/Destinations      |    Width, Inter-arrival Time 

The generator can sample various parameters of a publicly available [coflow trace](https://github.com/coflow/coflow-benchmark) , which was obtained from running jobs on a cluster in Facebook, and use them to upscale various other properties like trace size, network load, etc. 

#### Usage of Parameters
The values following parameters (variable used in generator) should be manually entered before running the generator: N (`NUM_COFLOWS`), P (`NUM_INP_PORTS`) and BW (`ACCESS_LINK_BANDWIDTH`).

The parameters a(`ALPHA`), c(`INTRA_COFLOW_CONTENTION`), D_1 (`SOURCE_NUM_DIST`), D_4 (`DESTINATION_DATA_DIST`) and L (`LOAD_FACTOR`) are specified during runtime as command line arguments.

The parameters D_2 and D_4 are sampled from the [Facebook trace](https://github.com/coflow/coflow-benchmark) and are stored using variables `hist_dist_ir` and `hist_dist_dd` in the generator, and can be easily extended to allow for any arbitrary distribution.

#### Running the Generator
The generator runs without errors with python >= 2.7.14, numpy >= 1.14.1, scipy >= 1.0.0 and matplotlib >= 2.1.2. 

To run the generator, use command
```
python trace_producer.py [NUM_COFLOWS] [ALPHA] [LOAD_FACTOR] [INTRA_COFLOW_CONTENTION] [SOURCE_NUM_DIST] [DESTINATION_DATA_DIST]
```

The following range of values can be used for the command line arguments

 Command Line Argument           | Input Value Range  
:-------------:| :-----:
 `NUM_COFLOWS` | `int` value > 0 
 `ALPHA`      |   `int` value in \{1,...,P\} 
 `LOAD_FACTOR`     |    `float` value in (0,1) 
 `INTRA_COFLOW_CONTENTION`      |    `float` value in [0,1] 
 `SOURCE_NUM_DIST`      |    `char` value U (unfiform dist) or Z (zipf dist) 
 `DESTINATION_DATA_DIST`      |    `char` value U (unfiform dist) or Z (zipf dist) 

For e.g. to generate a trace with 2000 coflows and 0.9 network load, with each coflow having a maximum of 20 sources, having 0.5 contention and uniform source frequency and destination data distributions
```
python trace_producer.py 2000 0.9 20 0.5 U U
```

To keep the parameters same as Facebook trace and vary just the number coflows and network load, run
```
python trace_producer.py 2000 FB-UP 0.9
```

#### Output Format
The generated trace is stored in a directory **traces/**. The trace has the following format
```
Line1: <NUM_INP_PORTS> <NUM_COFLOWS>
Line2: <Coflow 1ID> <Arrival Time (in millisec)> <Number of Flows in Coflow 1> <Number of Sources in Coflow 1> <Number of Destinations in Coflow 1> <Flow 1 Source ID> <Flow 1 Destination ID> <Flow 1 Size (in MB)> ... <Flow N Source ID> <Flow N1 Destination ID> <Flow N1 size (in MB)>
...
...
Line i+1:  <Coflow iID> <Arrival Time (in millisec)> <Number of Flows in Coflow i> <Number of Sources in Coflow i> <Number of Destinations in Coflow i> <Flow 1 Source ID> <Flow 1 Destination ID> <Flow 1 Size (in MB)> ... <Flow N Source ID> <Flow Ni Destination ID> <Flow Ni size (in MB)>
...
```

#### Analyzing the Output
A helper script **distribution_producer.py** is also provided to help generate the distributions of parameters: size, width, skew, avg-max-min network load, inter-arrival time and incast ratio for the generated traces.

To run this, use exactly the same arguments provided to generate the tracefile
```
python distribution_producer.py [NUM_COFLOWS] [ALPHA] [LOAD_FACTOR] [INTRA_COFLOW_CONTENTION] [SOURCE_NUM_DIST] [DESTINATION_DATA_DIST]
```
or
```
python distribution_producer.py [NUM_COFLOWS] FB-UP [LOAD_FACTOR]
```

A **.txt** file for each parameter is generated with a parameter value corresponding to each coflow in the tracefile. The **.txt** files can be found in respective folders named according to the parameter involved. These files can then be easily used to obtain mean, median or cdf of the required distributions.