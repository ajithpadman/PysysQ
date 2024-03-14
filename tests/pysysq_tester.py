
from pysysq import *


if __name__ == '__main__':
    generate(json_file="input.json")
    # factory = SQDefaultObjectFactory(helper_factory=SQDefaultHelperFactory())
    # clock = factory.create_clock(name='Clock', clk_divider=1)
    # gen_q = factory.create_queue(name='GeneratorQueue', capacity=10)
    # generator = factory.create_packet_generator(name='Generator', clk=clock, output_q=gen_q)
    # proc_q = factory.create_queue(name='ProcessorQueue', capacity=10)
    # processor = factory.create_packet_processor(name='Processor', clk=clock, input_q=gen_q, output_q=proc_q)
    # filter_q = factory.create_queue(name='FilterQueue', capacity=10)
    # pkt_filter = factory.create_filter(name='Filter', clk=clock, input_q=proc_q, output_q=filter_q)
    # demux_q1 = factory.create_queue(name='DemuxQueue1', capacity=100)
    # demux_q2 = factory.create_queue(name='DemuxQueue2', capacity=100)
    # demux = factory.create_demux(name='Demux', clk=clock, input_q=filter_q, output_qs=[demux_q1, demux_q2])
    # processor_1_q = factory.create_queue(name='Processor1Queue', capacity=100)
    # processor_1 = factory.create_packet_processor(name='Processor1', clk=clock, input_q=demux_q1,
    #                                               output_q=processor_1_q)
    # processor_2_q = factory.create_queue(name='Processor2Queue', capacity=100)
    # processor_2 = factory.create_packet_processor(name='Processor2', clk=clock, input_q=demux_q2,
    #                                               output_q=processor_2_q)
    # merger_q = factory.create_queue(name='MergerQueue', capacity=100)
    # merger = factory.create_mux(name='Merger', clk=clock, input_qs=[processor_1_q, processor_2_q], output_q=merger_q)
    # sink = factory.create_packet_sink(name='Sink', clk=clock, input_q=merger_q)
    # simulator = factory.create_simulator(name='Simulator',max_sim_time=100,time_step= 0.10, children=[clock,
    #                                                                                                   generator,
    #                                                                                                   processor,
    #                                                                                                   pkt_filter,
    #                                                                                                   demux,
    #                                                                                                   processor_1,
    #                                                                                                   processor_2,
    #                                                                                                   merger,
    #                                                                                                   sink,
    #                                                                                                   gen_q,
    #                                                                                                   proc_q,
    #                                                                                                   filter_q,
    #                                                                                                   demux_q1,
    #                                                                                                   demux_q2,
    #                                                                                                   processor_1_q,
    #                                                                                                   processor_2_q,
    #                                                                                                   merger_q])
    # simulator.init()
    # simulator.start()
    # plotter = SQPlotter(name='processors', objs=[processor,processor_1,processor_2],output_file="processors.png", show_plot=False)
    # plotter2 = SQPlotter(name='Queues', objs=[ demux_q1,demux_q2],output_file="Queues.png", show_plot=False)
    # plotter.plot()
    # plotter2.plot()

