#!/usr/bin/python3
# -*- coding: utf-8 -*-

from .nifWrapper import NIFWrapper
from .nifAnnotation import NIFAnnotation
from .nifSentence import NIFSentence
from .nifDocument import NIFDocument
from .nifUtils import * 
from .nifParser import NIFParser


class NIFBenchmark:
    
    def __init__(self, _system=None, _gold=None): 
        if _system != None:
            self.setSystemResult(_system)
        
        if _gold != None:
            self.setGold(_gold)        
    
    def setSystemResult(self, _system):
        if _system.__class__.__name__ == "NIFWrapper":
            self.system = _system
        else:
            print("[Error] We expected an instance of NIFWrapper but we got "+_system.__class__.__name__)    
    
    def setGold(self, _gold):
        if _gold.__class__.__name__ == "NIFWrapper":
            self.gold = _gold
        else:
            print("[Error] We expected an instance of NIFWrapper but we got "+_gold.__class__.__name__)
    
    #----
    def findMatch(self,x,A):
        for i in range(len(A)):
            a = A[i]
            
            #print("/////")
            #print(a.getAttribute("nif:anchorOf"),": ",a.getUrlList())
            #print(x.getAttribute("nif:anchorOf"),": ",x.getUrlList())
            #print("....................> interseccion:",set(a.getUrlList()).intersection(set(x.getUrlList())) )
            #print("\\\\\\\\")
            
            if ((a.getIni() == x.getIni()) and (a.getFin() == x.getFin()) and 
               (set(a.getUrlList()).intersection(set(x.getUrlList()))!=set([]))):
                
                return i
        return -1
    
    
    def contingenceTableByDocument(self): 
        T = []
        for doc_gold in self.gold.documents:
            #print("-->doc_gold.uri:",doc_gold.uri)
            if doc_gold.uri in self.system.dictD:
                doc_sys = self.system.documents[self.system.dictD[doc_gold.uri]]
                ctt = self.contingenceTableBySentence(doc_gold, doc_sys)
                #print("tp:",len(ctt["tp"]), "fp:",len(ctt["fp"]), "fn:",len(ctt["fn"]))
                T.append(ctt)
            else:
                print("[Error] document <"+doc_gold.uri+"> is not covered in the system results")
        
        return T
    
    
    def contingenceTableBySentence(self, d_gold, d_syst):      
        tp = []
        fp = []
        fn = []
        
        for sent_gold in d_gold.sentences:
            if sent_gold.uri in d_syst.dictS:
                sent_sys = d_syst.sentences[d_syst.dictS[sent_gold.uri]]
                cont = self.contingenceTable(sent_gold, sent_sys)
                tp = tp + cont["tp"]
                fp = fp + cont["fp"]
                fn = fn + cont["fn"]
            else:
                print("[Error] document <"+sent_gold.uri+"> is not covered in the system results")
        return {"tp":tp,"fp":fp, "fn":fn}
    
    def contingenceTable(self, s_gold, s_syst):
        tp = []
        fp = []
        fn = []
        
        temp_s = [x for x in s_syst.annotations]
        
        for g in s_gold.annotations:
            p = self.findMatch(g,temp_s)
            #print("---->",g.getAttribute("nif:anchorOf"),p)
            if p == -1:
                fn.append(g)
            else:
                tp.append(g)
                temp_s[p:p+1] = []
        fp = temp_s
        return {"tp":tp,"fp":fp, "fn":fn}
    
    #----
    
    def P(self,tp,fp,fn):
        return (tp/(tp + fp))
        
    def R(self,tp,fp,fn):
        return (tp/(tp + fn))
    
    def F1(self,p,r):
        if p + r == 0: return 0.0
        return 2*p*r/(p + r)
    
    def microF(self):
        T = self.contingenceTableByDocument()
        tp = 0
        fp = 0
        fn = 0
        
        for t in T:
            #print("t:",T)
            tp = tp + len(t["tp"])
            fp = fp + len(t["fp"])
            fn = fn + len(t["fn"])
        #print(tp,fp,fn)
        p = self.P(tp,fp,fn)
        r = self.R(tp,fp,fn)
        f1 = self.F1(p,r)
        return {"precision":p, "recall":r, "f1":f1}
    

    #------
    # 'm' is the membership function, e.g., m = {"http://ex.org/ann1":0.2, ...}
    def sum_m(self,st,m):
        summ = 0
        
        for s in st:
            uri = s.uri
            if uri in m:
                summ = summ + m[uri]
                #print("=>",s.getAttribute("nif:anchorOf"),m[uri])
            else:
                summ = summ + 1
                print("[Error] No membership specification for annotation <"+uri+">")
        #print("summ:",summ)
        return summ
            
        
    def microFEL(self, m):
        T = self.contingenceTableByDocument()
        tp = 0
        fp = 0
        fn = 0
        
        for t in T:
            #print("t:",T)
            #print("tp:",[x.getLabel() for x in t["tp"]])
            #print("fp:",[x.getLabel() for x in t["fp"]])
            #print("fn:",[x.getLabel() for x in t["fn"]])
            s_tp = self.sum_m(t["tp"],m)
            #print("---> self.sum_m(t['tp'],m):",s_tp)
            tp = tp + s_tp
            fp = fp + len(t["fp"])#self.sum_m(t["fp"],m)
            fn = fn + len(t["fn"])#self.sum_m(t["fn"],m)
        #print("(tp,fp,fn):",(tp,fp,fn))
        p = self.P(tp,fp,fn)
        r = self.R(tp,fp,fn)
        f1 = self.F1(p,r)
        return {"precision":p, "recall":r, "f1":f1}
    

