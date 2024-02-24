import logging

from pysysq.sq_base.sq_clock import SQClock
from pysysq.sq_base.sq_clock_params import SQClockParams
from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_server import SQServer
from pysysq.sq_base.sq_server_params import SQServerParams
from pysysq.sq_base.sq_time_base import SQTimeBase

from pysysq.sq_simulaton_params import SQSimulationParams
from pysysq.sq_simulator import SqSimulator

logging.basicConfig(filename='sim.log', format=f'%(asctime)s:: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    encoding='utf-8', level=logging.DEBUG)


def tick_handler():
    logging.info(
        f'[custom_tick_handler]: Current Sim Time{SQTimeBase.get_current_sim_time()}')


if __name__ == '__main__':
    clk_params = SQClockParams(
        name="clk",
        evt_q=0,
        clk_time_steps=2
    )
    evnt_mgr = SQEventManager()
    clk = SQClock(params=clk_params, event_mgr=evnt_mgr)

    server_params = SQServerParams(name='Server1',
                                   evt_q=0,
                                   service_clk_ticks=10
                                   )
    server = SQServer(params=server_params, event_mgr=evnt_mgr)
    server_params2 = SQServerParams(name='Server2',
                                    evt_q=0,
                                    service_clk_ticks=5
                                    )
    server2 = SQServer(params=server_params2, event_mgr=evnt_mgr)
    clk.connect(server).connect(server2)
    simulation_params = SQSimulationParams(name="sim",
                                           evt_q=0,
                                           max_sim_time=100,
                                           time_step=0.10,
                                           sq_objects=[clk, server,server2]
                                           )

    simulator = SqSimulator(params=simulation_params,
                            event_mgr=evnt_mgr
                            )

    simulator.start()
