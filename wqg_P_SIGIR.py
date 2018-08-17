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
from random import randint

def bychance(p):
    r = randint(1,100)
    threshold = 100 * p;
    if r <= threshold:
        return True
    else:
        return False


EPSILON = 0.001

if (len(sys.argv) != 5):
    print 'Usage: %s <test.svm> <test.out> <query_part_dir> <test.q>' % sys.argv[0]
    exit(0)

svm_test=sys.argv[1]
test_out = sys.argv[2]
query_part_dir = sys.argv[3]
query_output = open(sys.argv[4], 'w')

d=defaultdict(dict)
qids=set()

with open(svm_test, 'r') as f1, open(test_out, 'r') as f2:
    for line_zip in zip(f1, f2):
        line = line_zip[0]

        qid = int(line.strip().split('\t')[-1])
        qids.add(qid)
        part = line.strip().split('\t')[-2].strip()
#        true_oddp = float(line.strip().split(' ')[0])
        pred_p = float(line_zip[1])
#        true_p = oddp2p(true_oddp)
#        print qid, part, oddp2p(true_oddp)

        if pred_p < 0:
            pred_p = EPSILON

        (d[qid])[part] = pred_p
        

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

    for part in query_parts[qid]:

        if part.startswith('#'):
            continue

        recall =None

        min_pred_p = min(d[qid].values())
        
        if part in d[qid]:
            recall = (d[qid])[part]
            
            '''
            # Test Here
            if bychance(0.8):
                recall = (d[qid])[part]
            else:
                recall = 0.5
                '''
        else:
            # For terms not appearing in top docs, assign default weight
            # Choice one: minimum weight
            # Choise two: 0.5 ==> seems not a good idea 
            #           pp          Helped T5->t6, T9-T10 a little bit, hurt T3->T4 a bit, T7->T8 no change

            recall = min(EPSILON, min_pred_p)
            

            
            
        query_output.write('\t%f %s\n' %(recall, part))
    
    query_output.write(' )\n')
    query_output.write('\t</text></query>\n')
    
query_output.write('</parameters>\n')

query_output.close()
