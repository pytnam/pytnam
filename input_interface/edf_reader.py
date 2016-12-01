# -*- coding: utf-8 -*-
# This module was created by Wiktor Rorot <wiktor.rorot@gmail.com> as a part of pytnam project (https://github.com/pytnam/pytnam) and is licensed under GNU GPL.

from collections import defaultdict

def read_edf(path):


    """ 
    The function edf_reader serves to read .edf files.

    ARGUMENTS:
        path (string): a path to the .edf file

    RETURNS:

        header (defaultdict(lambda: None)): a dictionnary containg general information about the recording, from the .edf file's header.
            It conveys following information:
                version (string): version of the .edf data format (always 0)
                patient_id (string): local patient id
                rec_id (string): local recording id
                stardate (string): startdate of the recording (dd.mm.yy) (for more info see edf and edf+ specs at: http://www.edfplus.info/specs/index.html)
                starttime (string): starttime of the recording (hh.mm.ss)
                header_bytes (integer): size of the header (in bytes)
                reserved_general (string): reserved field of 44 characters; since introduction of edf+ it conveys the information about the continuity of the record (see edf+ specs) 
                num_records (integer): the recording in the edf format is broken into records of not less than 1s and no more than 61440 bytes (see specs);
                record_duration (float): duration of one record; usually an integer >= 1;
                ns (integer): number of signals in the recording (e.g. in EEG - number of channels)
                labels (list of strings): labels of signals;
                transducer (dictionnary - string: string): key: label (an element of labels), value: transducer type; 
                physical_dim (dictionnary - string: string): key: label (an element of labels), value: physical dimension; 
                physical_min (dictionnary - string: float): key: label (an element of labels), value: physical minimum;
                physical_max (dictionnary - string: float): key: label (an element of labels), value: physical maximum;
                digital_min (dictionnary - string: float): key: label (an element of labels), value: digital minimum;
                digital_max (dictionnary - string: float): key: label (an element of labels), value: digital maximum;
                prefiltering (dictionnary - string: string): key: label (an element of labels), value: signal's prefiltering;
                num_samples (dictionnary - string: integer): key: label (an element of labels), value: number of samples in each record of the signal;
                reserved_signal (dictionnary - string: string): key: label (an element of labels), value: a reserved field of 32 characters;
                frequency (dictionnary - string: float): key: label (an element of labels), value: frequency of the signal;

        signal (defaultdict(list)): a dictionnary of the following format: key: label, value: list of samples;

            NOTE: this version ignores the differences between edf and edf+, what makes her more suitable for edf, rather than edf+ files

            TODO: signal is represented in the digital or physical form? does it have to be transformed?
    """

    data_file = open(path, 'rb')
    data = data_file.read()
    position, header = read_header(data)
    header['frequency'] = defaultdict(float)
    for label in header['labels']:
        header['frequency'][label] = header['num_samples'][label]/header['record_duration']
    position, signal = read_signal(data, position, header)
    return header, signal

def read_header(data):

    def static_header(data, header):

    # this part of code reads the part of the header with the general information about the record
        header['version'] = data[0:7].strip().decode('ascii')
        header['patient_id'] = data[7:88].strip().decode('ascii')
        header['rec_id'] = data[88:168].strip().decode('ascii')
        header['startdate'] = data[168:176].strip().decode('ascii')
        header['starttime'] = data[176:184].strip().decode('ascii')
        header['header_bytes'] = int(data[184:192].strip().decode('ascii'))
        header['reserved_general'] =  data[192:236].strip().decode('ascii')
        header['num_records'] = int(data[236:244].strip().decode('ascii'))
        header['record_duration'] = float(data[244:252].strip().decode('ascii'))
        header['ns'] = int(data[252:256].strip().decode('ascii'))
        return header

    def dynamic_header(data, header):

    # this part reads the part of the header with the information about each signal
        ns = header['ns']
        pos = 256
        labels = []

        for i in range(ns):
            labels.append(data[pos:pos+16].strip().decode('ascii'))
            pos += 16
        header['labels'] = labels

        header['transducer'] = defaultdict(str)
        header['physical_dim'] = defaultdict(str)
        header['physical_min'] = defaultdict(int)
        header['physical_max'] = defaultdict(float)
        header['digital_min'] = defaultdict(float)
        header['digital_max'] = defaultdict(float)
        header['prefiltering'] = defaultdict(str)
        header['num_samples'] = defaultdict(int)
        header['reserved_signal'] = defaultdict(str)
        
        for label in header['labels']:
            header['transducer'][label] = data[pos : pos+80].strip().decode('ascii')
            pos += 80
        for label in header['labels']:
            header['physical_dim'][label] = data[pos : pos+8].strip().decode('ascii')
            pos += 8
        for label in header['labels']:
            header['physical_min'][label] = float(data[pos : pos+8].strip().decode('ascii'))
            pos += 8
        for label in header['labels']:
            header['physical_max'][label] = float(data[pos : pos+8].strip().decode('ascii'))
            pos += 8
        for label in header['labels']:
            header['digital_min'][label] = float(data[pos : pos+8].strip().decode('ascii'))
            pos += 8
        for label in header['labels']:
            header['digital_max'][label] = float(data[pos : pos+8].strip().decode('ascii'))
            pos += 8
        for label in header['labels']:
            header['prefiltering'][label] = data[pos : pos+80].strip().decode('ascii')
            pos += 80
        for label in header['labels']:
            header['num_samples'][label] = int(data[pos : pos+8].strip().decode('ascii'))
            pos += 8
        for label in header['labels']:
            header['reserved_signal'][label] = data[pos : pos+32].strip().decode('ascii')
            pos += 32
        
        return pos, header

    header = defaultdict(lambda: None)
    header = static_header(data, header)
    pos, header = dynamic_header(data, header)    

    return pos, header


def read_signal(data, pos, header):

    signal = defaultdict(list)
    num_records = header['num_records']

    for i in range(num_records):
        for label in header['labels']:
            num_samples = header['num_samples'][label]
            for i in range(num_samples):
                signal[label].append(int.from_bytes(list(data[pos], data[pos+1], data[pos+2]), byteorder='little', signed=True))
                pos += 2

    return pos, signal 