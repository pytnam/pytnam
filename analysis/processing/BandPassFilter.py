"""
Basic band-pass filtering feature.
By default, the filtering mechanism is Butterworth as implemented in the scipy.signal package.
Other filter designs will be successively added.
"""
import scipy.signal as signal
from analysis.Reportable import Reportable


class BandPassFilter(Reportable):
    def __init__(self, data, channels, method="Butterworth filter"):
        """
        :type data: ImportedData
        :type channels: List(String)
        :type method: String
        """
        self.data = data
        self.channels = channels
        self.method = method