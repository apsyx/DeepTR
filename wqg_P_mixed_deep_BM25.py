##==========================================================================
 # Copyright (c) 2014 Carnegie Mellon University.  All Rights Reserved.
 #
 # Use of the Lemur Toolkit for Language Modeling and Information Retrieval
 # is subject to the terms of the software license set forth in the LICENSE
 # file included with this software (and below), and also available at
 # http://www.lemurproject.org/license.html
 #
##==========================================================================

import sys
from collections import defaultdict
from Constants import *
import ast
import subprocess
import math

def oddp2p(oddp):
#    if oddp< 0.01:
#    return 0.01
    return oddp/ (oddp+1.0)

def qid2trecid(qid):
    if qid in range(301, 451) + range(601, 701):
        return 8
    if qid in range(451, 551):
        return 10
    if qid in range(701, 851):
        return 14

    if qid in range(2001, 2201):
        return 22

    ## separator ##
    if qid >= 401 and qid <= 450:
        return 8
    
    if qid >= 501 and qid <= 550:
        return 10

    if qid >= 751 and qid <= 800:
        return 14
        
    if qid >=2101 and qid <= 2200:
        return 22



def getIndexDocCount(trecid):
    if trecid == 8:
        return 528155
    if trecid == 10:
        return 1692096

    if trecid == 14:
        return 25205179
    
    if trecid == 22:
        return 29038220

def getIdf(df, docCount):
    return math.log((0.5+docCount-df)/(0.5+df))

EPSILON = 0.000001

if (len(sys.argv) != 5):
    print 'Usage: %s <test.svm> <test.out> <query_part_dir> <test.q>' % sys.argv[0]
    exit(0)

svm_test=sys.argv[1]
test_out = sys.argv[2]
query_part_dir = sys.argv[3]
query_output = open(sys.argv[4], 'w')
w_t = 0.8
w_b = 0.1
w_u = 0.1

# TODO
d=defaultdict(list)
qids=set()

with open(svm_test, 'r') as f1, open(test_out, 'r') as f2:
    for line_zip in zip(f1, f2):
        line = line_zip[0]

        qid = line.strip().split('\t')[-1]
        qids.add(int(qid))
        part = line.strip().split('\t')[-2]
#        true_oddp = float(line.strip().split(' ')[0])
        pred_p = float(line_zip[1])
#        true_p = oddp2p(true_oddp)
#        print qid, part, oddp2p(true_oddp)

        if not part.startswith('#'):
            d[qid+'_t'].append((part, pred_p))

        elif part.startswith('#1'):
            d[qid+'_b'].append((part, pred_p))
        else:
            d[qid+'_u'].append((part, pred_p))


sorted(qids)

query_parts=defaultdict(list)

for qid in qids:
    query_part_file = '%s/%d.part' %(query_part_dir, qid)
    with open(query_part_file, 'r') as part_in:
        for line in part_in:
            part = line.strip()
            query_parts[qid].append(part)

query_output.write('<parameters>\n')
for qid in qids:
    query_output.write('\t<query><type>indri</type><number>%d</number><text>\n' % qid)
    query_output.write('#weight(\n')

    #term

    if len(d['%d_t' % qid]) > 0 and w_t > 0:
        query_output.write('         %f #weight( ' % w_t)

        for item in d['%d_t' % qid]:
            pred_p = item[1]
            
            tid = qid2trecid(qid)
            index = INDICES_PREFIX + '/indext%d-v5.3/' % tid
            df_cmd = '%s %s dx %s' % (DUMPINDEX, index, part)
            df_output = subprocess.check_output(df_cmd.split(' ', 3))
            df = ast.literal_eval(df_output.split(':')[-1])
            
            docCount = getIndexDocCount(tid)
            idf = getIdf(df, docCount)
            
            # plug in p(t|R) to bm25 weight
            bm25_weight = 1.0 + (math.log(pred_p) - math.log(1-pred_p)) / idf

            if bm25_weight < 0:
                bm25_weight = EPSILON
                print 'Negative weight for %s in query %d absorbed to %f' % (part, qid, EPSILON)

            query_output.write('%f %s ' % (bm25_weight, item[0]))

        query_output.write(')\n')

    if qid == 2058:
        query_output.write(' )\n')
        query_output.write('\t</text></query>\n')
        continue
        
    query_output.write('         %f #combine( ' % w_b)

    #bigram

    for part in query_parts[qid]:
        if part.startswith('#1'):
            query_output.write(' %s ' % ( part))

    query_output.write(')\n')

    # unordered
    query_output.write('         %f #combine( ' % w_u)
    
    for part in query_parts[qid]:
        if part.startswith('#uw'):
            query_output.write(' %s ' % ( part))

    query_output.write(')\n')

    
    query_output.write(' )\n')
    query_output.write('\t</text></query>\n')
    
query_output.write('</parameters>\n')

query_output.close()
