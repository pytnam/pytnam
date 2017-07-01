"""
Extraction of the crucial EEG bands: low+high alpha, beta, gamma, theta.
"""

from collections import defaultdict

from analysis.Reportable import Reportable
import biosppy.signals as signals
import numpy as np

'''Created by rj as part of the Pytnam Project.'''


class BandExtractionFilter(Reportable):
    def __init__(self, data, channels):
        """
        Constructor method.
        :type data: ImportedData - the data to be analysed
        :type channels: List(String) - list of EEG record channel labels to be analysed
        """
        self.data = data
        self.channels = channels
        self.analysis_name = "Average band power extraction for gamma, alpha low/high, beta, gamma"
        self.parameters.append()

    def return_as_node(self):
        # TODO
        pass

    def extract_band_powers(self):
        """
        This method extracts average signal powers at the most important EEG frequency bands defined as follows:
        theta := 4-8 Hz
        alpha_low := 8-10 Hz
        alpha_high := 10-13 Hz
        beta := 13-25 Hz
        gamma := 25-40 Hz
        biosppy biosignal processing library is used as band power extraction tool.
        :return: defaultdict(String: np.array) - dictionary where keys are frequency names from
        {'theta', 'alpha_low', 'alpha_high', 'beta', 'gamma} and values are np.arrays containing extracted
        average power at a given frequency band (EEG channels as rows like in ImportedData objects).
        """
        # defaultdict signal (channel labels as keys):
        signal = self.data['signal']
        raw_list = []

        # Get the raw data in appropriate format (np.array with signal samples, channels as columns)
        for ch_label in self.channels:
            temp_tuple = signal[ch_label]
            single_channel = temp_tuple[1]
            raw_list.append(single_channel)
        raw_for_analysis = np.array(raw_list)
        raw_for_analysis = raw_for_analysis.transpose()

        # Retrieve the sampling rate of the data
        # (all channels are assumed to have the same sampling rate, as they come from the same record):
        sampling_rate = self.data['info']['frequencies'][self.channels[0]]

        # Run the bandpower analysis (as biosppy ReturnTuple object:
        long_return_tuple = signals.eeg.eeg(raw_for_analysis, sampling_rate, labels=None, show=False)

        # retrieve only the bandpower arrays (as dictionary with freqency band names as keys):
        names = ['theta', 'alpha_low', 'alpha_high', 'beta', 'gamma']
        result = defaultdict(lambda: None)
        for name in names:
            band_array = long_return_tuple[name].transpose()
            result[name] = band_array

        return result
