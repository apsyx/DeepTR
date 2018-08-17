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

if len(sys.argv)!=2:
    print 'Usage: %s <input_svm>' % sys.argv[0]
    exit(0)

train_in=open(sys.argv[1], 'r')
A_out=open('%s.A'%sys.argv[1], 'w')
y_out=open('%s.y'%sys.argv[1], 'w')
B_out=open('%s.B'%sys.argv[1], 'w')
wsd_out=open('%s.forwsd' % sys.argv[1], 'w')
A_start=open('%s.starts' %sys.argv[1], 'w')
A_end=open('%s.ends' % sys.argv[1], 'w')

d=defaultdict(list)

pre_qid = -1
count = 0
for line in train_in:
    
    qid = line.strip().split('\t')[-1]
    concept = line.strip().split('\t')[-2]
#    print qid,
    parts = line.strip().split('#',1)[0].split(' ')
    y = float(parts[0])
    y_out.write('%f\n' % y)

    for part in parts:
        if ':' in part:
            value = float(part.split(':')[-1])
            A_out.write('%f ' % value)
            wsd_out.write('%f ' % value)

    A_out.write('\n')
    wsd_out.write('#%s\t%s\n' % (concept, qid))
    d[qid].append(line.strip())
    qqid = int(qid)

    count += 1
    if pre_qid == -1:
        A_start.write('%d\n' % count)
    elif qqid != pre_qid:
        A_start.write('%d\n' % count)
        A_end.write('%d\n' %(count-1))
        
    pre_qid = qqid

A_end.write('%d\n'% count)
A_start.close()
A_end.close()

A_out.close()
wsd_out.close()

def subtract(line_a, line_b):
    tple_a = ()
    tple_b = ()
    part_a = line_a.strip().split('#',1)[0].split(' ')
    part_b = line_b.strip().split('#',1)[0].split(' ')
    for part in part_a:
        if ':' in part:
            value = float(part.split(':')[-1])
            tple_a = tple_a + (value,)

    for part in part_b:
        if ':' in part:
            value = float(part.split(':')[-1])
            tple_b = tple_b + (value,)

#    print tple_a
#    print tple_b
    res = ()
    # NOTE BIGRAM - TERM HERE!!!
    for i in range(0, len(tple_a)):
        res = res + ((tple_b[i] - tple_a[i]),)

    return res

def concat(line_a, line_b):
    tple_a = ()
    tple_b = ()
    part_a = line_a.strip().split('#',1)[0].split(' ')
    part_b = line_b.strip().split('#',1)[0].split(' ')
    for part in part_a:
        if ':' in part:
            value = float(part.split(':')[-1])
            tple_a = tple_a + (value,)

    for part in part_b:
        if ':' in part:
            value = float(part.split(':')[-1])
            tple_b = tple_b + (value,)

#    print tple_a
#    print tple_b
    res = ()
    # NOTE FIRST BIGRAM AND THEN TERM HERE!!!
    for i in range(0, len(tple_b)):
        res = res + ((tple_b[i],))
        
    for i in range(0, len(tple_a)):
        res = res + ((tple_a[i],))

    return res

    
for k in d:
    size = len(d[k])
    for i in range(0,size):
        for j in range(i,size):
            if i!=j:
                line_a = d[k][i]
                line_b = d[k][j]

                part_a = line_a.split('\t')[-2]
                part_b = line_b.split('\t')[-2]
                if not part_a.startswith('#') and part_b.startswith('#'):
                    terms_b = part_b.split('(')[-1].split(')')[0].split(' ')
                    if part_a in terms_b:
                        res = concat(line_a, line_b)
                        for val in res:
                            B_out.write('%f ' % val)
                        B_out.write('\n')
                    
                if part_a.startswith('#1') and part_b.startswith('#uw'):
                    string_a = part_a.split('(')[-1].split(')')[0]
                    string_b = part_b.split('(')[-1].split(')')[0]
                    if string_a == string_b:
                        res = concat(line_a, line_b)
                        for val in res:
                            B_out.write('%f ' % val)
                        B_out.write('\n')

                
B_out.close()

