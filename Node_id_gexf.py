#!/usr/bin/env python3


import pandas as pd
import networkx as nx
import numpy as np
import os,sys,argparse
import time

#Processing tnodeliste interaction file

def process_file(infile, outputfile):
    interaction = pd.read_csv(infile, sep="\s+", usecols=['protein1', 'protein2', 'combined_score'])
    interaction['protein1'] = interaction['protein1'].map(lambda x:x.lstrip('9606.'))
    interaction['protein2'] = interaction['protein2'].map(lambda x:x.lstrip('9606.'))
    unique_protein = np.unique(interaction[['protein1', 'protein2']].values)
    unique_protein_list = unique_protein.tolist()
    unique_protein_list_df = pd.DataFrame(unique_protein_list)
    unique_protein_list_df.index = np.arange(1, len(unique_protein_list_df) + 1)
    index_change = unique_protein_list_df.reset_index()
    index_change.columns = ['Nodes', 'ENSP_ID']
    name_change = index_change[['ENSP_ID', 'Nodes']]
    nodelist = name_change['Nodes'].tolist()
    ensp_list = name_change.groupby('ENSP_ID').Nodes.apply(list).to_dict()
    interaction['Nodes1']= interaction['protein1'].map(ensp_list)
    interaction['Nodes2']= interaction['protein2'].map(ensp_list)
    interaction['Nodes1']= interaction['Nodes1'].str.get(0)
    interaction['Nodes2']= interaction['Nodes2'].str.get(0)
    final_df = interaction[['Nodes1', 'Nodes2', 'combined_score']]


#Building tnodeliste grapnodelist witnodelist edges from dataframe
    Graph = nx.from_pandas_edgelist(final_df, 'Nodes1', 'Nodes2', ['combined_score'])
   

#Adding node attributes

    node_attr1 = dict(zip(nodelist, unique_protein_list))
    nx.set_node_attributes(Graph, node_attr1, 'ENSP-ID')


#writing gexf file
    nx.write_gexf(Graph, outputfile)
    

    
def getArgs():
    parser = argparse.ArgumentParser('pytnodeliston')
    parser.add_argument('-infile', required=True)
    parser.add_argument('-outfile', required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = getArgs()
    file = process_file(args.infile, args.outfile)
    
    start = time.time()
    end = time.time()
    print ('time elapsed:' + str(end - start))

    









