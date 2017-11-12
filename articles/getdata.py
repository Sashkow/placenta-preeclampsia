import os
from articles.models import Experiment, Microarray, Sample, SampleAttribute, StandardName, StandardValue

from lxml import etree
import pickle 
#start
from bioservices.arrayexpress import ArrayExpress

from Bio.Affy import CelFile


from django.db.models import Q

import datetime
import numpy

import requests

import glob
import collections

import csv



def generate_pdata(source, secondaryaccession, destination):
    """
    source -- folder with series files
    destination -- output pdata folder
    """
    captions = 'SampleAccessionNumber   DataSetAccesionNumber'
    files = os.listdir(source)
    for f in files:
        print(f)

s = ArrayExpress()
# res = s.queryExperiments(
# keywords="pre-eclampsia+OR+preeclampsia+OR+pre-eclamptic+OR+preeclamptic",
#                              exptype="*array*",
#                              species="homo+sapiens")
# exclude = ["E-MTAB-3732"]
# children = res.getchildren()
# for exp in children:
#     if exp.find("accession").text in exclude:
#     
# children.remove(exp)
# from past.translation import install_hooks, remove_hooks
# install_hooks(['pyaffy'])
# import pyaffy
# remove_hooks()


def cel_to_expression_matrix():
    cdf = os.getcwd()+'/downloads/E-GEOD-6573.raw.1/HG-U133_Plus_2.cdf'
    celpath = os.getcwd()+'/downloads/E-GEOD-6573.raw.1'
    path_pattern = os.path.join(celpath, '*.gz')
    files = glob.glob(path_pattern, recursive=True)
    print(files)

    cels = {fpath.split('/')[-1]:fpath for fpath in files}
    cels = collections.OrderedDict(cels)

    print(pyaffy.rma(cdf, cels))

    
def download_exp_file(experiment, filename):
    downloadsfolder = 'downloads'
    url = 'https://www.ebi.ac.uk/arrayexpress/files/' + experiment + "/" + filename
    print(url)
    local_filename = url.split('/')[-1]
    r = requests.get(url, stream=True)
    f = open(os.path.join(os.getcwd(),downloadsfolder,local_filename), 'wb')
    i = 0
    for chunk in r.iter_content(chunk_size=1024*1024): 
        if chunk: # filter out keep-alive new chunks
            print(i)
            f.write(chunk)
            i+=1

    f.close()
    return

def print_exp_accession_microarrays_platform_name():
    # exps = ['E-GEOD-14722', 'E-GEOD-54618', 'E-GEOD-44711', 'E-GEOD-9984',
    #         'E-GEOD-4707', 'E-GEOD-12216', 'E-GEOD-30186', 'E-GEOD-10588', 
    #         'E-GEOD-13155', 'E-GEOD-24129', 'E-GEOD-12767', 'E-GEOD-60438',
    #         'E-GEOD-6573', 'E-GEOD-35574', 'E-GEOD-36083', 'E-GEOD-74341',
    #         'E-GEOD-73374', 'E-GEOD-47187', 'E-GEOD-37901', 'E-GEOD-15789',
    #         'E-GEOD-43942']
    exps = ['E-GEOD-74341', 'E-GEOD-48424', 'E-GEOD-43942', 'E-GEOD-15789', 'E-GEOD-10588', 'E-GEOD-13155', 'E-GEOD-12216'] 
    i = 1
    for exp in exps:
        experiment = Experiment.objects.get(data__contains={"accession":exp})
        arrays = experiment.microarrays.all()
        for array in arrays:
            name = array.data['name']
            short = array.data['short'] if 'short' in array.data else ''
            print('\t'.join([str(i),experiment.data['accession'], experiment.data['secondaryaccession'], name, short]))
            i += 1




def get_expression_matrix():
    exps = ['E-GEOD-14722', 'E-GEOD-54618', 'E-GEOD-44711', 'E-GEOD-9984',
            'E-GEOD-4707', 'E-GEOD-12216', 'E-GEOD-30186', 'E-GEOD-10588', 
            'E-GEOD-13155', 'E-GEOD-24129', 'E-GEOD-12767', 'E-GEOD-60438',
            'E-GEOD-6573', 'E-GEOD-35574', 'E-GEOD-36083', 'E-GEOD-74341',
            'E-GEOD-73374', 'E-GEOD-47187', 'E-GEOD-37901', 'E-GEOD-15789',
            'E-GEOD-43942']
    # lumi
    # exps = ['E-GEOD-54618', 'E-GEOD-44711', 'E-GEOD-4707', 'E-GEOD-30186', 'E-GEOD-60438', 'E-GEOD-35574']
    noraw = []
    for exp in exps:
        arrays = Experiment.objects.get(data__contains={"accession":exp}).microarrays.all()
        arrays = [str(array) for array in arrays]
        print(exp, arrays)
        res = s.retrieveExperiment(exp)
        experiment = res.getchildren()[0]
        files = [x.getchildren() for x in experiment.getchildren() if x.tag == "files"]
        hasraw = False
        
        for x in files[0]:
            filename = x.get('name')
            print('     ', filename)
    
            if 'processed' in filename:
                print('   ', filename)
                hasraw = True
                download_exp_file(exp, filename)
        # if not hasraw:
        #     noraw.append(exp)
        #     print("!", exp)

    # print(noraw)


def get_sample_attributes_with_no_old_name():
    """
    12%
    """

    all_exps = Experiment.objects.all()
    exps = []
    for exp in all_exps:
        if not ('excluded' in exp.data):
            exps.append(exp)

    samples = Sample.objects.filter(experiment__in=exps)
    print("samples", len(samples))
    attributes = SampleAttribute.objects.filter(sample__in=samples)

    print("exps", len(exps))
    exp_data = {}
    for exp in exps:
        exp_samples = samples.filter(experiment=exp)
        exp_attributes = attributes.filter(sample__in=exp_samples)
        exp_data[str(exp)] = [
                len(exp_samples),
                len(exp_attributes),
                float(len(exp_attributes)/len(exp_samples))]

    print(exp_data)
    lst = [exp_data[exp][2] for exp in exp_data]
    print(lst, numpy.mean(lst), numpy.std(lst))


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
    retreive experiment data from ArrayExpress and add it to db
    """

    experiment, microarrays = get_experiment_attributes(experiment_id)
    samples = get_experiment_samples_attributes(experiment_id)
    experiment_obj = Experiment.add_or_replace(data=experiment)
    print("Created:", experiment_obj)


    for microarray in microarrays:
        microarray_obj = Microarray.add_or_replace(data=microarray)
        if not(experiment_obj.microarrays.filter(id=microarray_obj.id).exists()):
            experiment_obj.microarrays.add(microarray_obj)
            experiment_obj.save()
            print("Added microarray:", microarray_obj, "to", experiment_obj)

    for sample in samples:  
        sample_obj = Sample.add_or_replace(experiment=experiment_obj,
                                           data=sample)
        sample_attributes = SampleAttribute.objects.filter(sample=sample_obj)
        for old_name, old_value in sample.items():

            if old_value == None or old_value == '':
                SampleAttribute.add_or_replace(sample_obj, old_name, '<empty>')
            else:
                SampleAttribute.add_or_replace(sample_obj, old_name, old_value)


def sample_to_db(experiment_id, sample_data):
    """

    :param experiment_id: string of experiment ArrayExpress accession number
    :param sample_data: dict
    :return:
    """

        




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


# get all unique name value pairs for exp
# to tsv
# manually add standard names, values
# save
# read tsv to SampleAttribute table of the database

def unify_exp(exp):
    """

    """
    experiment = Experiment.find(exp)
    attributes = experiment.sample_attributes()
    # pairs = ["\t".join([str(attribute.old_name), str(attribute.old_value)])
    #         for attribute 
    #         in attributes]

    # for pair in sorted(set(pairs)):
    #     print(pair)
    
    # print(len(attributes))
    # for attribute in apttributes:
    #     print(attribute)
    with open('articles/temp/standardize_E-GEOD-73685_full.tsv') as tsvin:
        rows = csv.reader(tsvin, delimiter='\t')
        for row in rows:
            print(row)
            row = [item for item in row if item]
            sample_attributes = attributes.filter(old_name=row[0],old_value = row[1])
            samples = sample_attributes
            for sample_attribute in sample_attributes:

                unificated_name = StandardName.objects.get(name = row[2])
                unificated_value = StandardValue.objects.get(value = row[3])
                sample_attribute.unificated_name = unificated_name
                sample_attribute.unificated_value = unificated_value
                print("Modified!", sample_attribute, end='')
                sample_attribute.save()
                print(".. and saved!")
                

                for pair in range(4, len(row), 2): # if row length = 8 then [4,6]
                    unificated_name = StandardName.objects.get(name = row[pair])
                    unificated_value = StandardValue.objects.get(value = row[pair + 1])
                    new_sa = SampleAttribute.objects.create(
                            sample=sample_attribute.sample,
                            old_name = sample_attribute.old_name,
                            old_value = sample_attribute.old_value,
                            unificated_name = unificated_name,
                            unificated_value = unificated_value)
                    
                    print("Created!", new_sa, end='')
                    new_sa.save()
                    print(".. and saved!")

def sample_tsv_to_three_column_tsv():
    """Create "sample    old_name    old_value" tsv based on samples.tsv"""
    with open('articles/temp/vsevolod.tsv') as tsvin:
        rows = list(csv.reader(tsvin, delimiter='\t'))
        pairs = []
        rownames = rows[0]
        for rowid in range(1,len(rows)):
            sample_name = rows[rowid][0]
            if sample_name:
                for colid in range(len(rows[rowid])):
                    if rows[rowid][colid]:
                        pairs.append('\t'.join([sample_name, rownames[colid], rows[rowid][colid]]))

        with open('articles/temp/three_cols_vsevolod.tsv', 'w') as tsv:
            for pair in pairs:
                tsv.write(pair+'\n')

def three_column_tsv_check():
    attributes = SampleAttribute.objects.all()

    with open('articles/temp/three_cols_vsevolod.tsv', 'r') as tsv:
        rows = list(csv.reader(tsv, delimiter='\t'))
        for row in rows:
            sample = SampleAttribute.objects.filter(
                unificated_name__name='Sample Name',
                old_value=row[0]).first()
            if sample:
                sample = sample.sample
            else:
                print("No such sample", row[0])
                return

            attribute = attributes.filter(sample=sample, unificated_name__name=row[1]).first()

            """
            1. sample unificated_name unificated_value
                do nothing
            2. sample unificated_name old_value
                do nothing
            3. sample unificated_name
                modify old_value
            4. sample
                add new old name old value
            5. nothing
                print(nosample)
            """
            if attribute:
                if attribute.unificated_value:
                    value = attribute.unificated_value.value
                else:
                    value = ""
                if value == row[2] or attribute.old_value == row[2]:
                    # print("Do nothing for", attribute)
                    pass
                else:
                    print("Modify old value", attribute.old_value, "to", row[2], "in", row, attribute)
                    # attribute.old_value = row[2]
            else:
                pass
                # print("Make new attribute", row)

















                # SampleAttribute.add_or_replace(
                #         sample=sample,
                #         old_name=row[1],
                #         old_value=row[2]
                # )









def tsv_to_db():
        with open('articles/temp/three_cols_vsevolod.tsv', 'r') as tsv:
            rows = list(csv.reader(tsv, delimiter='\t'))
            for row in rows:
                sample = SampleAttribute.objects.filter(
                        unificated_name__name='Sample Name',
                        old_value=row[0]).first()
                
                if sample:
                    sample = sample.sample
                    unificated_name = StandardName.objects.filter(name=row[1]).first()
                    if unificated_name:
                        unificated_value = StandardValue.objects.filter(value=row[2]).first()
                        if unificated_value:
                            if SampleAttribute.objects.filter(
                                    sample,
                                    unificated_name=unificated_name,
                                    unificated_value=unificated_value):
                                print("Exists", sample, unificated_name, unificated_value)
                            else:
                                print("Not Exist", sample, unificated_name, unificated_value)
                        else:
                            
                            if SampleAttribute.objects.filter(
                                    sample=sample,
                                    unificated_name=unificated_name,
                                    old_value=row[2]):
                                print("Exists", sample, unificated_name, row[2])
                            else:
                                print("Not Exist", sample, unificated_name, row[2])


"""
samples.tsv to three column.tsv
three_column.tsv to db as old names
three_column.tsv to standardize.tsv
standardize.tsv to unify_exp()
"""


def main():
    pass
    # get_sample_attributes_with_no_old_name()
    # get_experiment_samples_attributes('E-GEOD-14722')
    

if __name__ == '__main__':
    main()
