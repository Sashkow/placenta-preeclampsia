import pickle

from django.test import TestCase
from django.test import Client


from articles.models import Experiment

# from sets import Set

from articles.models import *

import os
# os.chdir(os.path.dirname(__file__))

class TestShowModel(TestCase):
    def setUp(self):
        self.c = Client()

    def test_to_show_in_showmodel(self):
        # sh = ShowModel()
        # self.assertTrue(hasattr(sh,'to_show'))
        us = StandardName()
        us.name = 'hi'
        self.assertTrue(hasattr(us,'_show'))
        self.assertTrue(hasattr(us,'to_show'))

        print(us._show())


calss TestSample(TestSample):
    def setUp(self):
        self.c = Client()

    def test_add_or_replace(self):
        e = Experiment.objects.create(data={'test':'test'})
        s1 = Sample.objects.create(experiment=e)

        un = SamplesAttributeNameInExperiment.objects.create(old_name='name')

        sa_name = SampleAttribute.objects.create(sample=s1, unificated_name=un)

        data = {'name':'test',}
        s2 = Sample.objects.test_add_or_replace(e, data)
        self.assertEqual(s1, s2)

        data_
        s3 = Sample.objects.test_add_or_replace(e, data)





