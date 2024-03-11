from pysysq.sq_base.sq_filter import SQFilterHelper


class SQAllPassFilter(SQFilterHelper):

    def filter(self, pkt) -> bool:
        return True
