import csv
import pandas as pd
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--irecf", type=str, required=True, help="output csv file of LDA model of region IREC")
parser.add_argument("--walmidf", type=str, required=True, help="output csv file of LDA model of region WALMID")
args = parser.parse_args()

irecf = args.irecf + '.csv'
walmidf = args.walmidf + '.csv'

# irec
irec = pd.read_csv(irecf)
irec_cyq_ridnum_dict = {}
irec_cyq_dict = {}
irec_cyd_ridweight_dict = {}
for row in irec.values.tolist():
    clusterid = row[0]
    locale = 'IRELAND COMBINED'
    rid = row[2]
    year = row[3]
    quarter = row[4]
    keywords = row[5]
    keywords_weight = row[6]
    ridweight = row[7]
    cyq = str(clusterid)+'-'+str(year)+'-'+str(quarter)
    if cyq not in irec_cyq_ridnum_dict.keys():
        irec_cyq_ridnum_dict[cyq] = 1
        irec_cyq_dict[cyq] = [clusterid, locale, year, quarter, keywords, keywords_weight]
        irec_cyd_ridweight_dict[cyq] = str(rid)+', '+str(ridweight)
    else:
        irec_cyq_ridnum_dict[cyq] += 1
        irec_cyd_ridweight_dict[cyq]+=', '+str(rid)+', '+str(ridweight)
irec_clusterid_list = []
irec_locale_list = []
irec_year_list = []
irec_quarter_list = []
irec_cluster_keyword_list = []
irec_cluster_analysis_results_list = []
for _, values in irec_cyq_dict.items():
    irec_clusterid_list.append(values[0])
    irec_locale_list.append(values[1])
    irec_year_list.append(values[2])
    irec_quarter_list.append(values[3])
    irec_cluster_keyword_list.append(values[4])
    irec_cluster_analysis_results_list.append(values[5])
irec_cluster_no_companies_list = list(irec_cyq_ridnum_dict.values())
irec_COMPANIES_list = list(irec_cyd_ridweight_dict.values())
irec_data = pd.DataFrame()
irec_data['cluster_id'] = irec_clusterid_list
irec_data['locale'] = irec_locale_list
irec_data['year'] = irec_year_list
irec_data['quarter'] = irec_quarter_list
irec_data['cluster_no_companies'] = irec_cluster_no_companies_list
irec_data['cluster_keyword'] = irec_cluster_keyword_list
irec_data['cluster_analysis_result']= irec_cluster_analysis_results_list
irec_data['COMPANIES']= irec_COMPANIES_list
new_irec_clusterid1 = []
irec_tps = []
irec_tp = []
irec_clusterid = irec_data['cluster_id'].tolist()
for i in irec_clusterid:
    new_id = int('1'+str(i))
    new_irec_clusterid1.append(new_id)
irec_year = irec_data['year'].tolist()
irec_quarter = irec_data['quarter'].tolist()
for y, q in zip(irec_year, irec_quarter):
    irec_tps.append(int(str(y)+str(q)))
    irec_tp.append((str(y)+' - Q'+str(q)))
irec_ridweight = irec_data['COMPANIES'].tolist()
new_irec_clusterid2 = []
irec_rid = []
irec_weight = []
for idx, ridweight in zip(irec_clusterid, irec_ridweight):
    ridweight = ridweight.strip().split(', ')
    new_id = int('1'+str(idx))
    for i in range(0,len(ridweight)-1,2):
        rid = ridweight[i]
        weight = ridweight[i+1]
        new_irec_clusterid2.append(new_id)
        irec_rid.append(rid)
        irec_weight.append(weight)


# walmid
walmid = pd.read_csv(walmidf)
walmid_cyq_ridnum_dict = {}
walmid_cyq_dict = {}
walmid_cyd_ridweight_dict = {}
for row in walmid.values.tolist():
    clusterid = row[0]
    locale = 'WALES/MIDLANDS'
    rid = row[2]
    year = row[3]
    quarter = row[4]
    keywords = row[5]
    keywords_weight = row[6]
    ridweight = row[7]
    cyq = str(clusterid)+'-'+str(year)+'-'+str(quarter)
    if cyq not in walmid_cyq_ridnum_dict.keys():
        walmid_cyq_ridnum_dict[cyq] = 1
        walmid_cyq_dict[cyq] = [clusterid, locale, year, quarter, keywords, keywords_weight]
        walmid_cyd_ridweight_dict[cyq] = str(rid)+', '+str(ridweight)
    else:
        walmid_cyq_ridnum_dict[cyq] += 1
        walmid_cyd_ridweight_dict[cyq]+=', '+str(rid)+', '+str(ridweight)
walmid_clusterid_list = []
walmid_locale_list = []
walmid_year_list = []
walmid_quarter_list = []
walmid_cluster_keyword_list = []
walmid_cluster_analysis_results_list = []
for _, values in walmid_cyq_dict.items():
    walmid_clusterid_list.append(values[0])
    walmid_locale_list.append(values[1])
    walmid_year_list.append(values[2])
    walmid_quarter_list.append(values[3])
    walmid_cluster_keyword_list.append(values[4])
    walmid_cluster_analysis_results_list.append(values[5])
walmid_cluster_no_companies_list = list(walmid_cyq_ridnum_dict.values())
walmid_COMPANIES_list = list(walmid_cyd_ridweight_dict.values())
walmid_data = pd.DataFrame()
walmid_data['cluster_id'] = walmid_clusterid_list
walmid_data['locale'] = walmid_locale_list
walmid_data['year'] = walmid_year_list
walmid_data['quarter'] = walmid_quarter_list
walmid_data['cluster_no_companies'] = walmid_cluster_no_companies_list
walmid_data['cluster_keyword'] = walmid_cluster_keyword_list
walmid_data['cluster_analysis_result']= walmid_cluster_analysis_results_list
walmid_data['COMPANIES']= walmid_COMPANIES_list

new_walmid_clusterid1 = []
walmid_tps = []
walmid_tp = []
walmid_clusterid = walmid_data['cluster_id'].tolist()
for i in walmid_clusterid:
    new_id = int('2'+str(i))
    new_walmid_clusterid1.append(new_id)
walmid_year = walmid_data['year'].tolist()
walmid_quarter = walmid_data['quarter'].tolist()
for y, q in zip(walmid_year, walmid_quarter):
    walmid_tps.append(int(str(y)+str(q)))
    walmid_tp.append((str(y)+' - Q'+str(q)))
new_walmid_clusterid2 = []    
walmid_rid = []
walmid_weight = []
walmid_ridweight = walmid_data['COMPANIES'].tolist()
for idx, ridweight in zip(walmid_clusterid, walmid_ridweight):
    ridweight = ridweight.strip().split(', ')
    new_id = int('2'+str(idx))
    for i in range(0,len(ridweight)-1,2):
        rid = ridweight[i]
        weight = ridweight[i+1]
        new_walmid_clusterid2.append(new_id)
        walmid_rid.append(rid)
        walmid_weight.append(weight)


cluster_id = []
locale = []
year = []
quarter = []
cluster_no_companies = []
cluster_keyword = []
cluster_analysis_result = []
time_points = []
time_point = []
cluster_id1 = new_irec_clusterid1 + new_walmid_clusterid1 
locale = irec_data['locale'].tolist() + walmid_data['locale'].tolist() 
year = irec_data['year'].tolist() + walmid_data['year'].tolist() 
quarter = irec_data['quarter'].tolist() + walmid_data['quarter'].tolist() 
cluster_no_companies = irec_data['cluster_no_companies'].tolist() + walmid_data['cluster_no_companies'].tolist() 
cluster_keyword = irec_data['cluster_keyword'].tolist() + walmid_data['cluster_keyword'].tolist() 
cluster_analysis_result = irec_data['cluster_analysis_result'].tolist() + walmid_data['cluster_analysis_result'].tolist() 
time_points = irec_tps + walmid_tps 
time_point = irec_tp + walmid_tp 
fame_pd = pd.DataFrame()
fame_pd['cluster_id'] = cluster_id1
fame_pd['locale'] = locale
fame_pd['year'] = year
fame_pd['quarter'] = quarter
fame_pd['cluster_no_companies'] = cluster_no_companies
fame_pd['cluster_keyword'] = cluster_keyword
fame_pd['cluster_analysis_result'] = cluster_analysis_result
fame_pd['time_points'] = time_points
fame_pd['time_point'] = time_point
fame = pd.read_excel('fame.xlsx', sheet_name='academic wayback_companies')
writer = pd.ExcelWriter('powerbidata.xlsx', engine='xlsxwriter')
fame_pd.to_excel(writer, sheet_name='academic wayback_clusters', index=False)
fame.to_excel(writer, sheet_name='academic wayback_companies', index=False)
writer.save()

rid = irec_rid + walmid_rid
weight = irec_weight + walmid_weight
cluster_id2 = new_irec_clusterid2 + new_walmid_clusterid2
powerbi_pd = pd.DataFrame()
powerbi_pd['cluster_id'] = cluster_id2
powerbi_pd['rid'] = rid
powerbi_pd['weight'] = weight
# powerbi_pd.to_csv('powerbi.csv', index=False, header=True)

f = open('powerbi.txt', 'w')
f.write('cluster_id'+' '+'rid'+' '+'weight'+'\n')
for c, r, w in zip(cluster_id2, rid, weight):
    f.write(str(c)+' '+str(r)+' '+str(w)+'\n')
f.close()







