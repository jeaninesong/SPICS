
import pickle
import pandas as pd
import os
import argparse
from argparse import ArgumentParser
import time

import collections
import math

#########################################################################################
def timer(global_time,local_time):
    gtime=round(time.time() - global_time, 2)
    ltime=round(time.time() - local_time, 2)     
    print("--- "+str(ltime)+" / "+str(gtime)+" sec ---\n")
    return 


##########################################################################################
# get the input from the command line - both are required (simplify: file_name=sys.argv[0])
##########################################################################################
global_time = time.time()
root = os.path.dirname(os.path.realpath(__file__))

parser = ArgumentParser()
parser.add_argument("--sec", type=int, default=1)
parser.add_argument("--secf", type=str, default='section_sic.dict')
parser.add_argument("--divf", type=str, default='division_sic.dict')
parser.add_argument("--ridsicf", type=str, default='ridsic.dict')
parser.add_argument("--rf", type=str, required=True, help='Result of LDA model')

args = parser.parse_args()

sec_flag = args.sec
secf = args.secf
divf = args.divf
ridsicf = args.ridsicf
rf = args.rf

print('\n\n\n[EVALUATION]')
print(parser.parse_args())
print('')


##########################################################################################
# Load data
##########################################################################################
print('Load data...')
local_time = time.time()

secsic_dict = pickle.load(open(secf, 'rb'))
divsic_dict = pickle.load(open(divf, 'rb'))
ridsic_dict = pickle.load(open(ridsicf, 'rb'))

r_data = pd.read_csv(rf)

# print('secsic_dict:', secsic_dict)
# print('divsic_dict:', divsic_dict)
# print('ridsic_dict:', ridsic_dict)

# key: sic value: section/division
sec_list = []
sicsec_dict = {}
for sec, sics in secsic_dict.items():
    for sic in sics:
        if sec not in sec_list:
            sec_list.append(sec)
        sicsec_dict[sic] = sec_list.index(sec)
print('sicsec_dict:', len(sicsec_dict))           

div_list = []
sicdiv_dict = {}
for div, sics in divsic_dict.items():
    for sic in sics:
        if div not in div_list:
            div_list.append(div)
        sicdiv_dict[sic] = div_list.index(div)
print('sicdiv_dict:', len(sicdiv_dict))   

timer(global_time,local_time)

##########################################################################################
# Evaluation Function
##########################################################################################
def purity_score(result, label):
    total_num = len(label)
    cluster_counter = collections.Counter(result)
    original_counter = collections.Counter(label)
    t = []
    for k in cluster_counter:
        p_k = []
        for j in original_counter:
            count = 0
            for i in range(len(result)):
                if result[i] == k and label[i] == j: 
                    count += 1
            p_k.append(count)
        temp_t = max(p_k)
        t.append(temp_t)
    return sum(t)/total_num

def NMI(result, label):
    total_num = len(label)
    cluster_counter = collections.Counter(result)
    original_counter = collections.Counter(label)
    MI = 0
    eps = 1.4e-45
    for k in cluster_counter:
        for j in original_counter:
            count = 0
            for i in range(len(result)):
                if result[i] == k and label[i] == j:
                    count += 1
            p_k = 1.0*cluster_counter[k] / total_num
            p_j = 1.0*original_counter[j] / total_num
            p_kj = 1.0*count / total_num
            MI += p_kj * math.log(p_kj /(p_k * p_j) + eps, 2)
    H_k = 0
    for k in cluster_counter:
        H_k -= (1.0*cluster_counter[k] / total_num) * math.log(1.0*cluster_counter[k] / total_num+eps, 2)
    H_j = 0
    for j in original_counter:
        H_j -= (1.0*original_counter[j] / total_num) * math.log(1.0*original_counter[j] / total_num+eps, 2)
    return 2.0 * MI / (H_k + H_j)

def contingency_table(result, label):
    total_num = len(label)
    TP = TN = FP = FN = 0
    for i in range(total_num):
        for j in range(i + 1, total_num):
            if label[i] == label[j] and result[i] == result[j]:
                TP += 1
            elif label[i] != label[j] and result[i] != result[j]:
                TN += 1
            elif label[i] != label[j] and result[i] == result[j]:
                FP += 1
            elif label[i] == label[j] and result[i] != result[j]:
                FN += 1
    return (TP, TN, FP, FN)

def rand_index(result, label):
    TP, TN, FP, FN = contingency_table(result, label)
    return 1.0*(TP + TN)/(TP + FP + FN + TN)

def precision(result, label):
    TP, TN, FP, FN = contingency_table(result, label)
    return 1.0*TP/(TP + FP)

def recall(result, label):
    TP, TN, FP, FN = contingency_table(result, label)
    return 1.0*TP/(TP + FN)

def F_measure(result, label, beta=1):
    prec = precision(result, label)
    r = recall(result, label)
    return (beta*beta + 1) * prec * r/(beta*beta * prec + r)

##########################################################################################
# Section Evaluation 
##########################################################################################
if sec_flag == 1:
    print('Section Evaluation...')
    local_time = time.time()

    seclabel_list = []
    secresult_list = []
    for row in r_data.values.tolist():
        clusterid = int(row[0])
        rid = str(row[2])
        sic = ridsic_dict[rid]
        if sic not in sicsec_dict.keys():
            continue
        label = sicsec_dict[sic]
        seclabel_list.append(label)
        secresult_list.append(clusterid)

    NMI_value = NMI(secresult_list, seclabel_list)
    print('NMI of Section Evaluation:', NMI_value)

    fscore = F_measure(secresult_list, seclabel_list)
    print('F-score of Division Evaluation:', fscore)

    timer(global_time,local_time)

##########################################################################################
# Division Evaluation 
##########################################################################################
if sec_flag != 1:
    print('Division Evaluation...')
    local_time = time.time()

    divlabel_list = []
    divresult_list = []
    for row in r_data.values.tolist():
        clusterid = int(row[0])
        rid = str(row[2])
        sic = ridsic_dict[rid]
        if sic not in sicdiv_dict.keys():
            continue
        label = sicdiv_dict[sic]
        divlabel_list.append(label)
        divresult_list.append(clusterid)

    NMI_value = NMI(divresult_list, divlabel_list)
    print('NMI of Division Evaluation:', NMI_value) 

    fscore = F_measure(divresult_list, divlabel_list)
    print('F-score of Division Evaluation:', fscore)

    timer(global_time,local_time)

