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
import subprocess
from Constants import *
from doit_deep_cikm import prepare_svm_file
from doit_deep_cikm import get_all_qids

def get_trec_id(trec_str):
    if trec_str == 'robust04':
        return 7
    elif trec_str == 'wt10g':
        return 9
    elif trec_str == 'gov2':
        return 13
    elif trec_str == 'clueweb09b':
        return 21

if len(sys.argv)!=6:
    print 'Usage: %s <trec_str> <QL|SD> <LM|BM25> <qtfs_folder> <tmp_folder>' % sys.argv[0]
    exit(0)

trec_str = sys.argv[1]
trecid = get_trec_id(trec_str.strip())

query_model = sys.argv[2]
retrieval_model = sys.argv[3]

if (query_model!= 'QL' and query_model != 'SD') or (retrieval_model != 'LM' and retrieval_model !='BM25'):
    print 'Usage: %s <trec_str> <QL|SD> <LM|BM25> <qtfs_folder> <tmp_folder>' % sys.argv[0]
    exit(0)


qtfs_folder = sys.argv[4]
tmp_folder = sys.argv[5]

all_qids = get_all_qids(trec_str)


nfold = 5

foldsize = len(all_qids) / nfold

folds =[]
res_file = '%s/%s.res' % (tmp_folder, trec_str)
query_file = '%s/%s.q' % (tmp_folder, trec_str)

os.system(' > %s' % res_file)
os.system(' > %s' % query_file)

for i in range(0, nfold):
    test_qids = all_qids[i*foldsize:(i+1)*foldsize]
    train_qids = all_qids[:i*foldsize] + all_qids[(i+1)*foldsize:]

    train_file = '%s/%s.fold%d.train.svm' % (tmp_folder, trec_str, (i+1))
    test_file  = '%s/%s.fold%d.test.svm' %  (tmp_folder, trec_str, (i+1))

    prepare_svm_file(qtfs_folder, train_qids, train_file)
    prepare_svm_file(qtfs_folder, test_qids,  test_file)

    os.system(PYTHON27 + ' svm2mtb_complete.py %s' % (train_file))
    os.system(PYTHON27 + ' svm2mtb_complete.py %s' % (test_file))

    #lasso regression with deep features
    command = MATLAB + ' -nodesktop -nojvm -singleCompThread -nosplash -r \"deep_lasso(\'%s.A\', \'%s.y\', \'%s.A\', \'%s.y\')\"' %(train_file, train_file, test_file, test_file)

    os.system(command)

    prefix = '%s.%s' % (train_file, test_file.split('/')[-1])

    if query_model == 'QL' and retrieval_model == 'LM':
        # weighted keyword query
        os.system(PYTHON27 + ' wqg_P_SIGIR.py %s %s.A.%s.A.out desc_parts_stopped %s.q' %(test_file, train_file, test_file.split('/')[-1], prefix))

    elif query_model == 'SD' and retrieval_model == 'LM':
        # deep weighted sd - (unigrams weighted only)
        os.system(PYTHON27 + ' wqg_P_mixed_deep.py %s %s.A.%s.A.out desc_parts_stopped %s.q' %(test_file, train_file, test_file.split('/')[-1],  prefix))

    elif query_model == 'QL' and retrieval_model == 'BM25':
        # generate BM25 queries (P(t|R) needs to be absored in weight -> see BM25 retrieval fuction)
        os.system(PYTHON27 + ' wqg_P_BM25.py %s %s.A.%s.A.out desc_parts_stopped %s.q' %(test_file, train_file, test_file.split('/')[-1], prefix))

    elif query_model == 'SD' and retrieval_model == 'BM25':
        # deep weighted sd - (unigrams weighted only for BM25)
        os.system(PYTHON27 + ' wqg_P_mixed_deep_BM25.py %s %s.A.%s.A.out desc_parts_stopped %s.q' %(test_file, train_file, test_file.split('/')[-1],  prefix))


    if retrieval_model == 'LM':
        # indri 5.3 for LM
        os.system(INDRIRUNQUERY + ' -count=1000 %s.%s.q -index=%s/indext%d-v5.3/ -trecFormat=t -rule=method:d,mu:2500 > %s.res' %(train_file, test_file.split('/')[-1], INDICES_PREFIX, trecid, prefix))

    elif retrieval_model == 'BM25':
        #indri 5.3 for BM25 
        os.system(INDRIRUNQUERY + ' -count=1000 %s.%s.q -index=%s/indext%d-v5.3/ -trecFormat=t -rule=method:okapi > %s.res' %(train_file, test_file.split('/')[-1], INDICES_PREFIX, trecid, prefix))
        

    os.system('cat %s.res >> %s' % (prefix, res_file))
    os.system('cat %s.q >> %s' % (prefix, query_file))

#eval_output_test = subprocess.check_output(('./trec_eval ../qrels/qrels.t%d.txt %s.res' %(trecid, prefix)).split(' '))
#eval_map_test = float(eval_output_test.strip().split('\n')[5].split('\t')[-1])
#eval_p10_test = float(eval_output_test.strip().split('\n')[22].split('\t')[-1])

# significance test
qrel_cmd = './trec_eval -q ./qrels/qrels.%s.txt %s > %s.eval' % (trec_str, res_file, res_file)
os.system(qrel_cmd)
