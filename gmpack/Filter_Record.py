#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #
#    Class Documentation:                                           #
#                                                                   #
#                                                                   #
#                                                                   #
#                                                                   #
#                                                                   #
#                                                                   #
#                                                                   #
#                                                                   #
#                                                                   #
#                                                                   #
#   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #   #

# Modules
import numpy as np
import scipy


class FilterRecord(object):
    def __init__(self, time_series, low=0.0, high=0.0, f_type='band_pass', domain="frequency"):
        self.name = time_series     # file name of the time series
        self.domain = domain        # frequency or time
        self.range_min = low        # minimum filter value
        self.range_max = high       # maximum filter value
        self.filter_type = f_type   # low, high or band pass


        pass

    def apply(self):
        pass

    def design(self):
        pass

    def read(self):
        pass

    def write(self):
        pass