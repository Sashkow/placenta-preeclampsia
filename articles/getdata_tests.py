from articles.getdata import *

from bioservices.arrayexpress import ArrayExpress

import pickle

from django.test import TestCase
import unittest

from models import Experiment

# from sets import Set

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.s = ArrayExpress()
        self.acc_lst = []
        # with open("acc_lst.testdata", "wb") as afile:
        #     pickle.dump(self.acc_lst, afile)
        with open("acc_lst.testdata", "rb") as afile:
            self.acc_lst = pickle.load(afile)

    def tearDown(self):
        self.s.session.close()

    def test_get_experiment_acc_lst(self):
        res = get_experiment_acc_lst()
        self.assertTrue(res)
        for item in res:
            self.assertTrue(isinstance(item, str))

    def test_get_experiment_attributes(self): 
        """

        """   
        exp = self.s.retrieveExperiment("E-GEOD-74341")
        exp_attrs = get_experiment_attributes(exp)

        self.assertTrue(isinstance(exp_attrs, dict))

        must_have = ['species', 'id', 'accession', 'secondaryaccession',
         'name', 'experimenttype', 'releasedate', 'lastupdatedate',
        'samples', 'assays', 'organism']

        self.assertTrue(set(must_have) in set(exp_attrs.keys))

    
    # def test_split(self):
    #     s = 'helelo world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)


class GetExperimentDataTestCase(TestCase):

    def test_exp_to_db_runs(self):
        exp_accession = "E-GEOD-74341"
        exp_to_db(exp_accession)
        self.assertEquals(
            len(Experiment.objects.all(data__accession=exp_accession), 1))




if __name__ == '__main__':
    unittest.main()
