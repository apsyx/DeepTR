## Code for "Learning to Reweight Terms with Distributional Representations"

#### 0. Overview

   This file contains instructions, data sets, and tools to run the
   model presented in the paper [Learning to Reweight Terms with
   Distributional Representations](https://dl.acm.org/citation.cfm?id=2767700) (published at SIGIR 2015).

#### 1. Software dependencies:
   
   In order to run the tool, the following prerequisites must be
      installed: 

      a) Python 2 
      b) Indri 5.3 or later 
      c) word2vec 
      d) Matlab 
      e) Python 2 packages:
         gensim
         numpy
         scipy


#### 2. How to run the tool:

   *** Before running the tools, make sure to modify the variables for
   dependency tools and paths in Constants.py. ***

   See detailed comments in Constnts.py for the switches;

   We provide info processed TREC queries from ROBUST04, WT10G, GOV2
   and CLUEWEB09B, distributed under the following directories:

     * true_recalls: stores the ground truth recall for query terms for model traning

     * desc_parts_stopped: stores the processed query parts from those queries

   The tools supports running on Condor or single machine mode, just
   set HAS_CONDOR to be FALSE

   There are two major steps involved of using the tool:
   
   a) Computer features for terms in all queries over all
   collections. The entry for this is
   
        doit_features.sh

   To be able to run this step, the corresponding binary files for
   trained word vectors must be in place and paths be set right in
   doit_features.sh. (such as the Google vectors, vectors trained on
   GOV2 and WT10g)

   b) Use the constructed feature files for query terms to train and
   evaluate the term recall prediction model. The entry for this is
      
        doit_latest.sh

   To be able to run this step and get evaluation results, the Indri
   indices for (robust04, wt10g, gov2 and clueweb09b) must be in place
   with their paths set correctly. The name of the index must be:
        ROBUST04:   indext7-v5.3  (also make a symbolic link indext8-v5.3 to it)
        WT10G:      indext9-v5.3  (also make a symbolic link indext10-v5.3 to it)
        GOV2:       indext13-v5.3 (also make a symbolic link indext14-v5.3 to it)
        CLUEWEB09B: indext21-v5.3 (also make a symbolic link indext22-v5.3 to it)
   
   Also make sure the qrels files for all these dataset are under directory "qrels"        

#### 3. Collect the results:
   
   The retrieved documents will be stored in tmp-METHOD directories,
   with METHOD referring to different ways of constructing the query
   with the predicted weights. Also evaluation results from trec_eval
   will be stored in those directories (need trec_eval to be in current
   directory first)


If you use this code or our results in your research, please cite as appropriate:

```
@inproceedings{zheng2015learning,
  title={Learning to reweight terms with distributed representations},
  author={Zheng, Guoqing and Callan, Jamie},
  booktitle={Proceedings of the 38th international ACM SIGIR conference on research and development in information retrieval},
  pages={575--584},
  year={2015},
  organization={ACM}
}
```

Guoqing Zheng, 2015
** Please report questions and bugs to gzheng@cs.cmu.edu **

