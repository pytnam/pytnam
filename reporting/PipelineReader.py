"""
A reader for XML files representing Pytnam analyses, enabling to reconstruct the whole analysis step-by-step.
It works on an XML pipeline representation as specified in the PipelineWriter class.
"""
from collections import defaultdict

from lxml import etree

from reporting.PipelineInfo import PipelineInfo

'''Created by rj as part of the Pytnam Project.'''


class PipelineReader:
    filename = ""

    def __init__(self, filename):
        """
        Constructor method.
        :param filename: String representing name of the file to read from.
        """
        # Check for format correctness:
        if not filename.endswith(".xml"):
            raise ValueError('Filename incorrect: the extension must be .xml!')
        else:
            self.filename = filename

    def read_pipeline(self):
        """
        This method reads a Pytnam Pipeline from an XML file. NOT FUNCTIONAL NOW
        Validation against Pytnam schema will be added soon.
        :return: defaultdict[String: Reportable] - dictionary with string keys and newly created analysis classes as values
        """
        # Initialize the result dictionary:
        result = defaultdict(lambda: None)

        # Parse:
        with open(self.filename, 'r') as file:
            # Get the whole XML tree:
            pipeline_tree = etree.parse(file)
            # Retrieve PipelineInfo object from the 0-th node:
            pipeline_info = pipeline_tree[0].getchildren()
            author_name = pipeline_info[0].get("author")
            pipeline_name = pipeline_info[1].get("pipeline")
            data_description = pipeline_info[2].get("data")
            analysis_date = pipeline_info[3].get("date")
            info = PipelineInfo(author_name, pipeline_name, data_description, analysis_date)
            result["info"] = info

            # Retreve pipeline body (sequence of analyses):
            pipeline_body = pipeline_tree[1]

            # TODO
