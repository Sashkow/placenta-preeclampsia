import pickle

from django.test import TestCase
from django.test import Client


from articles.models import Experiment

# from sets import Set

from articles.models import ShowModel, UnificatedSamplesAttributeName

import os
# os.chdir(os.path.dirname(__file__))

class TestShowModel(TestCase):
    def setUp(self):
        self.c = Client()

    def test_to_show_in_showmodel(self):
        # sh = ShowModel()
        # self.assertTrue(hasattr(sh,'to_show'))
        us = UnificatedSamplesAttributeName()
        us.name = 'hi'
        self.assertTrue(hasattr(us,'_show'))
        self.assertTrue(hasattr(us,'to_show'))

        print(us._show())
