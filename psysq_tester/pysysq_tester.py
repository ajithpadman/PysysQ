import logging

from pysysq import *

logger = logging.getLogger("Tester")

if __name__ == '__main__':
    generate_and_run(json_file='input.json', simulation='tester', show_plot=True)
    # factory = SQDefaultObjectFactory(helper_factory=SQDefaultHelperFactory())
    #
    # clk = factory.create_clock(name='Clock',
    #                            clk_divider=1)
    # generator = factory.create_packet_generator(name='Generator')
    # gen_q = factory.create_queue(name='Gen_Queue',
    #                              capacity=10)
    # proc1_q = factory.create_queue(name='Proc1_Queue',
    #                                capacity=10)
    # proc2_q = factory.create_queue(name='Proc2_Queue',
    #                                capacity=10)
    # sink_q = factory.create_queue(name='Sink_Queue',
    #                               capacity=10)
    # demux = factory.create_demux(name='Demux',
    #                              input_q=gen_q,
    #                              tx_qs=[proc1_q, proc2_q])
    # sq_pkt_proc1 = factory.create_packet_processor(name='PktProc1',
    #                                                clk=clk,
    #                                                input_q=proc1_q)
    # sq_pkt_proc2 = factory.create_packet_processor(name='PktProc2',
    #                                                clk=clk,
    #                                                input_q=proc2_q)
    # sink1 = factory.create_packet_sink(name='Sink1')
    #
    # clk.control_flow(generator).control_flow(gen_q).control_flow(demux)
    # demux.control_flow(sq_pkt_proc1)
    # demux.control_flow(sq_pkt_proc2)
    # clk.control_flow(sq_pkt_proc1).control_flow(sink_q)
    # clk.control_flow(sq_pkt_proc2).control_flow(sink_q)
    # sq_pkt_proc1.control_flow(sink1)
    # simulator = factory.create_simulator(name='Simulator',
    #                                      max_sim_time=100,
    #                                      time_step=0.1,
    #                                      children=[clk, generator, gen_q, proc1_q, proc2_q, sink_q, demux, sq_pkt_proc1,
    #                                                sq_pkt_proc2, sink1])
    # simulator.init()
    # simulator.start()
    # sq_plotter = SQPlotter(name='Plotter',
    #                        objs=[sq_pkt_proc1, sq_pkt_proc2], output_file='sq_pkt_proc1.png', show_plot=True)
    # sq_plotter2 = SQPlotter(name='Plotter2',
    #                         objs=[proc1_q, proc2_q], output_file='proc1_q.png')
    # sq_plotter.plot()
    # sq_plotter2.plot()
