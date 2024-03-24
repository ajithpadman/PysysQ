from .sq_sim_data_gen_strategy import SQSimulatorDataGenStrategy, \
    SQClockDataGenStrategy, SQSISODataGenStrategy, SQMISODataGenStrategy, \
    SQSIMODataGenStrategy, SQNISODataGenStrategy, SQSINODataGenStrategy, SQQueueDataGenStrategy


class SQSimDataGenCtx:
    def __init__(self):
        self.str = None
        self.strategy_map = {
            'SQSimulator': SQSimulatorDataGenStrategy(ctx=self),
            'SQClock': SQClockDataGenStrategy(ctx=self),
            'SQFilter': SQSISODataGenStrategy(ctx=self),
            'SQMerger': SQMISODataGenStrategy(ctx=self),
            'SQMux': SQMISODataGenStrategy(ctx=self),
            'SQDemux': SQSIMODataGenStrategy(ctx=self),
            'SQPacketGenerator': SQNISODataGenStrategy(ctx=self),
            'SQPktProcessor': SQSISODataGenStrategy(ctx=self),
            'SQPktSink': SQSINODataGenStrategy(ctx=self),
            'SQQueue': SQQueueDataGenStrategy(ctx=self),
            'SQSplitter': SQSIMODataGenStrategy(ctx=self)

        }
        self.factory_map = {
            'SQSimulator': 'create_simulator',
            'SQClock': 'create_clock',
            'SQFilter': 'create_filter',
            'SQMerger': 'create_merger',
            'SQMux': 'create_mux',
            'SQDemux': 'create_demux',
            'SQPacketGenerator': 'create_packet_generator',
            'SQPktProcessor': 'create_packet_processor',
            'SQPktSink': 'create_packet_sink',
            'SQQueue': 'create_queue',
            'SQSplitter': 'create_splitter'
        }
        self.type = None

    @property
    def strategy(self):
        return self.str

    @strategy.setter
    def strategy(self, strategy):
        self.str = strategy

    @property
    def factory(self):
        return self.factory_map[self.type]

    @factory.setter
    def factory(self, factory):
        self.factory_map[self.type] = factory

    def generate(self, data: dict):
        self.type = data['type']
        if self.type in self.strategy_map:
            self.strategy = self.strategy_map[self.type]
        else:
            raise ValueError(f'Invalid Type {self.type}')
        return self.strategy.generate(data)
