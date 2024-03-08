from pysysq.sq_base.sq_filter import SQFilterConfig


class SQAllPassFilter(SQFilterConfig):

    def filter(self, pkt) -> bool:
        return True
