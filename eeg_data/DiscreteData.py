# -*- coding: utf-8 -*-
from collections import defaultdict
from eeg_data.Epoch import Epoch
import numpy as np



class DiscreteData:

    """
    This class represents the data after epoch extraction. 
    Each object of this class holds epochs extracted basing on exactly one event. 
    Epochs are kept in a np.array (@epochs) of respective Epoch objects, position in the array responds to the event id.
    """

    def __init__(self, data, event_type_id, start=-1000, end=2000):

        try:
            events_exemplars_times = data.data["info"]["events"][event_type_id]

            epochs = []

            channels = data.data["signal"].keys()  # TODO: docelowo parametryzowalne

            for event in events_exemplars_times:
                epochs.append(Epoch(data, channels, event, start, end))

            self.epochs = np.array(epochs)

        except TypeError:
            pass

    def average_epochs(self, channels):

        """This method returns an arithmetic average value of brain activation over all epochs."""

        averaged = defaultdict(lambda: np.array([[],[]]))

        for channel in channels:
            average_channel = []
            for index in range(self.epochs[0].data[channel][1]):
                average_index = 0
                for epoch in self.epochs:
                    average_index += epoch.data[channel][1][index]
                average_channel.append((average_index/len(self.epochs)))
            averaged[channel] = np.array([self.epochs[0].data[channel][0], np.array(average_channel)])

        return averaged
