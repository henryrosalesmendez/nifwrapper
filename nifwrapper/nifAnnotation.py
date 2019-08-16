#!/usr/bin/python3
# -*- coding: utf-8 -*-
    
#------------------------------------------------------------------------------------------------------
from .nifUtils import standarURI, attr2nif, uriShort
#------------------------------------------------------------------------------------------------------
class NIFAnnotation:
    """
    Here you can store the info about each annotation
    """
    
    
    def __init__(self):
        self.attr = {}  # other attributes -- {"attrNam1":  {  "value": "val" , "type":"xsd:string"    } , ...        }
        self.uri = ""
    
    def __init__(self, _uri = None,_ini=None, _fin=None, _uriList=None, _tag=None):
        self.attr = {}  # other attributes -- {"attrNam1":  {  "value": "val" , "type":"xsd:string"    } , ...        }
        self.uri = ""
        if _uri!=None:   self.uri = _uri        
        if _ini!=None:    self.addAttribute("nif:beginIndex",_ini,"xsd:nonNegativeInteger")
        if _fin!=None:   self.addAttribute("nif:endIndex",_fin,"xsd:nonNegativeInteger")
        if _uriList!=None: self.addAttribute("itsrdf:taIdentRef",_uriList,"URI LIST")
        if _tag!=None:   self.addAttribute("itsrdf:taClassRef",_tag,"TAG LIST")
    
    
    def addAttribute(self,_name,_value,_type,_m=None):
        if _m!= None and _name in _m:
            _name = _m[_name]
        self.attr[_name] = {}
        self.attr[_name]["value"] = _value
        self.attr[_name]["type"] = _type
    
    def getAttribute(self,_name):
        if _name in self.attr:
            return self.attr[_name]["value"]
        return None
    
    def getUri(self):
        return self.uri;
        
    def getIni(self):
        return self.getAttribute("nif:beginIndex");
    
    def getFin(self):
        return self.getAttribute("nif:endIndex");
    
    def getUrlList(self):
        return self.getAttribute("itsrdf:taIdentRef");
    
    def getUrlShortList(self):
        L = self.getAttribute("itsrdf:taIdentRef")
        return [uriShort(x) for x in L]
    
    def getTagList(self):
        return self.getAttribute("itsrdf:taClassRef")
    
    def toString(self, passedValues = None):
        ini = self.getIni()
        fin = self.getFin()
        
        if not ini or not fin:
            print("[Error]: Annotation <"+self.uri+"> with out ini/fin predicate")
            return ""
        
        s = standarURI(self.uri, ini, fin) + "\n        a nif:String , nif:Context , nif:Phrase , nif:RFC5147String ;\n"   
        s = s + attr2nif(self.attr, set([]), passedValues)
        
        return s

        
         
