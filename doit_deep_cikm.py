##==========================================================================
 # Copyright (c) 2014 Carnegie Mellon University.  All Rights Reserved.
 #
 # Use of the Lemur Toolkit for Language Modeling and Information Retrieval
 # is subject to the terms of the software license set forth in the LICENSE
 # file included with this software (and below), and also available at
 # http://www.lemurproject.org/license.html
 #
##==========================================================================

import os
import sys
from query_term_feature_le import *
from time import strftime
from Constants import *

def prepare_svm_file(qtfs_folder, qids, filename):
    with open(filename, 'w') as svm_out:
        for qid in qids:
            ifilename = '%s/q%d.desc.svm' %(qtfs_folder, qid)
            if not os.path.exists(ifilename):
                continue

            with open(ifilename, 'r') as ifile:
                for line in ifile:
                    svm_out.write('%s\n' % line.strip())


def tid2range(tid):
    if tid==21:
        return range(2001, 2100)
    if tid==22:
        return range(2101, 2201)
    
    if tid==35:
        return range(151, 301)
    if tid==37:
        return range(151, 401)
    if tid==39:
        return range(151, 501)

    if tid==13 or tid==14:
        tid+=1

    return range(tid*50+1, tid*50 + 51)

def tid2range2(tid):
    if tid==7:
        return range(351, 431) + range(441,451)
    if tid==8: 
        return range(431, 441)

def get_test_tid(tid):
    if tid==35:
        return 6
    if tid==37:
        return 8
    if tid==39:
        return 10
    if tid==8:
        return 6
    else:
        return tid+1

def get_test_tid2(tid):
    if tid==35:
        return 6
    if tid==37:
        return 8
    if tid==39:
        return 10
    else:
        return tid

def getTTFbdocs(test_tid):
    if test_tid ==3:
        return [300]
    elif test_tid==7:
        return [150]
    elif test_tid==9:
        return [250]
    elif test_tid==11:
        return [600]
    elif test_tid==35:
        return [300]
    elif test_tid==37:
        return [150]
    elif test_tid==39:
        return [250]

def get_all_qids(dataset):
    if dataset == 'robust04':
        return range(301, 451) + range(601, 701)
    elif dataset == 'wt10g':
        return range(451, 551)
    elif dataset == 'gov2':
        return range(701, 851)
    elif dataset == 'clueweb09b':
        return range(2001, 2201)

if __name__ == '__main__':
    if len(sys.argv)!= 5:
        print 'Usage: %s <qtfs_folder> <tmp_foler> <QL|SD> <LM|BM25>' % sys.argv[0]
        exit(0)

    qtfs_folder = sys.argv[1]
    tmp_folder = sys.argv[2]
    query_model = sys.argv[3]
    retrieval_model = sys.argv[4]

    if (query_model!= 'QL' and query_model != 'SD') or (retrieval_model != 'LM' and retrieval_model !='BM25'):
        print 'Usage: %s <qtfs_folder> <tmp_foler> <QL|SD> <LM|BM25>' % sys.argv[0]
        exit(0)

    for trecno in ['robust04', 'wt10g', 'gov2', 'clueweb09b']:
        if HAS_CONDOR: # has condor for parallel computing
            jobstr = '%s/%s.%s' %(tmp_folder, trecno, strftime('%Y%m%d'))
            jobname = '%s.job' % jobstr
            f = open(jobname, 'w')
            f.write('Universe = vanilla\n')
            f.write('initialdir = ./\n')
            f.write('executable = %s\n' % PYTHON27)
            f.write('arguments = deep_cikm_condor.py %s %s %s %s %s\n'%(trecno, query_model, retrieval_model, qtfs_folder, tmp_folder))
            f.write('output = '+jobstr+'.out\n')
            f.write('log = '+jobstr+'.log\n')
            f.write('error = '+jobstr+'.err\n')
            f.write('queue\n')
            f.close()
            os.system('condor_submit '+ jobname)
        else: # otherwise do it sequentially
            cmd = '%s deep_cikm_condor.py %s %s %s %s %s\n'%(PYTHON27, trecno, query_model, retrieval_model, qtfs_folder, tmp_folder)
            os.system(cmd)
            
