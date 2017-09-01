from articles.getdata import *

from bioservices.arrayexpress import ArrayExpress

import pickle

from django.test import TestCase
import unittest

from articles.models import Experiment

# from sets import Set

import os
os.chdir(os.path.dirname(__file__))

class TestGetData(TestCase):

    def setUp(self):
        self.s = ArrayExpress()
        self.acc_lst = []
        # with open("acc_lst.testdata", "wb") as afile:
        #     pickle.dump(self.acc_lst, afile)
        
        with open("acc_lst.testdata", "rb") as afile:
            self.acc_lst = pickle.load(afile)

    def tearDown(self):
        self.s.session.close()

   

    def test_get_experiment_attributes(self): 
        """

        """   
        exp_data = get_experiment_attributes("E-GEOD-74341")

        self.assertTrue(isinstance(exp_data, tuple))
        self.assertTrue(len(exp_data), 2)
        print(exp_data[0], exp_data[1])
        self.assertTrue(isinstance(exp_data[0],dict))
        self.assertTrue(isinstance(exp_data[1],dict))

        experiment_must_have = ['species', 'id', 'accession', 'secondaryaccession',
         'name', 'experimenttype', 'releasedate', 'lastupdatedate',
        'samples', 'assays', 'organism']

        self.assertTrue(set(experiment_must_have).
                            issubset(set(exp_data[0].keys())))


    
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
        exp_in_db = Experiment.objects.filter(data__contains={'accession':exp_accession})
        self.assertEquals(len(exp_in_db), 1)



# if __name__ == '__main__':
    # unittest.main()
