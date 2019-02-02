#!/usr/bin/python3
# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------------------------------
from .nifDocument import NIFDocument

#------------------------------------------------------------------------------------------------------
class NIFWrapper:
    """
    Here, you can handle your NIF corpora. NIFWrapper is the class that will store the sets of document.
    """

    def __init__(self):
        self.documents = []
        self.dictD = {}
        self.prefix = {}

    def setPrefix(self, _prefix):
        self.prefix = _prefix
        
    def pushDocument(self,_doc):
        self.dictD[_doc.getUri()] = len(self.documents)
        self.documents.append(_doc)
        
    def sorting(self):
        for d in self.documents:
            d.sorting()
        
        self.dictD = {} 
        pos = 0
        for d in self.documents:
            self.dictD[d.uri] = pos
            pos = pos + 1
            
            

            
            
            
    
    def toString(self):
        s = ""
        for p in self.prefix:
            s = s + "@prefix %s: %s .\n"%(p,self.prefix[p])
        s = s + "\n"
        
        
        for d in self.documents:
            s = s + d.toString()
            s = s + "\n"
        
        return s
    


'''
#------------------------------------------------------------------------------------------------------

'''


    

#wrp = NIFWrapper()
