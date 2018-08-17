##==========================================================================
 # Copyright (c) 2014 Carnegie Mellon University.  All Rights Reserved.
 #
 # Use of the Lemur Toolkit for Language Modeling and Information Retrieval
 # is subject to the terms of the software license set forth in the LICENSE
 # file included with this software (and below), and also available at
 # http://www.lemurproject.org/license.html
 #
##==========================================================================

#!/bin/bash

# Start modifying the hardcoded variables here
# directory for storing the feature outputs
QTFS_PREFIX="qtfs"

# necessary tmp directory for the experiments
TMP_PREFIX="tmp"

# names for word vectors
vectors=("trec7")
# "wt10g" "gov2" "clueweb100" "clueweb300" "clueweb500" "google300")

# model locations
models=("/bos/tmp17/USERID/trec7-300.bin")
# "/bos/tmp17/USERID/wt10g-300.bin" "/bos/tmp17/USERID/gov2-new-300.bin" "/bos/tmp17/USERID/clueweb09b-new-100.bin" "/bos/tmp17/USERID/clueweb09b-new-300.bin" "/bos/tmp17/USERID/clueweb09b-new-500.bin" "/bos/usr0/USERID/TermRecall/src/word2vec/GoogleNews-vectors-negative300.bin")

# dimensions of word vectors
dims=(300 300 300 100 300 500 300)
# End modifying the hardcoded variables here

# make up all the directories and generate the features
for ((i=0;i<${#vectors[@]};i++))
do
    vector=${vectors[$i]}
    mkdir -p ${QTFS_PREFIX}-${vector}
    model=${models[$i]}
    dim=${dims[$i]}
    python2 word2vec_feature.py ${model} ${dim} ${QTFS_PREFIX}-${vector} 0

    mkdir -p ${TMP_PREFIX}-${vector}
    mkdir -p ${TMP_PREFIX}-${vector}_mix
    mkdir -p ${TMP_PREFIX}-${vector}_bm25
    mkdir -p ${TMP_PREFIX}-${vector}_mix_bm25
done
