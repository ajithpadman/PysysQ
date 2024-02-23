import logging

from pysysq.sq_base.sq_event_manager import SQEventManager
from pysysq.sq_base.sq_time_base import SQTimeBase
from pysysq.sq_clock import SQClock
from pysysq.sq_clock_params import SQClockParams

from pysysq.sq_simulaton_params import SQSimulationParams
from pysysq.sq_simulator import SqSimulator

logging.basicConfig(filename='sim.log', format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
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
    clk.set_tick_handler(tick_handler)
    simulation_params = SQSimulationParams(name="sim",
                                           evt_q=0,
                                           max_sim_time=100,
                                           time_step=0.10,
                                           sq_objects=[clk]
                                           )

    simulator = SqSimulator(params=simulation_params,
                            event_mgr=evnt_mgr
                            )
    simulator.start()
