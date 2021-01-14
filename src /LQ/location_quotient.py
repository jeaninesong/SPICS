import sys
import pandas as pd
import spacy
import numpy as np
import math
import argparse
from argparse import ArgumentParser
nlp = spacy.load('en_core_web_lg')

parser = ArgumentParser()
parser.add_argument("--irecf", type=str, default='IREC Result of LDA model')
parser.add_argument("--walmidf", type=str, required=True, help='WALMID Result of LDA model')
args = parser.parse_args()

irecf = args.irecf
walmidf = args.walmidf

# irec
# learn embeddings of keywords 
irec = pd.read_csv(irecf)
irecid_keywords_dict = {}
for cid, keywords in zip(irec['cluster_id'], irec['keyword'].tolist()):
    if cid not in irecid_keywords_dict.keys():
        cid = int('1'+str(cid))
        irecid_keywords_dict[cid] = keywords
irec_id_vec = {}
for cid, cluster in irecid_keywords_dict.items():
    clusters_vecs = []
    cluster = ' '.join(cluster.split(', '))
    for word in nlp(cluster):
        clusters_vecs.append(word.vector)
    cluster_vec = np.mean(np.array(clusters_vecs), axis=0)
    irec_id_vec[cid] = cluster_vec
# count the number of companies 
irec_rids_dict = {}
ireccid_rids_dict = {}
for cid, rid in zip(irec['cluster_id'], irec['rid']):
    cid = int('1'+str(cid))
    if cid not in ireccid_rids_dict.keys():
        ireccid_rids_dict[cid] = [rid]
    else:
        if rid not in ireccid_rids_dict[cid]:
            ireccid_rids_dict[cid].append(rid)
    if rid not in irec_rids_dict.keys():
        irec_rids_dict[rid] = ''
ireccid_rids_sorted = {k: v for k, v in sorted(ireccid_rids_dict.items(), key=lambda item: item[0])}
ireccid_ridnum_dict = {}
for cid, rids in ireccid_rids_sorted.items():
    ireccid_ridnum_dict[cid] = len(rids)
# compute regional quotient 
print('Number of rid in irec:', len(irec_rids_dict))
ireccid_rq_dict = {}
cid_rq_dict = {}
for cid, ridnum in ireccid_ridnum_dict.items():
    ireccid_rq_dict[cid] = ridnum/len(irec_rids_dict)
    cid_rq_dict[cid] = ridnum/len(irec_rids_dict)

# walmid
# learn embeddings of keywords 
walmid = pd.read_csv(walmidf)
walmidid_keywords_dict = {}
for cid, keywords in zip(walmid['cluster_id'], walmid['keyword'].tolist()):
    cid = int('2'+str(cid))
    if cid not in walmidid_keywords_dict.keys():
        walmidid_keywords_dict[cid] = keywords
walmid_id_vec = {}
for cid, cluster in walmidid_keywords_dict.items():
    clusters_vecs = []
    cluster = ' '.join(cluster.split(', '))
    for word in nlp(cluster):
        clusters_vecs.append(word.vector)
    cluster_vec = np.mean(np.array(clusters_vecs), axis=0)
    walmid_id_vec[cid] = cluster_vec
# count the number of companies 
walmid_rids_dict = {}
walmidcid_rids_dict = {}
for cid, rid in zip(walmid['cluster_id'], walmid['rid']):
    cid = int('2'+str(cid))
    if cid not in walmidcid_rids_dict.keys():
        walmidcid_rids_dict[cid] = [rid]
    else:
        if rid not in walmidcid_rids_dict[cid]:
            walmidcid_rids_dict[cid].append(rid)
    if rid not in walmid_rids_dict.keys():
        walmid_rids_dict[rid] = ''
walmidcid_rids_sorted = {k: v for k, v in sorted(walmidcid_rids_dict.items(), key=lambda item: item[0])}
walmidcid_ridnum_dict = {}
for cid, rids in walmidcid_rids_sorted.items():
    walmidcid_ridnum_dict[cid] = len(rids)
# compute regional quotient 
print('Number of rid in walmid:', len(walmid_rids_dict))
walmidcid_rq_dict = {}
for cid, ridnum in walmidcid_ridnum_dict.items():
    walmidcid_rq_dict[cid] = ridnum/len(walmid_rids_dict)
    cid_rq_dict[cid] = ridnum/len(walmid_rids_dict)

region_quotient_pd = pd.DataFrame()
region_quotient_pd['cluster_id'] = list(cid_rq_dict.keys())
region_quotient_pd['region_quotient'] = list(cid_rq_dict.values())
# print('region_quotient_pd:', region_quotient_pd)
# region_quotient_pd.to_excel('region_quotient.xlsx', index=False)  

def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    return sumxy/math.sqrt(sumxx*sumyy)

irec_id_vec_sorted = {k: v for k, v in sorted(irec_id_vec.items(), key=lambda item: item[0])}
walmid_id_vec_sorted = {k: v for k, v in sorted(walmid_id_vec.items(), key=lambda item: item[0])}

irecid_wssslid_dict = {}
irecid_cs_dict = {}
for irec_idx, irec_vec in irec_id_vec_sorted.items():
    # walmid
    iw_cs_list = []
    iw_wid_list = []
    for walmid_idx, walmid_vec in walmid_id_vec_sorted.items():
        iw_cs = cosine_similarity(irec_vec, walmid_vec)
        iw_cs_list.append(iw_cs)
        iw_wid_list.append(walmid_idx)
    max_iw = max(iw_cs_list)
    max_widx = iw_wid_list[iw_cs_list.index(max(iw_cs_list))]
    max_iw_walmid_vec = walmid_id_vec_sorted[max_widx]
    irecid_wssslid_dict[irec_idx] = [max_widx]
    irecid_cs_dict[irec_idx] = max_iw
    
irecid_cs_dict_sorted = {k: v for k, v in sorted(irecid_cs_dict.items(), key=lambda item: item[1], reverse=True)}

# print(irecid_wssslid_dict)
# print(cid_rq_dict)

# location quotient
# top k cosine similarity 

print('irecid_cs_dict_sorted:', irecid_cs_dict_sorted)
topk = 10
top_ireccid_cs = list(irecid_cs_dict_sorted.keys())
top_irec_cid = []
top_walmid_cid = []
i = 0
for icid in top_ireccid_cs:
    print('icid:', icid)
    if i < topk:
        wcid = irecid_wssslid_dict[icid][0]
        if wcid not in top_walmid_cid:
            top_irec_cid.append(icid)
            top_walmid_cid.append(wcid)
            i += 1

ii_lq_dict = {}
iw_lq_dict = {}
wi_lq_dict = {}
ww_lq_dict = {}

locale_left = []
locale_right = []
cluster_id_left = []
cluster_id_right = []
location_quotient = []

for icid, wcid in zip(top_irec_cid, top_walmid_cid):
    ii_lq = cid_rq_dict[icid]/cid_rq_dict[icid]
    locale_left.append('IRELAND COMBINED')
    locale_right.append('IRELAND COMBINED')
    cluster_id_left.append(icid)
    cluster_id_right.append(icid)
    location_quotient.append(ii_lq)

    iw_lq = cid_rq_dict[icid]/cid_rq_dict[wcid]
    locale_left.append('IRELAND COMBINED')
    locale_right.append('WALES/MIDLANDS')
    cluster_id_left.append(icid)
    cluster_id_right.append(wcid)
    location_quotient.append(iw_lq)

    ii_lq_dict[str(icid)+'_'+str(icid)] = ii_lq
    iw_lq_dict[str(icid)+'_'+str(wcid)] = iw_lq
    
    wi_lq = cid_rq_dict[wcid]/cid_rq_dict[icid]
    locale_left.append('WALES/MIDLANDS')
    locale_right.append('IRELAND COMBINED')
    cluster_id_left.append(wcid)
    cluster_id_right.append(icid)
    location_quotient.append(wi_lq)

    ww_lq = cid_rq_dict[wcid]/cid_rq_dict[wcid]
    locale_left.append('WALES/MIDLANDS')
    locale_right.append('WALES/MIDLANDS')
    cluster_id_left.append(wcid)
    cluster_id_right.append(wcid)
    location_quotient.append(ww_lq)
    wi_lq_dict[str(wcid)+'_'+str(icid)] = wi_lq
    ww_lq_dict[str(wcid)+'_'+str(wcid)] = ww_lq

print('locale_left:', locale_left)
location_quotient_pd = pd.DataFrame()
location_quotient_pd['locale_left'] = locale_left
location_quotient_pd['locale_right'] = locale_right
location_quotient_pd['cluster_id_left'] = cluster_id_left
location_quotient_pd['cluster_id_right'] = cluster_id_right
location_quotient_pd['location_quotient'] = location_quotient
location_quotient_pd.to_excel('location_quotient.xlsx', index=False)  




