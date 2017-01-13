# -*- coding: utf-8 -*-
# This module was created by Wiktor Rorot <wiktor.rorot@gmail.com> as a part of pytnam project (https://github.com/pytnam/pytnam) and is licensed under GNU GPL.

import numpy as np
from collections import defaultdict
import input_interface


class ImportedData:

    """Objects of this class hold the imported data."""

    def __init__(self, path):
        header, signal = input_interface.Reader(path).data
        self.data = self.__importer(header, signal)

    def get_signal(self):
        return self.data["signal"]

    def get_info(self):
        return self.data["info"]

    @staticmethod
    def __importer(header, signal):

        """
        Changes format of data.

        Takes as an argument dict representing a header (of e.g. edf file) and dict representing the signal.

        RETURNS:
            data (defaultdict((np.array, np.array))): a dictionary where:
                key 'signal', value dictionary with following format:
                    key: label, value: tuple of which 1st element is numpy.array of timestamps, and 2nd element  is numpy.array of sample values at those timestamps
                key 'info', value dictionary with following keys:
                    patient_id (string): local patient id
                    frequencies (dictionary - string: float): key: label (an element of labels), value: frequency of the signal;
                    stardate (string): startdate of the recording (dd.mm.yy) (for more info see edf and edf+ specs at: http://www.edfplus.info/specs/index.html)
                    starttime (string): starttime of the recording (hh.mm.ss)
                    physical_dim (dictionary - string: string): key: label (an element of labels), value: physical dimension;
                    prefiltering (dictionary - string: string): key: label (an element of labels), value: signal's prefiltering;

        TODO: discuss whether the proposed format is okay (meaning the format of the signal) - it lets us have different frequencies in different signals; discuss whether the 'info' section has enough data
        """
        data = defaultdict(lambda: (np.array, np.array))

        for label in sorted(signal.keys()):
            freq = header['frequency'][label]
            time = [(0 + (x/freq)) for x in range(header['num_records']*header['num_samples'][label])]
            data["signal"][label] = (np.array(time), signal[label])

        data['info'] = defaultdict(lambda: None)

        data['info']['frequencies'] = header['frequency']
        data['info']['patient_id'] = header['patient_id']
        data['info']['startdate'] = header['startdate']
        data['info']['starttime'] = header['starttime']
        data['info']['physical_dim'] = header['physical_dim']
        data['info']['prefiltering'] = header['prefiltering']

        return data
