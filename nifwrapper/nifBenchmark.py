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
        self.onlyER = False
        self.showWarnings = True
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
            
            if self.onlyER == True:
                if ((a.getIni() == x.getIni()) and (a.getFin() == x.getFin())):    
                    return i
            elif ((a.getIni() == x.getIni()) and (a.getFin() == x.getFin()) and 
               (set(a.getUrlShortList()).intersection(set(x.getUrlShortList()))!=set([]))):    
                return i
        return -1
    
    def trim(self, uri):
        return uri.split("#")[0]
    
    def contingenceTableByDocument(self): 
        T = []
        
        #tempDictD = dict([(self.trim(k),v) for k,v in self.system.dictD.items()])
        #tempDictS = dict([(self.trim(k),v) for k,v in self.system.dictD.items()])
        
        for doc_gold in self.gold.documents:
            if doc_gold.uri in self.system.dictD:
                doc_sys = self.system.documents[self.system.dictD[doc_gold.uri]]
                ####doc_sys = self.system.documents[tempDictS[self.trim(doc_gold.uri)]]
                ctt = self.contingenceTableBySentence(doc_gold, doc_sys)
                T.append(ctt)
            else:
                if self.showWarnings == True:
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
                if self.showWarnings == True:
                    print("[Error] sentence <"+sent_gold.uri+"> is not covered in the system results")
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
        if tp + fp == 0: return 0
        return (tp/(tp + fp))
        
    def R(self,tp,fp,fn):
        if tp + fn == 0: return 0
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
            #for o in t["tp"]:
            #    print(o.getAttribute("nif:anchorOf"))
            tp = tp + len(t["tp"])
            fp = fp + len(t["fp"])
            fn = fn + len(t["fn"])
        #print("_______________>",tp,fp,fn)
        p = self.P(tp,fp,fn)
        r = self.R(tp,fp,fn)
        f1 = self.F1(p,r)
        return {"precision":p, "recall":r, "f1":f1}#, "tp":T}
    

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
                #print("--->m:",m)
                if self.showWarnings == True:
                    print("[Error] No membership specification for annotation <"+uri+">")
        #print("summ:",summ)
        return summ
    
    
    #------
    # the membership values are stores in the field "membership"
    def sum_attr(self,st):
        summ = 0
        
        for a in st:
            uri = a.uri
            if "el:membership" in a.attr:
                summ = summ + float(a.getAttribute("el:membership"))
                #print("=>",a.getAttribute("nif:anchorOf"),m[uri])
            else:
                summ = summ + 1
                if self.showWarnings == True:
                    print("[Error] No membership specification for annotation <"+uri+">")
        return summ
            
    '''    
    def microExtF1(self, m=None):
        T = self.contingenceTableByDocument()
        tp = 0
        fp = 0
        fn = 0
        
        for t in T:
            #print("t:",T)
            #print("tp:",[x.getLabel() for x in t["tp"]])
            #print("fp:",[x.getLabel() for x in t["fp"]])
            #print("fn:",[x.getLabel() for x in t["fn"]])
            if m == None:
                s_tp = self.sum_attr(t["tp"])
            else:
                s_tp = self.sum_m(t["tp"],m)
            #print("---> self.sum_m(t['tp'],m):",s_tp)
            tp = tp + s_tp
            fp = fp + len(t["fp"])#self.sum_m(t["fp"],m)
            fn = fn + len(t["fn"])#self.sum_m(t["fn"],m)
        print("(tp,fp,fn):",(tp,fp,fn))
        p = self.P(tp,fp,fn)
        r = self.R(tp,fp,fn)
        f1 = self.F1(p,r)
        return {"precision":p, "recall":r, "f1":f1}
    '''
    
    
    def sumatoryA(self,A,m):
        if m == None and self.showWarnings == True:
            print("[WARNING] membership function is empty")
        
        R_ = 0
        for doc_g in A.documents:
            for sentence_g in doc_g.sentences:
                for ann_g in sentence_g.annotations:
                    #print("-----")
                    #print("->",ann_g.getAttribute("nif:anchorOf"))
                    if m == None:
                        #print("--None--")
                        if "el:membership" in ann_g.attr:
                            #print("SIII")
                            R_ = R_ + float(ann_g.getAttribute("el:membership"))
                        else:
                            #print("NOOO")
                            R_ = R_ + 1
                    elif ann_g.uri in m:
                        #print("tiene m = ",m[ann_g.uri])
                        R_ = R_ + m[ann_g.uri]
                        #print("=>",ann_g.getAttribute("nif:anchorOf"),m[ann_g.uri])
                    
        return R_
            
    '''
    def microExtF1(self, m=None):
        T = self.contingenceTableByDocument()
        tp = 0
        fp = 0
        fn = 0
        
        for t in T:
            if m == None:
                s_tp = self.sum_attr(t["tp"])
            else:
                s_tp = self.sum_m(t["tp"],m)
            tp = tp + s_tp

        sp = tp
        p = 0
        S = self.system.getCantAnnotations()
        if S != 0 and sp!=0:
            p = sp/S
        
        r = 0
        R = self.sumatoryA(self.gold,m)
        if R != 0 and sp!=0:
            r = sp/R
            
        f1 = self.F1(p,r)
        return {"precision":p, "recall":r, "f1":f1}
    '''
    
    
    def microExtF1(self, m=None):
        T = self.contingenceTableByDocument()
        tp = 0
        fp = 0
        fn = 0
        
        tp_hard = 0
        for t in T:
            if m == None:
                s_tp = self.sum_attr(t["tp"])
            else:
                s_tp = self.sum_m(t["tp"],m)
            tp_hard = tp_hard + len(t["tp"])
            tp = tp + s_tp

        #sp = tp
        sp = tp_hard
        p = 0
        S = self.system.getCantAnnotations()
        if S != 0 and sp!=0:
            #p = sp/S
            p = tp_hard/S
        #print("===========")
        #print("hard tp:",tp_hard)
        #print("S:",S)
        #print("Precisoin:",p)
        
        r = 0
        R = self.sumatoryA(self.gold,m)
        if R != 0 and sp!=0:
            #r = sp/R
            r = tp/R
        #print("soft_tp:",tp)
        #print("Gold:",R)
        #print("Recall:",r)
            
        f1 = self.F1(p,r)
        return {"precision":p, "recall":r, "f1":f1}
    

