"""
This class substitutes a general interface that all analysis and statistics features must obey.
By convention, every class in the processing or stats package should inherit after Reportable.
This is to ensure that every analysis available in Pytnam integrates with the auto-reporting system.

The main framework for signal analysis in Pytnam is designed as follows:
each processing/statistics feature is implemented in its class, thus processing data always involves creating an object;
the objects provide analysis routines as a (hopefully) consistent API.
Every analysis object can be told to performs data serialization before the analysis, so as to make sure everything can be easily
recovered in case of any processing failure or an unnoticed mistake in parameters.

The common method for all Reportable analyses is return_as_node(), which returns an XML representation
of the object. These XML representations are used for automatic writing and reading sequences of Pytnam analyses.
Such sequences are called Pytnam Pipelines (after the R language pipeline-style analysis scripts).
Each user session with Pytnam involves creating at least one pipeline.
Writing pipelines to XML makes it possible to recover any sequence of Pytnam analyses on any computer with Pytnam installed,
without writing and running any Python scripts. Thus it is a feature aimed mostly at non-programmers,
who usually make for the majority of EEG processing tolbox users.
"""
from abc import ABC, abstractmethod
import pickle


class Reportable(ABC):
    """
    Variables storing the processing feature's important parameters:
    data - the data for the analysis;
    analysis_name - a string representing the name of the analysis method;
    parameters - a table containing the analysis' parameters. This may differ for each instance of a given class.
    While implementing, please make sure that ALL the parameters on the list are named.
    backup_address - a variable used by the backup/restore functions;
    temporary - another variable for backup (please see the code of the _backup function).
    """
    analysis_name = ""
    parameters = []
    backup_address = None
    temporary = None

    @abstractmethod
    def return_as_node(self):
        """
        This method is used by the reporting module.
        It should always return an lxml Element object - XML node, usually with children, ready for
        being processed by a PipelineWriter object.
        """
        pass

    def _backup(self, filename, to_file=False):
        """
        Internal method designed for saving a copy of the signal before performing analysis.
        Pickle module is used for fast serialization; the serialized byte stream can be saved to file
        or temporarily stored by the Reportable object.
        :param to_file: boolean
        :param filename: String
        """
        if to_file:
            f = open(filename, "b")
            pickle.dump(self.data, f, pickle.HIGHEST_PROTOCOL)
            f.close()
            self.backup_address = filename
        else:
            self.temporary = pickle.dumps(self.data, pickle.HIGHEST_PROTOCOL)

    def _restore(self):
        """
        Internal method for restoring the data in case the analysis fails.
        It presupposes that the data has been backed up using the _backup method, either to file or to object.
        """
        if self.backup_address is None:
            self.data = pickle.loads(self.temporary)
        else:
            source = open(self.backup_address, "b")
            self.data = pickle.load(source)
            source.close()
