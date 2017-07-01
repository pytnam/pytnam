"""
A simple info-holder class used for pipeline writing/reading.
It provides info about the Pytnam pipeline it is associated with.
An instance of this class should be created once for each analysis pipeline created by the user.
The data in String format should be provided by user through UI methods (an initial prompt, etc.).
The XML representation of a PipelineInfo object forms the first node in an XML pipeline document as created by PipelineWriter.
"""
import datetime
from lxml import etree

'''Created by rj as part of the Pytnam Project'''


class PipelineInfo:
    author_name = ""
    pipeline_name = ""
    data_description = ""
    analysis_date = None

    def __init__(self, author_name, pipeline_name, data_description, analysis_date = datetime.datetime.today()):
        """
        Constructor method. All parameters are intended to be provided by the user.
        :param author_name: the name of the analysis' author; arbitrary String
        :param pipeline_name: the name of the Pytnam pipeline the current PipelineInfo instance
        is associated with; arbitrary String
        :param data_description: a possibly short description of the dataset analysed in the pipeline; arbitrary String
        :param: analysis_date: date & time of the pipeline creation; set automatically as Python's today().
        """
        self.author_name = author_name
        self.pipeline_name = pipeline_name
        self.data_description = data_description
        self.analysis_date = analysis_date

    def return_as_node(self):
        """
        Standard method used by PipelineWriter objects.
        :return: lxml Element node, structured as follows:
        <pipeline_info>
            <author_name author="name here"/>
            <pipeline_name pipeline="sth here"/>
            <data_description data="descr here"/>
            <analysis_date date="datestring here"/>
        </pipeline_info>
        """
        node = etree.Element("pipeline_info")
        an = etree.SubElement(node, "author_name", author=self.author_name)
        pn = etree.SubElement(node, "pipeline_name", pipeline=self.pipeline_name)
        dd = etree.SubElement(node, "data_description", data=self.data_description)
        ad = etree.SubElement(node, "analysis_date", date=str(self.analysis_date))
        return node