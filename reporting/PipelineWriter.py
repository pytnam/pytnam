"""
Tool for writing Pytnam pipelines to XML.
Each Pytnam Pipeline XML file has the following structure:
<pytnam_pipeline>
    <pipeline_info>
    ----4 nodes here: <author_name>, <pipeline_name>, <data_description>, <analysis_date>----
    </pipeline_info>
    <pipeline_body>
    ----arbitrary number of nodes here, each of the form:
        <analysis>
        ----arbitrary no. of nodes here, including <analysis_name> and <parameters> node with children.----
        <analysis>
    ----
    </pipeline_body
</pytnam_pipeline>

Every analysis/stats class implementing Reportable should be able to return its XML node representation.
"""
from lxml import etree

'''Created by rj as part of the Pytnam Project.'''


class PipelineWriter:
    pipeline_as_list = None

    def __init__(self, pipeline_as_list):
        """
        Constructor method.
        :param pipeline_as_list: ordinary python list as in AppContext.current_pipeline,
        containing lxml Element objects representing analysis steps.
        The 0-th element of the list is assumed to be an XML representation of a PipelineInfo object (pipeline info)
        All the other elements of the list are assumed to be analysis step XML representations.
        """
        self.pipeline_as_list = pipeline_as_list

    def write_to_file(self, filename):
        """
        Writes the pipeline to XML file.
        :param filename: name of the destination XML file; must end with '.xml'
        """
        # Build a complete XML tree representation of the pipeline (analysis):
        root = etree.Element("pytnam_pipeline")
        root.append(self.pipeline_as_list[0])
        body = etree.Element("pipeline_body")
        for i in range(1, len(self.pipeline_as_list)):
            elem = self.pipeline_as_list[i]
            body.append(elem)
        root.append(body)

        # Write the XML tree to file:
        if not filename.endswith(".xml"):
            raise ValueError('Filename incorrect: the extension must be .xml!')
        else:
            with open(filename, 'w') as file:
                root.write(file, encoding='UTF-8', pretty_print=True)
            file.close()
