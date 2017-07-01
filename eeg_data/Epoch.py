# -*- coding: utf-8 -*-
from collections import defaultdict
import numpy as np


class Epoch:
    """
    Holds a representation of a single epoch.
    
    :ivar data is a dictionary of channels, each channel is a np.array with a time representations to the event,
    :ivar id is the time of occurrence of event.
    """

    def __init__(self, imported_data, channels, event, start, end):

        data = defaultdict(lambda: np.array([[], []]))

        for channel_name in channels:
            data[channel_name] = np.array(imported_data["signal"][channel_name][0][event + start:event + end + 1],
                                          imported_data["signal"][channel_name][1][event + start:event + end + 1])

        self.data = data
        self.id = event  # może być redundantne
