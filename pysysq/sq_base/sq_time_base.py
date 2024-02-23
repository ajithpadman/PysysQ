import time


class SQTimeBase:
    current_sim_time = 0
    current_host_time = 0

    @classmethod
    def get_current_sim_time(cls):
        return cls.current_sim_time

    @classmethod
    def get_current_host_time(cls):
        return cls.current_host_time

    @classmethod
    def update_current_sim_time(cls):
        cls.current_sim_time += 1

    @classmethod
    def update_current_host_time(cls):
        cls.current_host_time = time.time() - cls.current_host_time

    @classmethod
    def reset_current_sim_time(cls):
        cls.current_sim_time =0

    @classmethod
    def reset_current_host_time(cls):
        cls.current_host_time = 0
