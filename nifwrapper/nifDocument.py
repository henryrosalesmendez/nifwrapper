#!/usr/bin/python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------------------------------
from .nifSentence import NIFSentence
import copy
from .nifUtils import attr2nif, standarURI, compare_ini_fin
#------------------------------------------------------------------------------------------------------

class NIFDocument:
    """
    Here you can store the info about each document
    """    
    
    def __init__(self, _uri = None):
        if _uri!= None:
            self.uri = _uri
        self.sentences = []
        self.dictS = {}
        self.attr = {}
        self.addAlwaysPositionsToUriInSentence = True
        
    def setUri(self, _uri):
        self.uri = _uri
    
    def getUri(self):
        return self.uri
    
    def pushSentence(self, sent):
        self.dictS[sent.getUri()] = len(self.sentences)
        self.sentences.append(sent)
    
    def addAttribute(self,_name,_value,_type):
        self.attr[_name] = {}
        self.attr[_name]["value"] = _value
        self.attr[_name]["type"] = _type
    
    def getAttribute(self,_name):
        if _name in self.attr:
            return self.attr[_name]["value"]
        return None
    
    def findByPosition(self, pini, pfin):
        po = 0
        for s in self.sentences:
            if (int(s.getIni()) == int(pini) and int(s.getFin()) == int(pfin)):
                return po
            po = po + 1
        return -1
    
    #def getSortedIndexSentences(self):
    #    print(self.dictS)
    #    return []
    
    def getText(self):
        txt = ""
        for idsent in self.dictS:
            index = self.dictS[idsent]
            txt = txt + self.sentences[index].getText() + " "
        return txt
    
    def sorting(self):    
        #sorted_list = sorted(self.sentences, cmp = compare_ini_fin)
        ##self.sentences.sort(key=cmp_)
        self.sentences.sort(key = lambda x: float(str(x.getIni())+"."+str(x.getFin())))
        #sentences = sorted_list
        
        for sent in self.sentences:
            sent.sorting()
            
        self.dictS = {} 
        pos = 0
        for sent in self.sentences:
            self.dictS[sent.uri] = pos
            pos = pos + 1
        
    
    
    def toString(self):
        
        if self.getAttribute("nif:sourceUrl") == None:
            self.addAttribute("nif:sourceUrl", [self.uri], "URI LIST");
        
        text = self.getText()
        ntext = len(text) 
        s =     standarURI(self.uri, 0, ntext) + "\n        a nif:String , nif:Context  , nif:RFC5147String ;\n"
        s = s + '        nif:isString """%s"""^^xsd:string ;\n'%(text)       
        s = s + attr2nif(self.attr, set(["nif:isString"]))
        s = s + "\n"
        
        for idsent in self.dictS:
            index = self.dictS[idsent]
            self.sentences[index].addAlwaysPositionsToUriInSentence = self.addAlwaysPositionsToUriInSentence
            s = s + self.sentences[index].toString()
            s = s + "\n"
            
        return s
    
    
    
    # Annotation where are stored with the start/end positions according to their sentences. 
    # A dictionary D = {(pos_initial, post_end):"label", ...} is returned in this method containing all the 
    # annotation of this document
    def getAnnotationDict(self, targetTag=None):
        D = {}
        for idsent in self.dictS:
            sent_ = self.sentences[self.dictS[idsent]]
            sent_ini = int(sent_.getIni())
            sent_fin = int(sent_.getFin())

            for idann in sent_.dictA:
                ann_ = sent_.annotations[sent_.dictA[idann]]
                if targetTag:
                    if "itsrdf:taClassRef" in ann_.attr  and  not targetTag in set(ann_.attr["itsrdf:taClassRef"]["value"]):
                        continue

                p = tuple([sent_ini + int(ann_.getIni()), sent_ini + int(ann_.getFin())])
                if not p in D:
                    D[p] = ann_.getAttribute("nif:anchorOf")

                
        return D
    
    
    
    
        
