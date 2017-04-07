from bioservices.arrayexpress import ArrayExpress

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

def annual_attributes_per_sample_in_placenta():
    exps = get_placenta_accession() 
    print(len(exps), 'experiment accession numbers retrieved')
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

    

annual_attributes_per_sample_in_placenta()
