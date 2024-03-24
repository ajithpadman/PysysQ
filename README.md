# PySysQ
PySysQ is a python package helping to implement discrete event simulations based on queueing theory.
The package provides the following elements to create a simulation

## Simulation Elements

### 1. SQSimulator
SQSimulator composes all the simulation elements and creates relationship between them.
SQSimulator runs the simulation event loop.Each loop is counted as a single simulation time tick.
#### Properties
- `max_sim_time`: Maximum number of loops the simulator will run.
- `time_step`: the delay in seconds between two simulation loops.

### 2. SQClock
SQClock is a simulation object that ticks at specific interval on the simulation loops. 
Other Simulation Objects can make use of the SQClock object to generate self clock timing.
The Simulation objects using the same clock object as their clock source will be operating in a synchronous manner.
#### Properties
- `clk_divider`: the delay in seconds between two clock ticks with respect to the simulation loops.

### 3. SQPacketGenerator
SQPacketGenerator is a simulation object that generates packets at specific interval on the simulation loops.
#### Properties
- `clk`: clock for timing packet generation.
- `output_q`: the queue to which the generated packets will be pushed.
- `helper`: the helper class is an object of SQPktGenHelper class.
  - ##### SQPktGenHelper
  - The SQPktGenHelper class is a helper class for SQPacketGenerator.
    The class provides the following methods to help the packet generation process.
    - `generate_pkts()`: generates  packets and keeps own pushing one packet per clock tick to output queue.