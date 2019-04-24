#!/usr/bin/python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------------------------------
from .nifAnnotation import NIFAnnotation
from .nifUtils import attr2nif, standarURI
#------------------------------------------------------------------------------------------------------
class NIFSentence:
    """
    Here you can store the info about each sentence
    """    
    
    
    def __init__(self,_uri=None):
        if _uri!=None:
            self.uri = _uri
        self.annotations = []
        self.dictA = {}    
        self.attr = {}
    
    def setText(self, _text):
        self.addAttribute("nif:isString",_text,"xsd:string")
        
    def getIni(self):
        return self.getAttribute("nif:beginIndex");
    
    def getFin(self):
        return self.getAttribute("nif:endIndex");
    
    def setUri(self, _uri):
        self.uri = _uri
    
    def getUri(self):
        return self.uri
        
    def pushAnnotation(self,_ann):
        self.dictA[_ann.getUri()] = len(self.annotations)
        self.annotations.append(_ann)
    
    def getText(self):
        res = self.getAttribute("nif:isString")
        if res == None:
            return self.getAttribute("nif:anchorOf")
        return res
    
    def addAttribute(self,_name,_value,_type,_m = None):
        if _m != None and _name in _m:
            _name = _m[_name]
        self.attr[_name] = {}
        self.attr[_name]["value"] = _value
        self.attr[_name]["type"] = _type
        
    def getAttribute(self,_name):
        if _name in self.attr:
            return self.attr[_name]["value"]
        return None
    
    def findByPosition(self, pini, pfin):
        po = 0
        for a in self.annotations:
            if (a.getIni() == pini and a.getFin() == pfin):
                return po
            po = po + 1
        return -1
    
    
    def sorting(self):    
        #sorted_list = sorted(self.annotations, cmp = compare_ini_fin)
        #annotations = sorted_list
        
        ##self.annotations.sort(key=cmp_)
        self.annotations.sort(key = lambda x: float(str(x.getIni())+"."+str(x.getFin())))
        
        self.dictA = {} 
        pos = 0
        for ann in self.annotations:
            self.dictA[ann.uri] = pos
            pos = pos + 1
    
    def toString(self):
        ini = self.getIni()
        fin = self.getFin()
        
        if not ini or not fin:
            print("[Error]: Sentence <"+self.uri+"> with out ini/fin predicate")
            return ""
        
        s = standarURI(self.uri, ini, fin) + "\n        a nif:String , nif:Context  , nif:RFC5147String ;\n"
        s = s + attr2nif(self.attr, set([]))
        s = s + "\n"
        
        #print("---------")
        #print(self.attr)
        #print("..........")
        #input("entonces?")
        #print("self.dictA:",self.dictA)
        for idann in self.dictA:
            index = self.dictA[idann]
            #print("-->",idann,index)
            s = s + self.annotations[index].toString()
            s = s + "\n"
        return s
        
        
