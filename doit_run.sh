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

QTFS_PREFIX="qtfs"
TMP_PREFIX="tmp"

# for google 300
python doit_deep_cikm.py ${QTFS_PREFIX}-google300 ${TMP_PREFIX}-google300 QL LM
python doit_deep_cikm.py ${QTFS_PREFIX}-google300 ${TMP_PREFIX}-google300_mix SD LM
python doit_deep_cikm.py ${QTFS_PREFIX}-google300 ${TMP_PREFIX}-google300_bm25 QL BM25
python doit_deep_cikm.py ${QTFS_PREFIX}-google300 ${TMP_PREFIX}-google300_mix_bm25 SD BM25

# for clueweb 100
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb100 ${TMP_PREFIX}-clueweb100 QL LM
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb100 ${TMP_PREFIX}-clueweb100_mix SD LM
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb100 ${TMP_PREFIX}-clueweb100_bm25 QL BM25
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb100 ${TMP_PREFIX}-clueweb100_mix_bm25 SD BM25

# for clueweb 300
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb300 ${TMP_PREFIX}-clueweb300 QL LM
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb300 ${TMP_PREFIX}-clueweb300_mix SD LM
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb300 ${TMP_PREFIX}-clueweb300_bm25 QL BM25
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb300 ${TMP_PREFIX}-clueweb300_mix_bm25 SD BM25

# for clueweb 500
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb500 ${TMP_PREFIX}-clueweb500 QL LM
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb500 ${TMP_PREFIX}-clueweb500_mix SD LM
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb500 ${TMP_PREFIX}-clueweb500_bm25 QL BM25
python doit_deep_cikm.py ${QTFS_PREFIX}-clueweb500 ${TMP_PREFIX}-clueweb500_mix_bm25 SD BM25

# for trec7
python doit_deep_cikm.py ${QTFS_PREFIX}-trec7 ${TMP_PREFIX}-trec7 QL LM
python doit_deep_cikm.py ${QTFS_PREFIX}-trec7 ${TMP_PREFIX}-trec7_mix SD LM
python doit_deep_cikm.py ${QTFS_PREFIX}-trec7 ${TMP_PREFIX}-trec7_bm25 QL BM25
python doit_deep_cikm.py ${QTFS_PREFIX}-trec7 ${TMP_PREFIX}-trec7_mix_bm25 SD BM25

# for wt10g
python doit_deep_cikm.py ${QTFS_PREFIX}-wt10g ${TMP_PREFIX}-wt10g QL LM
python doit_deep_cikm.py ${QTFS_PREFIX}-wt10g ${TMP_PREFIX}-wt10g_mix SD LM
python doit_deep_cikm.py ${QTFS_PREFIX}-wt10g ${TMP_PREFIX}-wt10g_bm25 QL BM25
python doit_deep_cikm.py ${QTFS_PREFIX}-wt10g ${TMP_PREFIX}-wt10g_mix_bm25 SD BM25

# for gov2
python doit_deep_cikm.py ${QTFS_PREFIX}-gov2 ${TMP_PREFIX}-gov2 QL LM
python doit_deep_cikm.py ${QTFS_PREFIX}-gov2 ${TMP_PREFIX}-gov2_mix SD LM
python doit_deep_cikm.py ${QTFS_PREFIX}-gov2 ${TMP_PREFIX}-gov2_bm25 QL BM25
python doit_deep_cikm.py ${QTFS_PREFIX}-gov2 ${TMP_PREFIX}-gov2_mix_bm25 SD BM25

