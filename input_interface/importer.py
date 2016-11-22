# -*- coding: utf-8 -*-
# This module was created by Wiktor Rorot <wiktor.rorot@gmail.com> as a part of pytnam project (https://github.com/pytnam/pytnam) and is licensed under GNU GPL.

import numpy as np
from collections import defaultdict

def importer(header, signal):

    """
    Changes format of data.

    Takes as an argument dict representing a header (of e.g. edf file) and dict representing the signal.

    RETURNS:
        data (defaultdict((np.array, np.array))): a dictionnary where:
            key: label, value: tuple of which 1st element is numpy.array of timestamps, and 2nd element  is numpy.array of sample values at those timestamps
            key 'info', value dictionnary with following keys:
                patient_id (string): local patient id
                frequencies (dictionnary - string: float): key: label (an element of labels), value: frequency of the signal;
                stardate (string): startdate of the recording (dd.mm.yy) (for more info see edf and edf+ specs at: http://www.edfplus.info/specs/index.html)
                starttime (string): starttime of the recording (hh.mm.ss)
                physical_dim (dictionnary - string: string): key: label (an element of labels), value: physical dimension; 
                prefiltering (dictionnary - string: string): key: label (an element of labels), value: signal's prefiltering;

    TODO: discuss whether the proposed format is okay (meaning the format of the signal) - it lets us have different frequencies in different signals; discuss whether the 'info' section has enough data
    """
    data = defaultdict(lambda: (np.array, np.array))

    for label in signal.keys():
        freq = header['frequency'][label]
        time = [(0 + (x/freq)) for x in range(header['num_records']*header['num_samples'][label])]
        data[label] = (np.array(time), np.array(signal[label]))

    data['info'] = defaultdict(lambda: None)

    data['info']['frequencies'] = header['frequency']
    data['info']['patient_id'] = header['patient_id']
    data['info']['startdate'] = header['startdate']
    data['info']['starttime'] = header['starttime']
    data['info']['physical_dim'] = header['physical_dim']
    data['info']['prefiltering'] = header['prefiltering']

    return data
