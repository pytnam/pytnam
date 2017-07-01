"""
This is a class to be used by the application control logic.
Every time a new analysis pipeline is created (i.e., usually, once per session)), AppContext is adjusted to contain:
a PipelineInfo object with info about the currently performed sequence of analyses,
a list of lxml Element objects representing subsequent steps of the analysis (pipeline nodes).
Pipeline nodes/analysis steps can be added by using the add_pipeline_node method.
"""
'''Created by rj as part of the Pytnam Project.'''


class AppContext:
    current_pipeline = None
    pipeline_record = []

    def __init__(self, pipeline_info):
        """
        Constructor method.
        :param pipeline_info: PipelineInfo object containing data about the currently active Pytnam Pipeline.
        """
        self.current_pipeline = pipeline_info

    def add_pipeline_node(self, node):
        """
        This method adds a new analysis step to a list of such steps stored by the currently active AppContext bject.
        :param node: lxml Element object as created by return_as_node method from the Reportable interface.
        """
        self.pipeline_record.append(node)
