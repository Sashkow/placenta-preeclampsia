import pandas
import csv
import os
import glob
# with open('/home/sashko/a/python/placenta-preeclampsia/articles/static/tsv/samples.tsv', 'rb') as f:
#     reader = csv.reader(f, delimiter='\t')
#     for row in reader:
#         print row

outfile = "/home/sashko/a/python/placenta-preeclampsia/articles/everyone.tsv"







def merge_with_igea(phenodata_folder, merged_folder):
	"""
	Merges each tsv file in phenodata_folder with igea metadata
	and saves files into merged_folder
	"""
	tsvs = glob.glob(os.path.join(phenodata_folder,'*.tsv'))
	igea_tsv = '/home/sashko/a/python/placenta-preeclampsia/articles/static/tsv/samples.tsv'


	for current_tsv in tsvs:

		df1 = pandas.read_csv(igea_tsv, sep='\t', parse_dates=False)
		df2 = pandas.read_csv(current_tsv, sep='\t', parse_dates=False)

		df3 = pandas.merge(
			df1,
			df2,
			left_on='Sample Name',
			right_on='Source.Name',
			how='right'
		)

		df3.to_csv(
				os.path.join(merged_folder, current_tsv.split('/')[-1]),
		 		sep="\t", header=True, index=False, na_rep="NA")


merge_with_igea(
		'/home/sashko/a/r/article-microarrays/pdata/',
		'/home/sashko/a/r/article-microarrays/pdata/merged'
)