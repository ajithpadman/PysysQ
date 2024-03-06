import logging

from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_event.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_pkt_gen import SQPacketGenerator
from pysysq.sq_base.sq_pkt_processor import SQPktProcessor
from pysysq.sq_base.sq_pkt_sink.sq_pkt_sink import SQPktSink
from pysysq.sq_base.sq_queue import SQSingleQueue
from pysysq.sq_base.sq_queue.sq_multi_queue import SQMultiQueue
from pysysq.sq_base.sq_statistics.sq_plotter import SQPlotter
from pysysq.sq_simulator import SQSimulator

logger = logging.getLogger("Tester")


if __name__ == '__main__':
    evnt_mgr = SQEventManager()
    evnt_mgr.set_log_level(logging.WARNING)
    clk = SQClock(name='clk', event_mgr=evnt_mgr)
    generator = SQPacketGenerator(name='Generator', event_mgr=evnt_mgr)
    queue1 = SQSingleQueue(name='Queue1', event_mgr=evnt_mgr, capacity=10)
    queue2 = SQSingleQueue(name='Queue2', event_mgr=evnt_mgr, capacity=5)
    queue3 = SQSingleQueue(name='Queue3', event_mgr=evnt_mgr, capacity=100)
    output_queue1 = SQSingleQueue(name='OutputQueue1', event_mgr=evnt_mgr, capacity=10)
    output_queue2 = SQSingleQueue(name='OutputQueue2', event_mgr=evnt_mgr, capacity=100)
    output_queue3 = SQSingleQueue(name='OutputQueue3', event_mgr=evnt_mgr, capacity=100)
    multi_q = SQMultiQueue(name='Multi_Q', event_mgr=evnt_mgr, queues=[queue1, queue2, queue3])

    sq_pkt_proc1 = SQPktProcessor(name='PktProc1',
                                  event_mgr=evnt_mgr,
                                  input_queue=multi_q,
                                  output_queue=output_queue1,
                                  clk=clk,
                                  metadata={'metadata1': True})
    sq_pkt_proc2 = SQPktProcessor(name='PktProc2',
                                  event_mgr=evnt_mgr,
                                  input_queue=multi_q,
                                  output_queue=output_queue2,
                                  clk=clk)
    sq_pkt_proc3 = SQPktProcessor(name='PktProc3',
                                  event_mgr=evnt_mgr,
                                  input_queue=multi_q,
                                  output_queue=output_queue3,
                                  clk=clk
                                  )

    sink1 = SQPktSink(name='Sink', event_mgr=evnt_mgr, input_queue=output_queue1)
    sink2 = SQPktSink(name='Sink2', event_mgr=evnt_mgr, input_queue=output_queue2)
    sink3 = SQPktSink(name='Sink3', event_mgr=evnt_mgr, input_queue=output_queue3)

    clk.control_flow(generator).control_flow(multi_q)
    clk.control_flow(sq_pkt_proc1).control_flow(sink1)
    clk.control_flow(sq_pkt_proc1).control_flow(sink1)
    clk.control_flow(sq_pkt_proc2).control_flow(sink2)
    clk.control_flow(sq_pkt_proc3).control_flow(sink3)

    sq_pkt_proc1.data_flow(sq_pkt_proc2)

    simulator = SQSimulator(name='Sim',
                            event_mgr=evnt_mgr,
                            children=[
                                clk, generator,
                                sq_pkt_proc1,
                                sq_pkt_proc2,
                                sq_pkt_proc3,
                                multi_q,
                                queue1,
                                queue2,
                                queue3,
                                output_queue1,
                                output_queue2,
                                output_queue3,
                                sink1,
                                sink2,
                                sink3
                            ])
    simulator.init()
    simulator.start()
    sq_plotter = SQPlotter(name='Plotter',
                           objs=[queue1], output_file='queue1.png')
    sq_plotter2 = SQPlotter(name='Plotter2',
                            objs=[queue2], output_file='queue2.png')
    sq_plotter.plot()
    sq_plotter2.plot()
