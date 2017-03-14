"""
This class substitutes a general interface that all analysis and statistics features must obey.
By convention, every class in the processing or stats package shall inherit after Reportable.
This allows to ensure that every analysis available in Pytnam integrates with the auto-reporting system.
No method in this class has a body, for the implementation may differ significantly across the subclasses.

The main framework for signal analysis in Pytnam is designed as follows:
each processing/statistics feature is implemented in its class, thus processing data always involves creating an object;
the objects provide analysis routines as a (hopefully) consistent API.
Every analysis object performs data serialization before the analysis, so as to make sure everything can be easily
recovered in case of any processing failure or an unnoticed mistake in parameters.
"""
from abc import ABC, abstractmethod
import pickle


class Reportable(ABC):
    """
    Variables storing the processing feature's important parameters:
    data - the data for the analysis;
    name - a string representing the name of the analysis method;
    parameters - a table containing the analysis' parameters. This may differ for each instance of a given class.
    While implementing, please make sure that ALL the parameters on the list are named.
    backup_addres - a variable used by the backup/restore functions;
    temporary - another variable for backup (please see the code of the _backup function).
    """
    name = ''
    parameters = []
    backup_address = None
    temporary = None

    @abstractmethod
    def get_representation(self):
        """
        This method is used by the reporting module.
        It should always return a list of arbitrary length, containing only strings and numbers representing
        parameters of the performed analysis.
        """
        pass

    def _backup(self, to_file=False, filename=''):
        """
        This method is designed for saving a copy of the signal before performing analysis.
        It uses pickle module for serialization; the serialized byte stream can be saved to file
        or temporarily stored by the Reportable object.
        :param to_file: boolean
        :param filename: String
        """
        if to_file:
            f = open(filename, 'b')
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
            f.close()
            self.backup_address = filename
        else:
            self.temporary = pickle.dumps(self.data, pickle.HIGHEST_PROTOCOL)

    def _restore(self):
        """
        Method for restoring the data in case the analysis fails.
        It presupposes that the data has been backed up using the _backup method, either to file or to object.
        """
        if self.backup_address is None:
            self.data = pickle.loads(self.temporary)
        else:
            source = open(self.backup_address, 'b')
            self.data = pickle.load(source)
            source.close()
