import logging

from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_clock_params import SQClockParams
from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_normal_pkt_gen_params import SQNormalPktGenParams
from pysysq.sq_base.sq_pkt_gen import SQPacketGenerator
from pysysq.sq_base.sq_poisson_pkt_gen_params import SQPoissonPktGenParams
from pysysq.sq_base.sq_pkt_processor import SQPktProcessor
from pysysq.sq_base.sq_pkt_processor_params import SQPktProcessorParams
from pysysq.sq_base.sq_plotter import SQPlotter
from pysysq.sq_base.sq_port_selection import PortSelection
from pysysq.sq_base.sq_queue import SQQueue
from pysysq.sq_base.sq_queue_params import SQQueueParams
from pysysq.sq_base.sq_replicator import SQReplicator
from pysysq.sq_base.sq_replicator_params import SQReplicatorParams
from pysysq.sq_base.sq_server import SQServer
from pysysq.sq_base.sq_server_params import SQServerParams
from pysysq.sq_base.sq_time_base import SQTimeBase

from pysysq.sq_simulaton_params import SQSimulationParams
from pysysq.sq_simulator import SQSimulator

logger = logging.getLogger("Tester")


def tick_handler():
    logger.info(
        f'[custom_tick_handler]: Current Sim Time{SQTimeBase.get_current_sim_time()}')


if __name__ == '__main__':
    # logging.getLogger("SQPktProcessor").setLevel(logging.WARNING)
    logging.getLogger("SQPacketGenerator").setLevel(logging.WARNING)
    logging.getLogger("SQClock").setLevel(logging.WARNING)
    logging.getLogger("SQEventManager").setLevel(logging.WARNING)
    # logging.getLogger("SQQueue").setLevel(logging.WARNING)
    logging.getLogger("SQSimulator").setLevel(logging.WARNING)
    logging.getLogger("SQEventQueue").setLevel(logging.WARNING)
    clk_params = SQClockParams(
        clk_time_steps=1
    )
    evnt_mgr = SQEventManager()
    clk = SQClock(name='clk', params=clk_params, event_mgr=evnt_mgr)

    generator_params = SQPoissonPktGenParams(
        rate=10,
        size=10,
        classes=["CAN", "UDP", "TCP"],
        priorities=[1, 2, 3]
    )
    gen_normal_params = SQNormalPktGenParams(
        no_pkts_mean=100,
        no_pkts_sd=200,
        pkt_size_mean=100,
        pkt_size_sd=200,
        classes=["CAN", "UDP", "TCP"],
        priorities=[1, 2, 3]
    )
    generator = SQPacketGenerator(name='Generator', params=gen_normal_params, event_mgr=evnt_mgr)

    replication_params = SQReplicatorParams(capacity=100, no_of_ports=3, port_selection=PortSelection.BROADCAST)
    replicator = SQReplicator(name='Replicator', params=replication_params, event_mgr=evnt_mgr)

    sq_pkt_proc1_params = SQPktProcessorParams(
        clk=clk,
        queue=replicator.get_queue(0),
    )
    sq_pkt_proc2_params = SQPktProcessorParams(
        clk=clk,
        queue=replicator.get_queue(1),
    )
    sq_pkt_proc3_params = SQPktProcessorParams(
        clk=clk,
        queue=replicator.get_queue(2),
    )
    sq_pkt_proc1 = SQPktProcessor(name='PktProc1', params=sq_pkt_proc1_params, event_mgr=evnt_mgr)
    sq_pkt_proc2 = SQPktProcessor(name='PktProc2', params=sq_pkt_proc2_params, event_mgr=evnt_mgr)
    sq_pkt_proc3 = SQPktProcessor(name='PktProc3', params=sq_pkt_proc3_params, event_mgr=evnt_mgr)

    simulation_params = SQSimulationParams(max_sim_time=1000,
                                           time_step=0.10,
                                           children=[clk, generator, sq_pkt_proc1, sq_pkt_proc2, sq_pkt_proc3,
                                                     replicator])
    clk.connect(generator).connect(replicator)
    clk.connect(sq_pkt_proc1)
    clk.connect(sq_pkt_proc2)
    clk.connect(sq_pkt_proc3)

    simulator = SQSimulator(name='Sim', params=simulation_params,
                            event_mgr=evnt_mgr
                            )
    simulator.init()

    simulator.start()
    sq_plotter = SQPlotter(name='Plotter',
                           objs=[sq_pkt_proc3])
    sq_plotter.plot()
