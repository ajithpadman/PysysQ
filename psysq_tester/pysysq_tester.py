import logging

from psysq_tester.sq_pkt_proc1_helper import SQPktProc1Helper
from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_event.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_mux_demux import SQMux, SQDemux
from pysysq.sq_base.sq_mux_demux.sq_rr_q_selector import SQRRQueueSelector
from pysysq.sq_base.sq_pkt_gen import SQPacketGenerator
from pysysq.sq_base.sq_pkt_processor import SQPktProcessor
from pysysq.sq_base.sq_pkt_sink.sq_pkt_sink import SQPktSink
from pysysq.sq_base.sq_queue import SQSingleQueue
from pysysq.sq_base.sq_statistics.sq_plotter import SQPlotter
from pysysq.sq_simulator import SQSimulator

logger = logging.getLogger("Tester")

if __name__ == '__main__':
    evnt_mgr = SQEventManager()
    evnt_mgr.set_log_level(logging.WARNING)
    clk = SQClock(name='clk', event_mgr=evnt_mgr)
    clk.set_log_level(logging.WARNING)
    generator = SQPacketGenerator(name='Generator', event_mgr=evnt_mgr)
    gen_q = SQSingleQueue(name='Generator_Queue', event_mgr=evnt_mgr, capacity=100)
    proc1_q = SQSingleQueue(name='Proc1_Queue', event_mgr=evnt_mgr, capacity=1)
    proc2_q = SQSingleQueue(name='Proc2_Queue', event_mgr=evnt_mgr, capacity=10)
    sink_q = SQSingleQueue(name='Sink_Queue', event_mgr=evnt_mgr, capacity=10)
    demux = SQDemux(name='LoadBalancer',
                    event_mgr=evnt_mgr,
                    no_of_ports=2,
                    input_q=gen_q,
                    queues=[proc1_q, proc2_q],
                    helper=SQRRQueueSelector([proc1_q, proc2_q]))
    sq_pkt_proc1 = SQPktProcessor(name='PktProc1',
                                  event_mgr=evnt_mgr,
                                  input_queue=proc1_q,
                                  clk=clk,
                                  helper=SQPktProc1Helper(name='PktProc1Helper'))
    sq_pkt_proc2 = SQPktProcessor(name='PktProc2',
                                  event_mgr=evnt_mgr,
                                  input_queue=proc2_q,
                                  clk=clk)
    sink1 = SQPktSink(name='Sink', event_mgr=evnt_mgr)

    clk.control_flow(generator).control_flow(gen_q).control_flow(demux)
    demux.control_flow(sq_pkt_proc1)
    demux.control_flow(sq_pkt_proc2)
    clk.control_flow(sq_pkt_proc1).control_flow(sink_q)
    clk.control_flow(sq_pkt_proc2).control_flow(sink_q)
    sq_pkt_proc1.control_flow(sink1)

    simulator = SQSimulator(name='Sim',
                            event_mgr=evnt_mgr,
                            max_sim_time=100,
                            children=[
                                clk, generator,
                                sq_pkt_proc1,
                                proc1_q,
                                proc2_q,
                                gen_q,
                                sink1
                            ])
    simulator.init()
    simulator.start()
    sq_plotter = SQPlotter(name='Plotter',
                           objs=[sq_pkt_proc1, sq_pkt_proc2], output_file='sq_pkt_proc1.png', show_plot=True)
    sq_plotter2 = SQPlotter(name='Plotter2',
                            objs=[proc1_q, proc2_q], output_file='proc1_q.png')
    sq_plotter.plot()
    sq_plotter2.plot()
