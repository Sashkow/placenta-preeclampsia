from django.test import TestCase

from django.test import Client


class TestExperimentAutoFillButton(TestCase):
	"""
	TestCase for custom AutoFill button in Experiment admin interface

	On button hit 
		if accession field exists and has value
			download experiment data as xml from arrayexpress site
			fill Expeiment form with data
			fill Microarray inline form with data; more than one Microarray instance possible

	AutoFill button is added by overriding admin/change_form.html template
	AutoFill button is handled by overriding response_change method in ExperimentAdmin ModelForm
	"""
	def setUp(self):
		self.c = Client()

	def test_autofill_button_exists(self):
		"""
		test AutoFill button exists in admin interface for Experiment 
		"""
		response = self.c.get('/admin/articles/experiment/add/')
		
	def test_

	
