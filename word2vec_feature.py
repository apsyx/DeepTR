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
import gensim
import glob
from collections import defaultdict

def query_inrange(qid):
    if qid >= 301 and qid <=550:
        return True

    if qid >= 601 and qid <= 850:
        return True

    if qid >=2001 and qid <= 2200:
        return True

    return False

def compute_rep_feat_mean(rep_list, mean_list):
    feats = []
    for i in range(0, len(rep_list)):
        feats.append(rep_list[i] - mean_list[i]);
            
    return feats

if len(sys.argv)!=5:
    print 'Usage: %s <model.bin> <vector_dim> <output_dir> <do_phrases?>' % sys.argv[0]
    print 'Generate all features for parts in query_desc_parts dir.'
    exit(0)

model_file = sys.argv[1]
vector_dim = int(sys.argv[2])
output_dir = sys.argv[3]
do_phrase = False

if int(sys.argv[4])==1:
    do_phrase = True

# load model
print 'Loading model %s ...' % model_file
#model = gensim.models.Word2Vec.load_word2vec_format('word2vec/GoogleNews-vectors-negative300.bin', binary=True)
model = gensim.models.Word2Vec.load_word2vec_format('%s'% model_file, binary=True)
print 'Loading model done.'

for filename in glob.glob('true_recalls/q*.desc.true.recall'):
    terms = []
    qid = int(filename.split('/')[-1].split('.')[0].split('q')[-1])
    if not query_inrange(qid):
        continue

    reps = defaultdict(list)
    
    term2svmpart = dict()
    term2recall = dict()

    with open(filename, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            true_recall = float(line.strip().split(' ')[0])
            svmpart = line.strip().split('#', 1)[-1]
            term = parts[-2].strip() 
            if not term.startswith('#'): # unigram
                terms.append(term)
                term2svmpart[term] = svmpart
                term2recall[term] = true_recall
            elif do_phrase: # do if do_phrase  is True
                terms.append(term)
                term2svmpart[term] = svmpart
                term2recall[term] = true_recall

    mean_rep = []
    for i in range(0, vector_dim):
        mean_rep.append(0)

    output_terms = [] # store the terms which has word vector mappings
    output_terms_set = set()
    for term in terms:
        if 'GoogleNews-vectors-negative300.bin' in model_file: # google vectors are case sensitive
            term_to_check = term
        else:
            term_to_check = term.lower()                       # others vectors (trained on TREC corpora) are all lower cased!!!
        if term_to_check.startswith('#'):
            term_to_check = term_to_check.split('(')[-1].split(')')[0]
            term_to_check = '_'.join(term_to_check.split())
        rep = None
        try:
            rep = model[term_to_check]
        except KeyError:
            print 'KEY ERROR FOR :', term_to_check, 'abandoned.'

            
            ''' #ignore terms that has no vector mapping
            rep = []
            for i in range(0, 300):
                rep.append(0)
            '''

        if rep!=None:
            reps[term] = rep
            output_terms.append(term)
            
            if term_to_check not in output_terms_set:
                for i in range(0, vector_dim):
                    mean_rep[i] += rep[i]

            output_terms_set.add(term_to_check)

    if len(output_terms) > 0:
        for i in range(0, vector_dim):
            mean_rep[i] = mean_rep[i] / len(output_terms_set)

    outputfilename = '%s/%s.desc.svm' % (output_dir, filename.split('/')[-1].split('.')[0])
    print outputfilename
                                
    with open(outputfilename, 'w') as w:
        for term in output_terms:
            recall = term2recall[term]
            svmpart = term2svmpart[term]
            feats = compute_rep_feat_mean(reps[term], mean_rep)
            
            w.write('%f '% recall)
            feat_id = 1
            for value in feats:
                w.write('%d:%f ' % (feat_id, value))
                feat_id +=1
                
            w.write('#%s\n' % (svmpart))



                
            
    


