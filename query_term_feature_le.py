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
import glob
import sys
from Constants import * 

def trecid2qids(trecid):
    if trecid>=13:
        trecid+=1
    
    return range(trecid*50+1,trecid*50+51)

def getMu(trecid):
    if trecid<=8:
        return [900,1500]
    elif trecid<=10:
        return [1500]
    elif trecid<=12:
        return [900]

def getFbdocs(trecid, mu):
    if trecid<=8:
        if mu==900:
            return [500, 120, 130, 140,150,160,170,180,190,200,250,300,400]
        else:
            return [300, 120, 130, 140,150,160,170,180,190,200,250]
    elif trecid<=10:
        if mu==900:
            return [200, 120, 130, 140,150,160,170,180,190]
        else:
            return [300, 120, 130, 140,150,160,170,180,190,200,250]
    elif trecid<=12:
        return [700, 300, 400, 500, 600]

if __name__ == '__main__':
    for trecno in range(3,13):
    #for trecno in range(13,15):
        for qid in trecid2qids(trecno):
            for mu in getMu(trecno):
                for fbdoc in getFbdocs(trecno, mu):
                    for svddim in [150]:
                        filename = '../qtfs/q%d.okw.desc.mu%d.fbdocs%d.svddim%d.svm'%(qid,mu,fbdoc,svddim)
                        if not os.path.exists(filename):
                            print filename
                            jobstr =  'q%d.okw.desc.mu%d.fbdocs%d.svddim%d.svm'%(qid,mu,fbdoc,svddim)
                            jobname = ".jobs/"+jobstr+".job"
                            f = open(jobname, "w")
                            f.write("Universe = vanilla\n")
                            f.write("initialdir = /bos/usr2/gzheng/TermRecall/src\n")
                            f.write("executable = query_term_feature_gen\n")
                            if trecno <=4:
                                f.write("arguments = " + str(qid) + " /bos/usr2/gzheng/Boolean/res/t" + str(trecno)+".okw.mu"+str(mu)+".res " + str(fbdoc) + " " + str(svddim) + " "+filename+"\n")
                            else:
                                f.write("arguments = " + str(qid) + " /bos/usr2/gzheng/Boolean/res/t" + str(trecno)+".okw.desc.mu"+str(mu)+".res " + str(fbdoc) + " " + str(svddim) + " "+filename+"\n")
                            f.write("output = .jobs/"+jobstr+".out\n")
                            f.write("log = .jobs/"+jobstr+".log\n")
                            f.write("error = .jobs/"+jobstr+".err\n")
                            f.write("queue\n")
                            f.close()
                            os.system("condor_submit "+ jobname)
                    
