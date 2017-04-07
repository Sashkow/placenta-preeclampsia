from articles.models import Experiment, Microarray, Sample, SampleAttribute

from lxml import etree
import pickle 
#start
from bioservices.arrayexpress import ArrayExpress

from Bio.Affy import CelFile


from django.db.models import Q

import datetime


s = ArrayExpress()
# res = s.queryExperiments(
# keywords="pre-eclampsia+OR+preeclampsia+OR+pre-eclamptic+OR+preeclamptic",
#                              exptype="*array*",
#                              species="homo+sapiens")
# exclude = ["E-MTAB-3732"]
# children = res.getchildren()
# for exp in children:
#     if exp.find("accession").text in exclude:
#         children.remove(exp)

def get_expression_matrix():
    exps = ['E-GEOD-14722', 'E-GEOD-54618', 'E-GEOD-44711', 'E-GEOD-9984',
            'E-GEOD-4707', 'E-GEOD-12216', 'E-GEOD-30186', 'E-GEOD-10588', 
            'E-GEOD-13155', 'E-GEOD-24129', 'E-GEOD-12767', 'E-GEOD-60438',
            'E-GEOD-6573', 'E-GEOD-35574', 'E-GEOD-36083', 'E-GEOD-74341',
            'E-GEOD-73374', 'E-GEOD-47187', 'E-GEOD-37901', 'E-GEOD-15789',
            'E-GEOD-43942']
    for exp in exps:
        arrays = Experiment.objects.get(data__contains={"accession":exp}).microarrays.all()
        arrays = [str(array) for array in arrays]
        print(exp, arrays)
        res = s.retrieveExperiment(exp)
        exp = res.getchildren()[0]
        files = [x.getchildren() for x in exp.getchildren() if x.tag == "files"]
        for x in files[0]:
            print("     ", x.get("name"))
        


def get_sample_attributes_with_no_old_name():
    """
    12%
    """
    all_exps = Experiment.objects.all()
    exps = []
    for exp in all_exps:
        if not ('excluded' in exp.data):
            exps.append(exp)
    print("exps", len(exps))

    samples = Sample.objects.filter(experiment__in=exps)
    print("samples", len(samples))
    attributes = SampleAttribute.objects.filter(sample__in=samples)

    all_attributes_amnt = len(attributes)
    none_attrs = attributes.filter(old_name=None)
    none_samples_amnt = len(set(none_attrs.values_list('sample', flat=True)))
    print("None samples", none_samples_amnt)
    attributes_amnt = len(none_attrs)
    print(all_attributes_amnt, attributes_amnt, float(attributes_amnt)/all_attributes_amnt)


def get_studies_with_no_secondary_accession():
    exps = Experiment.objects.filter(~Q(data__contains='excluded'))
   
    geo_exps = exps.filter(data__contains='secondaryaccession')
    
    geo_years = [datetime.datetime.strptime(exp.data['releasedate'], "%Y-%m-%d").date() for exp in geo_exps]
    geo_avg_year = sum(geo_years)/len(geo_years)
    print(geo_years, geo_avg_year)
    geo_samples= Sample.objects.filter(experiment__in=geo_exps)
    geo_attrs = SampleAttribute.objects.filter(Q(sample__in=geo_samples) & ~Q(old_name=None))
    geo_attrs_per_sample = len(geo_attrs)/len(geo_samples)
    print("geo",len(geo_attrs), len(geo_samples), geo_attrs_per_sample)



    arr_exps = exps.filter(~Q(data__contains='secondaryaccession'))
    arr_years = [int(exp.data['releasedate'].split('-')[0]) for exp in arr_exps]
    arr_avg_year = sum(arr_years)/len(arr_years)
    print(arr_years, arr_avg_year)
    arr_samples= Sample.objects.filter(experiment__in=arr_exps)
    arr_attrs = SampleAttribute.objects.filter(Q(sample__in=arr_samples) & ~Q(old_name=None))
    arr_attrs_per_sample = len(arr_attrs)/len(arr_samples)
    print("arr:",len(arr_attrs), len(arr_samples), arr_attrs_per_sample)


def plot_annual_attrs_per_sample():
    exps = Experiment.objects.filter(~Q(data__contains='excluded'))
    exp_samples_attributes = {}
    for exp in exps:
        samples = exp.samples()
        attributes = SampleAttribute.objects.filter(Q(sample__in=samples) & ~Q(old_name=None))
        year = int(exp.data['releasedate'].split('-')[0])
        exp_samples_attributes[exp] = (year, len(samples), len(attributes))

    year_atributes_per_sample = {}

    for exp, ysa in exp_samples_attributes.items():
        if ysa[0] not in year_atributes_per_sample:
            year_atributes_per_sample[ysa[0]] = [ysa[1], ysa[2], 1]
        else:
            year_atributes_per_sample[ysa[0]][0]+=ysa[1]
            year_atributes_per_sample[ysa[0]][1]+=ysa[2]
            year_atributes_per_sample[ysa[0]][2]+=1

    for year in year_atributes_per_sample:
        atributes_per_sample = float(year_atributes_per_sample[year][1])/year_atributes_per_sample[year][0]
        samples_per_experiment = float(year_atributes_per_sample[year][0])/year_atributes_per_sample[year][2]
        year_atributes_per_sample[year] = [atributes_per_sample, samples_per_experiment, year_atributes_per_sample[year][2]]


    for year in sorted(year_atributes_per_sample):
        print(
                year,
                round(year_atributes_per_sample[year][0], 2),
                round(year_atributes_per_sample[year][1], 2),
                year_atributes_per_sample[year][2]
        )

def get_attrs_per_sample_in_experiment(experiment):
    samples = Sample.objects.filter(experiment=experiment)
    attributes = SampleAttribute.objects.filter(sample__in=samples)
    return float(len(attributes))/len(samples)

def plot_annual_attrs_per_sample2():
    exps = Experiment.objects.filter(~Q(data__contains='excluded'))
    exp_year_samples_per_attribute = {}
    for exp in exps:
        year = int(exp.data['releasedate'].split('-')[0])
        samples_per_attribute = get_attrs_per_sample_in_experiment(exp)
        exp_year_samples_per_attribute[exp] = (year, samples_per_attribute)

    year_atributes_per_sample = {}
    for exp, data in exp_year_samples_per_attribute.items():
        if data[0] not in year_atributes_per_sample:
            year_atributes_per_sample[data[0]] = [data[1], 1]
        else:
            year_atributes_per_sample[data[0]][0] += data[1]
            year_atributes_per_sample[data[0]][1] += 1
    

    for year, data in sorted(year_atributes_per_sample.items()):
        print(year, float(data[0])/data[1])






def get_experiment_attributes(experiment_id):
    """
    get attributes from experiment xml object

    returns dictionary attribute:value
    """
    
    exp = s.retrieveExperiment(experiment_id)
    # pass top level of xml 
    exp = exp.getchildren()[0]
    # exp = self.s.retrieveExperiment("E-GEOD-74341").getchildren()[0]
    exp_attrs = []
    exp_data = {}
    arrays_data = []  # list of dicts, one dict per microarray
    # add all attributes that are "leaves" of the xml tree
    for item in exp.getchildren():
      
        if item.text != None:
            exp_attrs.append(item.tag)
            exp_data[item.tag] = item.text
        else:
            if item.tag == 'arraydesign':
                array_data = {}            
                for array_attr in item.getchildren():
                    if array_attr.text != None:
                        array_data[array_attr.tag] = array_attr.text
                arrays_data.append(array_data)
    return exp_data, arrays_data


def get_experiment_samples_attributes(experiment_id):
    url ='xml/v3/experiments/'+experiment_id+'/samples'
    samples_xml = s.http_get(url, 'xml')

    samples_xml = s.easyXML(samples_xml)
    with open("samples_E-GEOD-74341.txt", "w") as text_file:
        print(samples_xml.prettify(), file=text_file)

    samples_xml = samples_xml.getchildren()
    samples = []
    for sample_xml in samples_xml:
        if sample_xml.tag == 'sample':
            sample = {}
            for characteristic in sample_xml.getchildren():
                if characteristic.tag == 'assay':
                    for item in characteristic.getchildren():
                        sample[item.tag] = item.text
                elif characteristic.tag == 'characteristic':
                    category_value = characteristic.getchildren()
                    if category_value[0].tag == 'category' and \
                       category_value[1].tag == 'value':
                        sample[category_value[0].text] = category_value[1].text
                    else:
                        print("Error while processing sample")
                elif characteristic.tag == 'source': 
                    # sometimes <name> tag which is under <assay>
                    # tag is absent or not unique 
                    first_tag = characteristic.getchildren()[0]
                    if first_tag.tag == 'name':
                        # print('Took name from sample xml <source> section',first_tag.tag,first_tag.text)
                        sample[first_tag.tag] = first_tag.text

            samples.append(sample)
    return samples



def exp_to_db(experiment_id):
    """
    retreive experiment data and add it to db
    """

    experiment, microarrays = get_experiment_attributes(experiment_id)
    samples = get_experiment_samples_attributes(experiment_id)
    experiment_obj = Experiment.add_or_replace(data=experiment)


    for microarray in microarrays:
        microarray_obj = Microarray.add_or_replace(data=microarray)
        if not(experiment_obj.microarrays.filter(id=microarray_obj.id).exists()):
            experiment_obj.microarrays.add(microarray_obj)
            experiment_obj.save()

    for sample in samples:  
        sample_obj = Sample.add_or_replace(experiment=experiment_obj,
                                           data=sample)
        sample_attributes = SampleAttribute.objects.filter(sample=sample_obj)
        for old_name, old_value in sample.items():

            if old_value == None or old_value == '':
                SampleAttribute.add_or_replace(sample_obj, old_name, '<empty>')
            else:
                SampleAttribute.add_or_replace(sample_obj, old_name, old_value)

        




def get_some():
    # get some experiment
    acc = "E-GEOD-74341"
    path ='xml/v3/experiments/E-GEOD-74341/samples'
    res = s.http_get(path,'xml')
    res = s.easyXML(res)



    # for item in lst:
    #     # print(item)
    #     s.retrieveFile(acc, item)

    with open("samples_E-GEOD-74341.txt", "w") as text_file:
        print(res.prettify(), file=text_file)

    # exp = res.getchildren()[0]
    # for thing in exp.findall("pre-eclampsia"):
    #   print("here", thing.text)

    # for x in res.getchildren():
    #     print(x.tag, x.text)

def get_all_unique_experiment_attributes_tag_names():
    acc = "E-GEOD-74341"
    exp = s.retrieveExperiment(acc).getchildren()[0]    

    for x in exp.getchildren():
        if x.text!=None:
            print(x.tag, x.text)



def get_preeclampsia_accession():
    """print all assenions of experiment with microarrays"""
#     new_res = s.queryAE(
# keywords="pre-eclampsia+OR+preeclampsia+OR+pre-eclamptic+OR+preeclamptic",
#                              exptype="*array*",
#                              species="homo+sapiens")



    res = ['E-GEOD-74341', 'E-GEOD-73377', 'E-GEOD-73375', 'E-GEOD-73374',
           'E-GEOD-60438', 'E-MTAB-3265', 'E-MTAB-3348',
           'E-MTAB-3309', 'E-GEOD-54400', 'E-GEOD-59274', 'E-GEOD-57767',
           'E-GEOD-48424', 'E-GEOD-57050', 'E-GEOD-54618', 'E-GEOD-49343',
           'E-GEOD-38747', 'E-GEOD-47187', 'E-GEOD-50783', 'E-GEOD-41681',
           'E-GEOD-44712', 'E-GEOD-44711', 'E-GEOD-44667', 'E-GEOD-43942',
           'E-GEOD-41336', 'E-GEOD-41331', 'E-GEOD-40182', 'E-GEOD-37901',
           'E-GEOD-36083', 'E-GEOD-35574', 'E-GEOD-31679', 'E-GEOD-30186',
           'E-GEOD-15789', 'E-GEOD-15787', 'E-GEOD-22526', 
              'E-GEOD-24129', 'E-GEOD-10588', 'E-GEOD-13155', 'E-TABM-682',
           'E-GEOD-14722', 'E-GEOD-12767', 'E-GEOD-13475', 'E-GEOD-12216',
           'E-GEOD-9984', 'E-GEOD-6573', 'E-GEOD-4100', 'E-GEOD-4707',
            'E-MEXP-1050']

            # cannot process 'E-GEOD-25906', 
            # 'E-MTAB-3732' irrelevant
            
    return res


def get_placenta_accession():
    # retu E-GEOD-59126

    return s.queryAE(
            keywords="placenta",
            exptype="*array*",
            species="homo+sapiens"
    )
    





def samples_total():
    samples_total = 0
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
keywords="pre-eclampsia+OR+preeclampsia+OR+pre-eclamptic+OR+preeclamptic+AND+NOT+E-MTAB-3732",
                             exptype="*array*",
                             species="homo+sapiens")

    # for exp in res.getchildren():
    #   for x in exp.getchildren():
    #       if x.tag == 'samples':
    #           if int(x.text) > 100:
    #               print(exp.find("accession").text,
    #                     exp.find("samples").text)


def get_all_sample_attribute_names():
    """get all sample attribute names from ArrayExpress db"""
    # dictionary: sample attribute name to experiment accession number
    attr_exp = {}

    res = [s.retrieveExperiment(accession) for accession in get_preeclampsia_accession()]

    for exp in res:
        for attr in exp.findall("sampleattribute"):
            # sample attribute name
            name = (attr.find("category").text).lower()
            # first sample attribute value as an example
            values = [x.text for x in attr.findall("value")]
            # experiment accession
            acc = exp.find("accession").text
            # experiment samples amnt 
            samples = exp.find("samples").text

            if name in attr_exp:
                attr_exp[name].append((acc, samples, values))
            else:
                attr_exp[name] = [(acc, samples, values)]

    with open("attr_names.txt", "w") as text_file:
        for attr in sorted(attr_exp):
            print(str(attr), file=text_file)
            for exp in attr_exp[attr]:
                print("     "+str(exp[0]+" ("+str(exp[1])+" samples)"), file=text_file)
                for value in exp[2]:
                    print("         "+str(value), file=text_file)


def print_exp_array_title(accession):
    exp = s.retrieveExperiment(accession)
    # pass top level of xml 
    exp = exp.getchildren()[0]
    for item in exp.getchildren():
        if item.tag == 'accession':
            print(item.text)
        if item.tag == 'arraydesign':            
            for array_attr in item.getchildren():
                if array_attr.tag == 'name':
                    print("     " + array_attr.text)


def read_cell_file(file_path):
    print(os.getwd())


def annual_attributes_per_sample_in_placenta():
    exps = get_placenta_accession() 
    exps = exps[exps.index('E-GEOD-59126')+1:]  

    exp_year_samples_per_attribute = {}
    for exp in exps:
        year = int(get_experiment_attributes(exp)[0]['releasedate'].split('-')[0])
        samples = get_experiment_samples_attributes(exp)
        samples_per_attribute = len(samples[0])
        exp_year_samples_per_attribute[exp] = (year, samples_per_attribute)
        print(exp, year, samples_per_attribute)

    year_atributes_per_sample = {}
    for exp, data in exp_year_samples_per_attribute.items():
        if data[0] not in year_atributes_per_sample:
            year_atributes_per_sample[data[0]] = [data[1], 1]
        else:
            year_atributes_per_sample[data[0]][0] += data[1]
            year_atributes_per_sample[data[0]][1] += 1
    

    for year, data in sorted(year_atributes_per_sample.items()):
        print(year, float(data[0])/data[1], data[1])






def main():
    get_experiment_samples_attributes('E-GEOD-14722')
    

if __name__ == '__main__':
    main()
