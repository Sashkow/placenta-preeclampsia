from bioservices.arrayexpress import ArrayExpress
import pickle
import requests
import xml.etree.ElementTree as etree

import numpy

s = ArrayExpress()


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


def get_placenta_accession():
    # retu E-GEOD-59126

    return s.queryAE(
            keywords="placenta",
            exptype="*array*",
            species="homo+sapiens"
    )

# def microarray_human_experimnents_to_file():
#     url = 'https://www.ebi.ac.uk/arrayexpress/xml/v3/experiments?exptype=transcription+profiling+by+array&species="homo sapiens"&date=2010*                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         '

#     local_filename = url.split('/')[-1]
#     # NOTE the stream=True parameter
#     r = requests.get(url, stream=True)
#     with open('temp/all.xml', 'wb') as f:
#         i = 0
#         for chunk in r.iter_content(chunk_size=1024): 

#             if chunk: # filter out keep-alive new chunks
#                 f.write(chunk)
#                 #f.flush() commented by recommendation from J.F.Sebastian
#             else:
#                 print("chunk dead)")
#             i+=1
#             print("chunk",i,"kb")
        
#         print('retrieving experiments:')
        
#         # for exp_id in exp_ids[:10]:
#         #     print("     ", exp_id)
#         #     exp = s.retrieveExperiment(exp_id)
#         #     # pass top level of xml 
#         #     exp = exp.getchildren()[0]
#         #     print(exp, file=f)


def placenta_experimnents_to_file():
    with open('temp/placenta_experiments.txt', 'w') as f:
        exps = s.queryExperiments(
                keywords="placenta",
                exptype="*array*",
                species="homo+sapiens")
        print(exps, file=f)

def preeclampsia_experimnents_to_file():
    """print all assenions of experiment with microarrays"""
    with open('temp/preeclampsia_experiments.txt', 'w') as f:
        exps = s.queryExperiments(
                keywords="pre-eclampsia+OR+preeclampsia+OR+pre-eclamptic+OR+preeclamptic",
                exptype="*array*",
                species="homo+sapiens")
        print(exps, file=f)

def exp_generator(experiments_file_path):
    with open(experiments_file_path, 'r') as f:
        yield f.readline()

def use_exp_generator(experiments_file_path):
    
    for event, elem in etree.iterparse(experiments_file_path, events=('start', 'end', 'start-ns', 'end-ns')):
        print(event, elem)

def get_experiments_attributes_from_file(experiments_file_path):
    """
    get release year, samples amount and unique attributes amount
    """
    with open(experiments_file_path, 'r') as f:
        content = f.read()
        print("reading...")
        exps = s.easyXML(content)
        print('read!')
        exps_data = {}
        total_attributes = 0
        total_samples = 0


        

        for exp in exps.getchildren():      
            
            year = 0
            samples = 0
            attributes = 0
            accession = ''
            skip = False

            for item in exp.getchildren():
                if item.tag == 'releasedate':
                    year = item.text.strip().split('-')[0]
                elif item.tag == 'sampleattribute':
                    attributes += 1
                elif item.tag == 'assays':
                    samples = int(item.text.strip())
                    if samples > 200:
                        skip = True
                elif item.tag == 'accession':
                    accession = item.text.strip()
                # print(year,attributes,samples,accession)


            attributes = attributes * samples            

            if not skip:
                total_attributes += attributes
                total_samples += samples
                exps_data[accession] = [year, samples, attributes]


        
        print(total_attributes, total_samples, float(total_attributes)/total_samples)
        for exp in exps_data:
                print(exp, exps_data[exp], float(exps_data[exp][2])/exps_data[exp][1])



        year_samples_attributes = {}
        for exp, data in exps_data.items():
            attrs_per_sample = float(exps_data[exp][2])/exps_data[exp][1]
            if data[0] not in year_samples_attributes:
                # year_samples_attributes[data[0]] = [data[1],data[2],1]
                year_samples_attributes[data[0]] = [[attrs_per_sample], 1]
                

            else:
                # year_samples_attributes[data[0]][0] += data[1]
                # year_samples_attributes[data[0]][1] += data[2]
                # year_samples_attributes[data[0]][2] += 1
                year_samples_attributes[data[0]][0].append(attrs_per_sample)
                year_samples_attributes[data[0]][1] += 1



        avg_list = []
        # print(year_samples_attributes)
        for year in sorted(year_samples_attributes):
            # print(
            #         year,
            #         round(float(year_samples_attributes[year][1])/year_samples_attributes[year][0],2),
            #         year_samples_attributes[year][2]
            # )
            lst = year_samples_attributes[year][0]
            avg_list.append(round(float(sum(lst))/len(lst),2))
            print(
                    year,
                    round(float(sum(lst))/len(lst),2),
                    year_samples_attributes[year][1])

        print(numpy.mean(avg_list), numpy.std(avg_list))


    

    # for year, data in sorted(year_atributes_per_sample.items()):
    #     print(year, float(data[0])/data[1], data[1])

    
# microarray_human_experimnents_to_file()
# preeclampsia_experimnents_to_file()
# placenta_experimnents_to_file()
# get_experiments_attributes_from_file('temp/placenta_experiments.txt')
get_experiments_attributes_from_file('temp/preeclampsia_experiments.txt')
# get_experiments_attributes_from_file('temp/all.xml')
# use_exp_generator('temp/all.xml')
