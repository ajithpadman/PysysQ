import logging

from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_clock_params import SQClockParams
from pysysq.sq_base.sq_event_manager import SQEventManager
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
    # logging.getLogger("SQServer").setLevel(logging.WARNING)
    #logging.getLogger("SQClock").setLevel(logging.WARNING)
    logging.getLogger("SQEventManager").setLevel(logging.WARNING)
    logging.getLogger("SQSimulator").setLevel(logging.WARNING)
    logging.getLogger("SQEventQueue").setLevel(logging.WARNING)
    clk_params = SQClockParams(
        clk_time_steps=2
    )
    evnt_mgr = SQEventManager()
    clk = SQClock(name='clk', params=clk_params, event_mgr=evnt_mgr)

    server_params = SQServerParams(service_clk_ticks=49)
    server = SQServer(name='Server1', params=server_params, event_mgr=evnt_mgr)
    server_params2 = SQServerParams(service_clk_ticks=5)
    server2 = SQServer(name='Server2', params=server_params2, event_mgr=evnt_mgr)
    clk.connect(server)

    simulation_params = SQSimulationParams(max_sim_time=100, time_step=0.10, children=[clk, server])

    simulator = SQSimulator(name='Sim', params=simulation_params,
                            event_mgr=evnt_mgr
                            )
    simulator.init()

    simulator.start()
