import h5py
import argparse
import numpy as np
import pandas as pd
import phenograph
from collections import Counter

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", required=True, help="filtered counts input")
parser.add_argument("-o","--output_path",required=False, default="./", help="path to the output")
parser.add_argument("-s", "--sample_name",required=False, default="", help="name of the sample")

args = parser.parse_args()

# clustering/classification params
n_neighbours = 100
n_jobs = 16
# points in the knn neighbourhood are weighted by the distance
weight='distance'

filtered_counts = np.loadtxt(args.input)

communities, graph, Q = phenograph.cluster(data=filtered_counts,k=n_neighbours,n_jobs=n_jobs, jaccard=True)

print(communities) # one of the outputs

communities_df = pd.DataFrame(communities,columns=['cluster'])
communities_df['cell_barcode'] = communities_df.index
communities_df = communities_df[['cell_barcode','cluster']] # order the columns
communities_df.head()

communities_df.to_csv(args.output_path + '/' + args.sample_name + "_clusters_phenograph_assignment.tsv",sep='\t',index=False)


cells_by_cluster = []
for cluster in sorted(list(Counter(communities))):
    cells_by_cluster.append(filtered_counts[communities==cluster])

avg_clusters = [m.mean(0) for m in cells_by_cluster] # 2nd output

avg_clusters_df = pd.DataFrame(avg_clusters)

avg_clusters_df.to_csv(args.output_path + '/' + args.sample_name + "_clusters_phenograph_profiles.tsv",sep='\t',index=False, header=False)
