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


class Reportable:

    """
    Variables storing the processing feature's important parameters:
    name - a string representing the name of the analysis method;
    parameters - a table containing the analysis' parameters. This may differ for each instance of a given class.
    While implementing, please make sure that ALL the parameters on the list are named.
    """
    name = ''
    parameters = []

    @staticmethod
    def get_representation():
        """
        This method is used by the reporting module.
        It should always return a list of arbitrary length, containing only strings and numbers representing
        parameters of the performed analysis.
        """
        pass
