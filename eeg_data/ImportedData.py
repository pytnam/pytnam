# -*- coding: utf-8 -*-

from collections import defaultdict
from eeg_data.input_interface.Reader import Reader
import numpy as np


class ImportedData:

    """Objects of this class hold the imported data."""

    def __init__(self, path):
        data = Reader(path)
        header, signal = data.data
        self.data = self.__importer(header, signal)

    @staticmethod
    def __importer(header, signal):

        """
        Changes format of data.

        Takes as an argument dict representing a header (of e.g. edf file) and dict representing the signal.

        RETURNS:
            data (defaultdict((np.array, np.array))): a dictionary where:
                key 'signal', value dictionary with following format:
                    key: label, value: tuple of which 1st element is numpy.array of timestamps, and 2nd element  is 
                    numpy.array of sample values at those timestamps
                key 'info', value dictionary with following keys:
                    patient_id (string): local patient id
                    frequencies (dictionary - string: float): key: label (an element of labels), value: frequency of the
                    signal;
                    startdate (string): startdate of the recording (dd.mm.yy) (for more info see edf and edf+ specs at: 
                    http://www.edfplus.info/specs/index.html)
                    starttime (string): starttime of the recording (hh.mm.ss)
                    physical_dim (dictionary - string: string): key: label (an element of labels), value: physical 
                    dimension;
                    prefiltering (dictionary - string: string): key: label (an element of labels), value: signal's 
                    prefiltering;
                    events (list of arrays): list of events; each event is represented as an array of times of marker's 
                    occurrence

        TODO: discuss whether the proposed format is okay (meaning the format of the signal) -
        it lets us have different frequencies in different signals; discuss whether the 'info' section has enough data 
        -> it probably doesn't since I omitted the physical_max and digital_max, so the data on the
        """

        data = defaultdict(lambda: defaultdict(lambda: None))

        for label in sorted(signal.keys()):
            freq = header['frequency'][label]
            time = [(x*1000/freq) for x in range(header['num_records']*header['num_samples'][label])] # should be in milliseconds now
            data["signal"][label] = np.array([np.array(time), np.array(signal[label])])

        data['info'] = defaultdict(lambda: None)

        data['info']['frequencies'] = header['frequency']
        data['info']['patient_id'] = header['patient_id']
        data['info']['startdate'] = header['startdate']
        data['info']['starttime'] = header['starttime']
        data['info']['physical_dim'] = header['physical_dim']
        data['info']['prefiltering'] = header['prefiltering']

        data['info']['events'] = []
        # not sure if this is a good enough way to represent events -
        # maybe it should be a dictionary with some info about the event as key? and an array (of time stamps) as value

        return data

    def get_event_from_event_channel(self, channel_name, threshold=1000):
        # do we want to have some meta data about the event? what was it, e.g. how loud was the sound, etc.
        # what other types of event extraction do we want?

        """
        This function extracts information about an event from a given channel (@channel_name) in the simplest way -
        it treats as an event marker a value of signal that is higher than a given value (@threshold).
        This function is best when in the data there is a channel that has only non-zero values when the event occurs
        (an event channel).
        """

        markers = []
        for x in range(self.data['signal'][channel_name].shape()[1]):
            time, value = self.data['signal'][channel_name][..., x]
            if value >= threshold:  # ">=" was an arbitrary decision
                markers.append(time)

        self.data['info']['events'].append(np.array(markers))

    def remove_channel(self, channel_name):
        del self.data["signal"][channel_name]
