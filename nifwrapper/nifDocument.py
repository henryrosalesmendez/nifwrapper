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
    
    def getSortedIndexSentences(self):
        print(self.dictS)
        return []
    
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
        text = self.getText()
        ntext = len(text) 
        s =     standarURI(self.uri, 0, ntext) + "\n        a nif:String , nif:Context  , nif:RFC5147String ;\n"
        s = s + '        nif:isString """%s"""^^xsd:string ;\n'%(text)       
        s = s + attr2nif(self.attr, set(["nif:isString"]))
        s = s + "\n"
        
        for idsent in self.dictS:
            index = self.dictS[idsent]
            s = s + self.sentences[index].toString()
            s = s + "\n"
            
        return s
        
    
        
