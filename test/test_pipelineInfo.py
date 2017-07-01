'''
Created by rj as part of the Pytnam Project
'''
from unittest import TestCase

import datetime

import lxml

from reporting.PipelineInfo import PipelineInfo


class TestPipelineInfo(TestCase):

    def test_init(self):
        author_name = "Ludwig Wittgenstein"
        pipeline_name = "Mock pipeline for testing purposes"
        data_description = "To show the fly the way out of the fly bottle"
        inf = PipelineInfo(author_name, pipeline_name, data_description)

        self.assertIsInstance(inf, PipelineInfo)
        self.assertEqual(inf.author_name, author_name)
        self.assertEqual(inf.pipeline_name, pipeline_name)
        self.assertEqual(inf.data_description, data_description)
        self.assertIsInstance(inf.analysis_date, datetime.datetime)

    def test_return_as_node(self):
        author_name = "Ludwig Wittgenstein"
        pipeline_name = "Mock pipeline for testing purposes"
        data_description = "To show the fly the way out of the fly bottle"
        inf = PipelineInfo(author_name, pipeline_name, data_description)

        test_node = inf.return_as_node()
        self.assertIsInstance(test_node, lxml.Element)