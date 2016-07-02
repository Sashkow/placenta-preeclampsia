from lxml import etree
#start
from bioservices.arrayexpress import ArrayExpress
s = ArrayExpress()

def get_some():
	# get some experiment
	acc = "E-GEOD-74341"
	# res = s.retrieveExperiment(acc)
	lst = s.retrieveFilesFromExperiment(acc)
	for item in lst:
		print(item)
		s.retrieveFile(acc, item)

	# with open("Output.txt", "w") as text_file:
	# 	print(res.prettify(), file=text_file)

	# exp = res.getchildren()[0]
	# for thing in exp.findall("pre-eclampsia"):
	# 	print("here", thing.text)

	# for x in exp.getchildren():
		# print(x.tag, x.text)



def print_accen():
	"""print all assenions of experiment with microarrays"""
	res = s.queryAE(
keywords="pre-eclampsia+OR+preeclampsia+OR+pre-eclamptic+OR+preeclamptic",
							 exptype="*array*",
							 species="homo+sapiens")
	res = ['E-GEOD-74341', 'E-GEOD-73377', 'E-GEOD-73375', 'E-GEOD-73374',
		   'E-GEOD-60438', 'E-MTAB-3732', 'E-MTAB-3265', 'E-MTAB-3348',
		   'E-MTAB-3309', 'E-GEOD-54400', 'E-GEOD-59274', 'E-GEOD-57767',
		   'E-GEOD-48424', 'E-GEOD-57050', 'E-GEOD-54618', 'E-GEOD-49343',
		   'E-GEOD-38747', 'E-GEOD-47187', 'E-GEOD-50783', 'E-GEOD-41681',
		   'E-GEOD-44712', 'E-GEOD-44711', 'E-GEOD-44667', 'E-GEOD-43942',
		   'E-GEOD-41336', 'E-GEOD-41331', 'E-GEOD-40182', 'E-GEOD-37901',
		   'E-GEOD-36083', 'E-GEOD-35574', 'E-GEOD-31679', 'E-GEOD-30186',
		   'E-GEOD-15789', 'E-GEOD-15787', 'E-GEOD-22526', 'E-GEOD-25906', 
		   'E-GEOD-24129', 'E-GEOD-10588', 'E-GEOD-13155', 'E-TABM-682',
		   'E-GEOD-14722', 'E-GEOD-12767', 'E-GEOD-13475', 'E-GEOD-12216',
		   'E-GEOD-9984', 'E-GEOD-6573', 'E-GEOD-4100', 'E-GEOD-4707',
		    'E-MEXP-1050']

	print(len(res))

	verified_res = []



def samples_total():
	samples_total = 0
	res = s.queryExperiments(
keywords="pre-eclampsia+OR+preeclampsia+OR+pre-eclamptic+OR+preeclamptic",
							 exptype="*array*",
							 species="homo+sapiens")
	for exp in res.getchildren():
		is_tag=False
		for x in exp.getchildren():
			if x.tag == 'samples' and int(x.text) < 100:
				print(int(x.text))
				samples_total+=int(x.text)
				is_tag = True
		if is_tag==False:
			print("no tag")
	print(samples_total) 

def get_exps_with_lots_samples():
	acc = []
	res = s.queryExperiments(
keywords="pre-eclampsia+OR+preeclampsia+OR+pre-eclamptic+OR+preeclamptic",
							 exptype="*array*",
							 species="homo+sapiens")
	for exp in res.getchildren():
		for x in exp.getchildren():
			if x.tag == 'samples':
				if int(x.text) > 100:
					print(exp.find("accession").text,
						  exp.find("samples").text)

def get_all_sample_attribute_names():
	"""get all sample attribute names from ArrayExpress db"""
	# dictionary: sample attribute name to experiment accession number
	attr_exp = {}
	res = s.queryExperiments(
keywords="pre-eclampsia+OR+preeclampsia+OR+pre-eclamptic+OR+preeclamptic",
							 exptype="*array*",
							 species="homo+sapiens")

	for exp in res.getchildren():
		for attr in exp.findall("sampleattribute"):
			# sample attribute name
			name = (attr.find("category").text).lower()
			# first sample attribute value as an example
			value = attr.find("value").text
			# experiment accession
			acc = exp.find("accession").text
			if name in attr_exp:
				attr_exp[name].append(value)
			else:
				attr_exp[name] = [value]

	with open("attr_names.txt", "w") as text_file:
		for key in sorted(attr_exp):
			print(key, attr_exp[key], file=text_file)

	


			


get_all_sample_attribute_names()